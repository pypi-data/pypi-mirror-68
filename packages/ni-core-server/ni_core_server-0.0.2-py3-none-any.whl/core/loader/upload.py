from datetime import date

import tornado
from logging_utils import Chronometer, LogDecorator
from tornado.web import MissingArgumentError

from .image import Image
from .rabbit import Messaging

messenger = Messaging()


class UploadHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    @Chronometer(function_name='upload-post-timer')
    @LogDecorator(decorator_log='upload-post-inspect')
    def post(self):  # POST /upload

        try:
            nom = self.get_argument('nom')
        except MissingArgumentError:
            nom = None

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

        description = self.get_argument('description')
        date_create = date.today()
        categorie = self.get_argument('categorie')

        print(f"nombre d'images {len(self.request.files)}")
        for _, files in self.request.files.items():
            for info in files:
                filename = info["filename"]
                body = info["body"]

                output_file = open("upload/" + filename, "wb")
                output_file.write(body)

                input_file = open("upload/" + filename, "rb")

                image = Image(
                    description=description,
                    categorie=categorie,
                    tags=tags,
                    date=date_create,
                    nom=nom,
                    file=input_file,
                    operations=operations)

                if image.validate():
                    messenger.send(image)
                    self.finish({'image': nom, 'operations': operations})
                else:
                    self.set_status(400)
                    self.finish({'error': 'bad request', 'reason': 'consumers are not valid'})
