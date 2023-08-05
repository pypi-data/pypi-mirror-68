import os
import random

import pika
from logging_utils import Chronometer, LogDecorator

RABBIT_HOST = os.getenv('RABBIT_HOST', '127.0.0.1')


class Messaging:

    @staticmethod
    def __create_connection():
        return pika.BlockingConnection(pika.ConnectionParameters(
            host=RABBIT_HOST
        ))

    @Chronometer(function_name='messaging-send-timer')
    @LogDecorator(decorator_log='messaging-send-inspect')
    def send(self, image):

        if image.operations:
            random.shuffle(image.operations)
        else:
            image.operations.append('to_save')

        queue_name = image.operations.pop()

        connexion = Messaging.__create_connection()

        channel = connexion.channel()
        channel.queue_declare(queue=queue_name)

        properties = {'categorie': image.categorie, 'tags': image.tags, 'description': image.description,
                      'nom': image.nom, 'operations': image.operations}

        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=image.file.read(),
            properties=pika.BasicProperties(headers=properties)
        )

        print(f'[x] image sent to {queue_name}')

        connexion.close()

        return queue_name

    @staticmethod
    def get_consumers(queue_name):
        connexion = Messaging.__create_connection()

        channel = connexion.channel()
        queue_state = channel.queue_declare(queue=queue_name)

        return queue_state.method.consumer_count
