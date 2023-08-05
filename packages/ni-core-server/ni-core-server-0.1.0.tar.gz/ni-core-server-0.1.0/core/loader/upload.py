from datetime import date

import tornado
from logging_utils import Chronometer, LogDecorator
from tornado.web import MissingArgumentError

from .image import ImageBuilder
from .rabbit import Messaging
from ..pipelining import PipelineBuilder

messenger = Messaging()


class UploadHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    @Chronometer(function_name='upload-post-timer')
    @LogDecorator(decorator_log='upload-post-inspect')
    def post(self):  # POST /upload

        try:
            tags = self.get_argument('tags')
            if tags:
                tags = tags.split(',')
            else:
                tags = []
        except MissingArgumentError:
            tags = []

        try:
            operations = self.get_argument('operations')
            if operations:
                operations = operations.split(',')
            else:
                operations = []
        except MissingArgumentError:
            operations = []

        print(f"nombre d'images {len(self.request.files)}")
        for _, files in self.request.files.items():
            for info in files:
                filename = info["filename"]
                body = info["body"]

                # Création de l'image
                builder = ImageBuilder(filename, body)
                builder.operations(operations)
                builder.tags(tags)
                image = builder.image

                if image.validate():
                    # Création de la pipeline associée
                    pipeline_builder = PipelineBuilder()
                    pipeline_builder.create(image)
                    pipeline = pipeline_builder.pipeline
                    messenger.send_to_pipeline(pipeline)
                    self.finish({'image': image.rename_file, 'operations': operations})
                else:
                    self.set_status(400)
                    self.finish({'error': 'bad request', 'reason': 'One or more consumers are unknown.'})
