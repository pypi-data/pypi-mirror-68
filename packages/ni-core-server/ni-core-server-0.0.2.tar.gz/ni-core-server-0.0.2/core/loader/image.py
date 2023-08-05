from logging_utils import LogDecorator

from core.consumer.api import Consumer


class Image:

    def __init__(self,
                 description=None,
                 categorie=None,
                 tags=None,
                 date=None,
                 date_update=None,
                 nom=None,
                 file=None,
                 operations=None):

        """
        Constructeur de la classe Image
        :param description: Description de l'image
        :param categorie: Catégorie de l'image
        :param tags: Tags de l'image
        :param date: Date de création de l'image
        :param date_update: Date de mise à jour de l'image
        :param nom: Nom de l'imagePOST
        :param file: Fichier image
        """
        self.__description = description
        self.__categorie = categorie
        self.__tags = tags
        self.__date = date
        self.__date_update = date_update
        self.__nom = nom
        self.__file = file
        self.__operations = operations

        if not self.__operations:
            self.__operations = []

        if not self.__tags:
            self.__tags = []

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    @property
    def nom(self):
        return self.__nom

    @nom.setter
    def nom(self, value):
        self.__nom = value

    @property
    def file(self):
        return self.__file

    @file.setter
    def file(self, value):
        self.__file = value

    @property
    def tags(self) -> list:
        return self.__tags

    @tags.setter
    def tags(self, tags: list):
        self.__tags = tags

    @property
    def date_create(self):
        return self.__date

    @date_create.setter
    def date_create(self, value):
        self.__date = value

    @property
    def date_update(self):
        return self.__date_update

    @date_update.setter
    def date_update(self, value):
        self.__date_update = value

    @property
    def categorie(self):
        return self.__categorie

    @categorie.setter
    def categorie(self, value):
        self.__categorie = value

    @property
    def operations(self) -> list:
        return self.__operations

    @operations.setter
    def operations(self, value: list):
        self.__operations = value

    @LogDecorator('imag-validate-inspect')
    def validate(self):
        consumers = [Consumer.find_by_name(operation) for operation in self.__operations]

        if any(consumer is None for consumer in consumers):
            print("Error on unknown consumer")
            return False

        if sum(consumer.final for consumer in consumers) != 1:
            print("Error on non-final consumer")
            return False

        return True

