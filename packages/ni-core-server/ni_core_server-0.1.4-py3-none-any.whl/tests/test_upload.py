import json

import requests

from core.consumer.api import Consumer
from core.pipelining.pipeline import Step, Pipeline
from .common import BaseHttpTestCase


class UploadEndpointsTest(BaseHttpTestCase):

    def validate_response_no_pipeline(self):
        response = self.fetch("/admin/pipelines/list")
        self.assertEqual(response.code, 200)
        json_response = json.loads(response.body)
        print(json_response)
        self.assertEqual(json_response['nb_pipeline'], 0)
        self.assertEqual(json_response['pipelines'], [])

    def test_upload_without_images(self):
        self.create_and_post_consumer("tagger", "tag1")
        content_type, body = self.prepare_image("resources/test.txt", "resources/only_tagger/.ni-pipeline.yml")
        url = "/upload"
        headers = {
            "Content-Type": content_type,
        }

        response = self.fetch(url, method='POST', body=body, headers=headers)

        self.assertEqual(response.code, 400)
        json_response = json.loads(response.body)
        self.assertEqual(json_response['error'], "bad request")
        self.assertEqual(json_response['reason'], "No images provided.")

    def test_add_pipeline(self):
        self.reset()
        self.validate_response_no_pipeline()

        content_type, body = self.prepare_image("resources/image.jpeg", "resources/only_tagger/.ni-pipeline.yml")
        url = "/upload"
        headers = {
            "Content-Type": content_type,
        }

        response = self.fetch(url, method='POST', body=body, headers=headers)

        self.assertEqual(response.code, 400)
        json_response = json.loads(response.body)
        self.assertEqual(json_response['error'], "bad request")
        self.assertEqual(json_response['reason'], "One or more consumers are unknown.")

        self.create_and_post_consumer("tagger", "tag1")
        response = self.fetch(url, method='POST', body=body, headers=headers)

        self.assertEqual(response.code, 200)

        json_response = json.loads(response.body)

        self.assertIsNotNone(json_response['pipeline'])
        self.assertEqual(json_response['image'], 'image')

        self.assertEqual(len(Step.objects), 1)
        step = Step.objects[0]
        self.assertEqual(step.status, 'PENDING')

    def test_upload_multiple_files(self):
        self.reset()
        self.create_and_post_consumer("tagger", "tag1")

        _, port = self.http_server._sockets[16].getsockname()

        f1 = open("resources/image.jpeg", 'rb')
        f2 = open("resources/temp.jpeg", 'rb')
        f3 = open("resources/test.txt", 'rb')
        f4 = open("resources/only_tagger/.ni-pipeline.yml", 'rb')
        files = {"image1": f1, "image2": f2, 'image3': f3, 'image4': f4}
        data = {}

        a = requests.Request(url=f"http://localhost:{port}", files=files, data=data)
        prepare = a.prepare()
        content_type = prepare.headers.get('Content-Type')
        body = prepare.body

        url = "/upload"
        headers = {
            "Content-Type": content_type,
        }

        response = self.fetch(url, method='POST', body=body, headers=headers)
        self.assertEqual(response.code, 200)
        self.assertEqual(len(Pipeline.objects), 2)
        self.assertEqual(len(Step.objects), 2)
