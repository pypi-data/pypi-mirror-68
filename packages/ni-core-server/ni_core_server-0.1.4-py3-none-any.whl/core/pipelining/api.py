import json

import tornado
from logging_utils import Chronometer, LogDecorator
from tornado.web import MissingArgumentError

from .pipeline import Pipeline, Step
from ..loader.image import ImageBuilder
from ..loader.rabbit import Messaging

messenger = Messaging()


class StepHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def __validating_submission(self):
        # Validation data presence
        if 'data' not in self.request.body_arguments:
            self.set_status(400)
            self.finish({'error': 'bad request', 'reason': 'No data provided.'})
            return None, None, None, None

        response = self.request.body_arguments['data'][0].decode('utf-8')

        if isinstance(response, str):
            response = response.replace("'", '"')

        print(type(response))
        print(response)
        data = json.loads(response)

        # Validation operations presence
        if 'step_id' not in data:
            self.set_status(400)
            self.finish({'error': 'bad request', 'reason': 'No step_id are provided.'})
            return None, None, None, None

        step_id = data['step_id']

        # Validation step exists
        step = Step.find_by_id(step_id)
        if not step:
            self.set_status(404)
            self.finish({'error': 'bad request', 'reason': 'Step are unknown.'})
            return None, None, None, None

        # Validation pipeline presence
        if 'pipeline_id' not in data:
            self.set_status(400)
            self.finish({'error': 'bad request', 'reason': 'No pipeline_id are provided.'})
            return None, None, None, None

        pipeline_id = data['pipeline_id']
        pipeline = Pipeline.find_by_id(pipeline_id)

        if not pipeline:
            self.set_status(404)
            self.finish({'error': 'bad request', 'reason': 'Pipeline are unknown.'})
            return None, None, None, None

        if 'consumer_id' not in data:
            self.set_status(400)
            self.finish({'error': 'bad request', 'reason': 'No consumer_id are provided.'})
            return None, None, None, None

        consumer_id = data['consumer_id']

        return step, pipeline, consumer_id, data

    @Chronometer(function_name='finish-post-timer')
    @LogDecorator(decorator_log='finish-post-inspect')
    def post(self):  # POST /step?status='start|succeed|failed'
        executer = {'started': self.__started, 'failed': self.__failed, 'succeed': self.__succeed}

        step, pipeline, consumer_id, params = self.__validating_submission()

        if not step:
            return

        status = self.get_argument('status')

        try:
            reason = self.get_argument('status')
        except MissingArgumentError:
            reason = None

        if status in executer:
            method = executer[status]
            should_continue = method(step, pipeline, consumer_id, reason)
            if not should_continue:
                self.set_status(200)
                self.finish("received")
                return
        else:
            self.set_status(400)
            self.finish({'error': 'bad request', 'reason': 'Status are unknown only started|failed|succeed is allowed.'})
            return

        for _, files in self.request.files.items():
            for info in files:
                filename = info["filename"]
                body = info["body"]

                # Création de l'image
                builder = ImageBuilder(filename, body)
                # builder.params(params)
                image = builder.image

                pipeline.image = image

                # Création de la pipeline associée
                messenger.send_to_pipeline(pipeline)
                self.finish({'image': image.name, 'pipeline': pipeline.pipeline_id})

    def __started(self, step, pipeline, consumer_id, reason):
        step.start_job(consumer_id)
        if pipeline.status == 'CREATED':
            pipeline.status = 'IN PROGRESS'
        return False

    def __succeed(self, step, pipeline, consumer_id, reason):
        step.stop_job()
        return True

    def __failed(self, step, pipeline, consumer_id, reason):
        step.failed_job(reason)
        if step.allow_failure:
            return True
        pipeline.failed_pipeline()
        return False


class AdminStepHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    @Chronometer(function_name='admin-pipeline-get-timer')
    @LogDecorator(decorator_log='admin-pipeline-get-inspect')
    def get(self, slug):  # GET /admin/pipelines/_slug_
        if slug == 'list':
            self.set_status(200)
            self.finish({'nb_pipeline': len(Pipeline.objects),
                         'pipelines': [item.__dict__() for item in Pipeline.objects]})
        else:
            pipeline = Pipeline.find_by_oid(slug)
            if not pipeline:
                self.set_status(404)
                self.finish({'error': 'not found', 'reason': "no pipeline exists"})
            else:
                self.set_status(200)
                self.finish(pipeline.__dict__())