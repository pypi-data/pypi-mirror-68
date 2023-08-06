import json

import requests

from core.pipelining.pipeline import Step, Pipeline
from .common import BaseHttpTestCase


class StatusEndpointsTest(BaseHttpTestCase):

    def setUp(self):
        super().setUp()
        # self.__prepare()

    def __prepare(self):
        self.create_and_post_consumer("tagger", "tagger:1")
        self.create_and_post_consumer("resizer", "resizer:1")
        self.create_and_post_consumer("cropper", "cropper:1")

    def _submit_request(self, url, path_image, path_pipeline_file):
        content_type, body = self.prepare_image(path_image, path_pipeline_file)
        headers = {
            "Content-Type": content_type,
        }
        return self.fetch(url, method='POST', body=body, headers=headers)

    def prepare_image_step(self, image_path, data):
        _, port = self.http_server._sockets[16].getsockname()

        f = open(image_path, 'rb')

        files = {"image": f}

        a = requests.Request(url=f"http://localhost:{port}", files=files, data=data)
        prepare = a.prepare()
        content_type = prepare.headers.get('Content-Type')
        body = prepare.body

        return content_type, body

    def _submit_request_job(self, url, path_image, data):
        content_type, body = self.prepare_image_step(path_image, data)
        headers = {
            "Content-Type": content_type,
        }
        return self.fetch(url, method='POST', body=body, headers=headers)

    def test_pipeline_success_one_job(self):
        self.reset()
        self.create_and_post_consumer("tagger", "tagger:1")
        response = self._submit_request("/upload", "resources/image.jpeg", "resources/only_tagger/.ni-pipeline.yml")

        self.assertEqual(response.code, 200)
        response_json = json.loads(response.body)
        pipeline_id = response_json['pipeline']
        self.assertEqual(len(Pipeline.objects), 1)
        pipeline = Pipeline.objects[0]
        print(pipeline.__dict__())
        self.assertEqual(len(pipeline.steps), 1)
        self.assertEqual(pipeline.status, 'CREATED')

        step = pipeline.steps[0]
        self.assertEqual(step.status, 'PENDING')
        self.assertIsNotNone(step.__dict__()['submission_time'])
        self.assertIsNone(step.__dict__()['start_time'])
        self.assertIsNone(step.__dict__()['end_time'])

        data = {"data": [{"step_id": step.step_id}]}
        response_job = self._submit_request_job("/step?status=started", "resources/image.jpeg", data)
        self.assertEqual(response_job.code, 400)

        data = {"data": [{"step_id": step.step_id, "pipeline_id": pipeline.pipeline_id}]}
        response_job = self._submit_request_job("/step?status=started", "resources/image.jpeg", data)
        self.assertEqual(response_job.code, 400)

        # Job is started
        data = {"data": [{"step_id": step.step_id, "pipeline_id": pipeline.pipeline_id,
                          "consumer_id": "tagger:1"}]}
        response_job = self._submit_request_job("/step?status=started", "resources/image.jpeg", data)

        print(f"response: ==============================================msg=========================> {response_job.body}")
        print(f"response: ==============================================msg=========================> {response_job.code}")
        self.assertEqual(response_job.code, 200)
        self.assertEqual(pipeline.status, 'IN PROGRESS')
        self.assertEqual(step.status, 'IN PROGRESS')
        self.assertIsNotNone(step.__dict__()['submission_time'])
        self.assertIsNotNone(step.__dict__()['start_time'])
        self.assertIsNone(step.__dict__()['end_time'])

        # Job is succeed
        data = {"data": [{"step_id": step.step_id, "pipeline_id": pipeline.pipeline_id,
                          "consumer_id": "tagger:1"}]}
        response_job = self._submit_request_job("/step?status=succeed", "resources/image.jpeg", data)
        self.assertEqual(response_job.code, 200)
        self.assertEqual(step.status, 'FINISHED')
        self.assertIsNotNone(step.__dict__()['submission_time'])
        self.assertIsNotNone(step.__dict__()['start_time'])
        self.assertIsNotNone(step.__dict__()['end_time'])
        self.assertEqual(pipeline.status, 'FINISHED')
