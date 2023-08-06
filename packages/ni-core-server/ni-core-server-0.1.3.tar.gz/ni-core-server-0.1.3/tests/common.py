import json

import requests
import tornado

from core.cm.commandLine import Application
from core.consumer.api import Consumer
from core.pipelining.pipeline import Pipeline, Step


class BaseHttpTestCase(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        return Application()

    def setUp(self):
        BaseHttpTestCase.reset()
        super().setUp()

    @staticmethod
    def reset():
        [pipeline.__del__() for pipeline in Pipeline.objects]
        [step.__del__() for step in Step.objects]
        [consumer.__del__() for consumer in Consumer.objects]

    def prepare_image(self, image_path, path_pipeline_file):
        _, port = self.http_server._sockets[16].getsockname()

        f = open(image_path, 'rb')
        p = open(path_pipeline_file, 'rb')

        files = {"image": f, "pipeline": p}

        data = {}

        a = requests.Request(url=f"http://localhost:{port}", files=files, data=data)
        prepare = a.prepare()
        content_type = prepare.headers.get('Content-Type')
        body = prepare.body

        return content_type, body

    def create_and_post_consumer(self, consumer_name, consumer_tag):
        test_consumer = {'name': consumer_name, 'tag': consumer_tag}
        response_post = self.fetch("/consumer", method='POST', body=json.dumps(test_consumer))
        self.assertEqual(response_post.code, 200)
        json_response = json.loads(response_post.body)
        cid = json_response['informations'].split("/")[-1].strip()
        self.assertIsNotNone(cid)
        return cid

    def job_send_status(self, status):
        response_post = self.fetch("/status", method='POST', body=json.dumps(test_consumer))

