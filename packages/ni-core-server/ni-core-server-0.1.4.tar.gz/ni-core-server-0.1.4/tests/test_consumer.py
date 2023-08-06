import json
from unittest import TestCase

import tornado

from core.consumer.api import Consumer
from core.cm.commandLine import Application


class ConsumerEndpointsTest(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        return Application()

    def validate_response_consumers(self, status_code, nb_consumers, consumer_list):
        response = self.fetch("/admin/consumers/list")
        self.assertEqual(response.code, status_code)
        json_response = json.loads(response.body)
        print(json_response)
        self.assertEqual(json_response['nb_consumers_total'], nb_consumers)
        self.assertEqual(json_response['consumers'], consumer_list)

    def create_and_post_consumer(self, consumer_name, consumer_tag):
        test_consumer = {'name': consumer_name, 'tag': consumer_tag}
        response_post = self.fetch("/consumer", method='POST', body=json.dumps(test_consumer))
        self.assertEqual(response_post.code, 200)
        json_response = json.loads(response_post.body)
        cid = json_response['informations'].split("/")[-1].strip()
        self.assertIsNotNone(cid)
        return cid

    def test_add_consumer(self):
        self.validate_response_consumers(200, 0, [])

        consumer_1_cid = self.create_and_post_consumer("consumer", "tag1")

        consumer_list = [{'oid': consumer_1_cid, 'name': 'consumer', 'rabbit_tag': 'tag1'}]
        self.validate_response_consumers(200, 1, consumer_list)

        consumer_conflict = {'name': 'consumer', 'tag': 'tag1'}
        response_conflict = self.fetch("/consumer", method='POST', body=json.dumps(consumer_conflict))
        self.assertEqual(response_conflict.code, 409)

        response_not_found = self.fetch("/admin/consumers/test")
        self.assertEqual(response_not_found.code, 404)

        response = self.fetch(f"/admin/consumers/{consumer_1_cid}")
        self.assertEqual(response.code, 200)

        response_delete_not_found = self.fetch("/consumer/test", method='DELETE')
        self.assertEqual(response_delete_not_found.code, 404)

        response_delete = self.fetch(f"/consumer/{consumer_1_cid}", method='DELETE')
        self.assertEqual(response_delete.code, 202)

        self.validate_response_consumers(200, 0, [])


class ConsumerTest(TestCase):

    def test_should_be_registered(self):
        print(Consumer.objects)
        consumer = Consumer("test", "tag")
        self.assertEqual(len(Consumer.objects), 1)
        self.assertEqual(consumer.name, "test")
        self.assertEqual(consumer.tag, "tag")
        self.assertIsNotNone(consumer.oid)

        consumer_found = Consumer.find_by_name("test")
        self.assertEqual(consumer, consumer_found)

        consumer.__del__()
        self.assertEqual(len(Consumer.objects), 0)