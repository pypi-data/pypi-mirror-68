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

    @Chronometer(function_name='finish-post-timer')
    @LogDecorator(decorator_log='finish-post-inspect')
    def post(self):  # POST /finish
        # Get parameters
        try:
            tags = self.get_argument('tags')
            if tags:
                tags = tags.split(',')
            else:
                tags = []
        except MissingArgumentError:
            tags = []

        operations = self.get_argument('operations')
        pipeline_id = self.get_argument('pipeline_id')
        pipeline = Pipeline.find_by_id(pipeline_id)

        step_id = self.get_argument('step_id')
        step = Step.find_by_id(step_id)

        consumer_id = self.get_argument('consumer_id')

        step.stop_job(consumer_id)

        for _, files in self.request.files.items():
            for info in files:
                filename = info["filename"]
                body = info["body"]

                builder = ImageBuilder(filename, body)
                builder.operations(operations)
                builder.tags(tags)
                image = builder.image

                pipeline.image = image

                messenger.send_to_pipeline(pipeline)


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