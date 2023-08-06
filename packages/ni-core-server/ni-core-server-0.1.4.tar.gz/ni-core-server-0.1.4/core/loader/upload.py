import json

import puremagic
import tornado
from logging_utils import Chronometer, LogDecorator
from tornado.web import MissingArgumentError

from .image import ImageBuilder
from .parser import PipelineParser
from .rabbit import Messaging
from ..consumer.api import Consumer
from ..pipelining import PipelineBuilder
from ..pipelining.pipeline import Step, StepBuilder

messenger = Messaging()


class UploadHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def __extract_images(self):
        images = []
        for _, files in self.request.files.items():
            for info in files:
                filename = info["filename"]
                body = info["body"]

                # test mimemagic
                try:
                    mime_type = puremagic.from_string(body, mime=True)
                    if mime_type.split('/')[0] == 'image':
                        builder = ImageBuilder(filename, body)
                        # builder.params(params)
                        images.append(builder.image)
                except puremagic.PureError:
                    pass

        if not images:
            self.set_status(400)
            self.finish({'error': 'bad request', 'reason': 'No images provided.'})

        return images

    def __extract_pipeline(self):
        for _, files in self.request.files.items():
            for info in files:
                filename = info["filename"]
                body = info["body"]

                if filename == '.ni-pipeline.yml':
                    parser = PipelineParser(body)
                    return parser.parse()

        return None

    def __validating_submission(self):
        steps_builder = self.__extract_pipeline()

        operations = [step_builder.name for step_builder in steps_builder]

        # Validation consumer exists
        consumers = [Consumer.find_by_name(operation) for operation in operations]

        if any(consumer is None for consumer in consumers):
            self.set_status(400)
            self.finish({'error': 'bad request', 'reason': 'One or more consumers are unknown.'})
            return None, None, None

        images = self.__extract_images()

        if not images:
            return None, None, None

        return operations, images, steps_builder

    @Chronometer(function_name='upload-post-timer')
    @LogDecorator(decorator_log='upload-post-inspect')
    def post(self):  # POST /upload

        operations, images, steps_builder = self.__validating_submission()

        if not operations:
            return

        print(f"nombre d'images {len(self.request.files)}")
        for image in images:
            # Création de la pipeline associée
            pipeline_builder = PipelineBuilder()
            pipeline_builder.create(image, operations, [step_builder.build() for step_builder in steps_builder
                                                        if step_builder.validate(image)])
            pipeline = pipeline_builder.pipeline
            messenger.send_to_pipeline(pipeline)
            self.finish({'image': image.name, 'pipeline': pipeline.pipeline_id})
