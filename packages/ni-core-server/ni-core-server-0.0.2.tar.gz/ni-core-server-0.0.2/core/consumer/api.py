import uuid
import time
from threading import Thread

import tornado
from tornado.web import RequestHandler
from uuid import uuid5

from logging_utils import Chronometer, LogDecorator

from core.loader.rabbit import Messaging


class Consumer:

    objects = []

    @staticmethod
    def find_by_oid(oid):
        try:
            return next(item for item in Consumer.objects if item.oid == oid)
        except StopIteration:
            return None

    @staticmethod
    def find_by_name(name):
        try:
            return next(item for item in Consumer.objects if item.name == name)
        except StopIteration:
            return None

    def __init__(self, name, heartbeat_url, final=False):
        self.__oid = str(uuid5(uuid.NAMESPACE_OID, name))
        self.__name = name
        self.__final = final
        self.__heartbeat_url = heartbeat_url
        self.__class__.objects.append(self)
        self.__alive = True

    @LogDecorator('consumer_del_inspect')
    def __del__(self):
        self.__class__.objects.remove(self)

    def __dict__(self):
        return {'oid': self.__oid, 'name': self.__name, 'heartbeat_url': self.__heartbeat_url, 'final': self.__final,
                'status': 'UP' if self.__alive else 'DOWN'}

    @property
    def name(self):
        return self.__name

    @property
    def final(self):
        return self.__final

    @property
    def oid(self):
        return self.__oid

    @property
    def heartbeat_url(self):
        return self.__heartbeat_url

    @property
    def status(self):
        return 'UP' if self.__alive else 'DOWN'

    @status.setter
    def status(self, value):
        self.__alive = value


class ConsumerHandler(RequestHandler):

    def data_received(self, chunk):
        pass

    @Chronometer(function_name='consumer-post-timer')
    @LogDecorator(decorator_log='consumer-post-inspect')
    def post(self):  # POST /consumer

        consumer_json = tornado.escape.json_decode(self.request.body)

        if 'name' not in consumer_json or 'heartbeat_url' not in consumer_json:
            self.set_status(400)
            self.finish({'error': 'bad request', 'reason': "'name' and 'heartbeat_url' are mandatory."})

        if not Consumer.objects:
            consumer = Consumer(consumer_json['name'], consumer_json['heartbeat_url'],
                                consumer_json['final'] if 'final' in consumer_json else False)
        elif not any(consumer_json['name'] == consumer.name
                     and consumer_json['heartbeat_url'] == consumer.heartbeat_url for consumer in Consumer.objects):
            consumer = Consumer(consumer_json['name'], consumer_json['heartbeat_url'],
                                consumer_json['final'] if 'final' in consumer_json else False)
        else:
            self.set_status(409)
            self.finish({'error': 'conflict', 'reason': "Consumer already register"})

        self.set_status(200)
        self.finish({'consumer': consumer.name, 'register': True,
                     'informations': f"/admin/consumers/{consumer.oid}"})

    @Chronometer(function_name='consumer-delete-timer')
    @LogDecorator(decorator_log='consumer-delete-inspect')
    def delete(self, slug):  # DELETE /consumer/oid
        consumer = Consumer.find_by_oid(slug)

        if not consumer:
            self.set_status(404)
            self.finish({'error': 'not found', 'reason': f"Consumer identified by '{slug}' not exist"})
        else:
            consumer.__del__()
            self.set_status(202)
            self.finish({'action': 'delete', 'msg': f"Consumer identified by '{slug}' not exist anymore"})


class AdminConsumerHandler(RequestHandler):

    def data_received(self, chunk):
        pass

    @Chronometer(function_name='resource-post-timer')
    @LogDecorator(decorator_log='resource-post-inspect')
    def get(self, slug):  # GET /admin/consumers/_slug_
        if slug == 'list':
            self.set_status(200)
            self.finish({'nb_consumers_total': len(Consumer.objects),
                         'consumers': [item.__dict__() for item in Consumer.objects]})
        else:
            consumer = Consumer.find_by_oid(slug)
            if not consumer:
                self.set_status(404)
                self.finish({'error': 'not found', 'reason': "no consumers exists"})
            else:
                self.set_status(200)
                self.finish(consumer.__dict__())


@Chronometer('heartbeat-timer')
def background_task():
    print("Start heartbeat")
    for consumer in Consumer.objects:
        count = Messaging.get_consumers(consumer.name)
        consumer.status = count == 0
    print("Waiting 30 seconds")
    time.sleep(30)


t = Thread(target=background_task)
t.start()
