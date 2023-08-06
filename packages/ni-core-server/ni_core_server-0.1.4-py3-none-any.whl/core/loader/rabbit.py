import logging
import os

import pika
from logging_utils import Chronometer, LogDecorator

RABBIT_HOST = os.getenv('RABBIT_HOST', '127.0.0.1')


class Messaging:

    @staticmethod
    def __create_connection():
        return pika.BlockingConnection(pika.ConnectionParameters(
            host=RABBIT_HOST
        ))

    def __init__(self):
        self.__log = logging.getLogger('Messaging')

    def __send_message(self,pipeline, step):
        connexion = Messaging.__create_connection()

        channel = connexion.channel()
        channel.queue_declare(queue=step.name)

        properties = {'operations': pipeline.operations, 'pipeline': pipeline.pipeline_id, 'step': step.step_id,
                      'params': step.variables, 'name': pipeline.image.name, 'extension': pipeline.image.extension}

        channel.basic_publish(
            exchange='',
            routing_key=step.name,
            body=pipeline.image.content,
            properties=pika.BasicProperties(headers=properties)
        )

        self.__log.debug(f'[x] image sent to {step.name}')

        connexion.close()

        return step.name

    @Chronometer(function_name='pipeline-send-timer')
    @LogDecorator(decorator_log='pipeline-send-inspect')
    def send_to_pipeline(self, pipeline):
        # Get Next step
        try:
            next_step = next(x for x in pipeline.steps if x.status == 'CREATED')
        except StopIteration:
            self.__log.debug('No more step found, pipeline ending')
            pipeline.stop_pipeline()
            return

        next_step.launch_job()
        self.__send_message(pipeline, next_step)

    @staticmethod
    def get_consumers(queue_name) -> int:
        connexion = Messaging.__create_connection()

        channel = connexion.channel()
        queue_state = channel.queue_declare(queue=queue_name)

        return queue_state.method.consumer_count
