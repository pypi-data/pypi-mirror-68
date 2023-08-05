from datetime import date
from uuid import uuid4

from logging_utils import LogDecorator

from core.consumer.api import Consumer


class Image:

    def __init__(self, content, filename, rename_file, extension, date_creation):
        self.__content = content
        self.__filename = filename
        self.__rename_file = rename_file
        self.__extension = extension
        self.__date_creation = date_creation
        self.__operations = None
        self.__tags = None

    @property
    def tags(self) -> list:
        return self.__tags

    @tags.setter
    def tags(self, tags: list):
        self.__tags = tags

    @property
    def date_create(self):
        return self.__date

    @property
    def operations(self) -> list:
        return self.__operations

    @operations.setter
    def operations(self, operations: list):
        self.__operations = operations

    @property
    def rename_file(self) -> str:
        return self.__rename_file

    @property
    def extension(self) -> str:
        return self.__extension

    @property
    def content(self):
        return self.__content

    @LogDecorator('image-validate-inspect')
    def validate(self):
        # @TODO La validation des consommateurs n'est pas de la responsabilité de l'image
        consumers = [Consumer.find_by_name(operation) for operation in self.__operations]
        return not any(consumer is None for consumer in consumers)


class ImageBuilder:

    def __init__(self, filename, body):
        # Get extension
        extension = filename.split('.')[-1]
        rename = f'{str(uuid4())}.{extension}'
        self.__image = Image(body, filename, rename, extension, date.today())

    def operations(self, operations:list) -> None:
        self.__image.operations = operations

    def tags(self, tags:list) -> None:
        self.__image.tags = tags

    @property
    def image(self) -> Image:
        return self.__image
