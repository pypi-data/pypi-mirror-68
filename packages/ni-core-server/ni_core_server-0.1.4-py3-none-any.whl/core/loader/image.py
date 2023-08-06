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
        self.__params = None

    @property
    def params(self) -> dict:
        return self.__params

    @params.setter
    def params(self, params: dict):
        self.__params = params

    @property
    def date_create(self):
        return self.__date

    @property
    def rename_file(self) -> str:
        return self.__rename_file

    @property
    def extension(self) -> str:
        return self.__extension

    @property
    def content(self):
        return self.__content

    @property
    def name(self):
        return self.__filename


class ImageBuilder:

    def __init__(self, filename, body):
        # Get extension
        extension = filename.split('.')[-1]
        name = "".join(filename.split('.')[:-1])
        rename = f'{str(uuid4())}.{extension}'
        self.__image = Image(body, name, rename, extension, date.today())

    """def operations(self, operations:list) -> None:
        self.__image.operations = operations

    def tags(self, tags:list) -> None:
        self.__image.tags = tags

    def params(self, params:dict) -> None:
        self.__image.params = params"""

    @property
    def image(self) -> Image:
        return self.__image
