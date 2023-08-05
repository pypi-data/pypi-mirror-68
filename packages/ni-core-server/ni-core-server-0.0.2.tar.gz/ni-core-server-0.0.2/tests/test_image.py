from unittest import TestCase

from .context import Image


class ImageTest(TestCase):

    def test_name(self):
        image = Image(nom='test')
        self.assertEqual('test', image.nom, "Name should be test")
        image.nom = 'override'
        self.assertEqual('override', image.nom, "Name should be override")
        image.nom = None
        self.assertIsNone(image.nom, "Name should be None")

    def test_tags(self):
        image = Image(tags=['voiture', 'vacance'])
        self.assertEqual(['voiture', 'vacance'], image.tags, "Tags should be voiture and vacance")
        image.tags = ['soleil']
        self.assertEqual(['soleil'], image.tags, "Tags should be soleil")
        image.tags = None
        self.assertIsNone(image.tags, "Tags should be None")

    def test_none_tags(self):
        image = Image()
        self.assertEqual([], image.tags, "Tags should be empty")

    def test_operations(self):
        image = Image(operations=['tagger', 'resizer'])
        self.assertEqual(['tagger', 'resizer'], image.operations, "Tags should be tagger and resizer")
        image.operations = ['tagger']
        self.assertEqual(['tagger'], image.operations, "Tags should be tagger")
        image.operations = None
        self.assertIsNone(image.operations, "Tags should be None")

    def test_file(self):
        file = open("resources/image.jpeg", "rb")
        image = Image(file=file)
        self.assertEqual(file, image.file, "Le fichier ne correspond pas lors de l'initialisation")
        temp = open("resources/temp.jpeg", "rb")
        image.file = temp
        self.assertEqual(temp, image.file, "Le fichier ne correspond pas lors du setter")
        image.file = None
        self.assertIsNone(image.file, "File should be None")
