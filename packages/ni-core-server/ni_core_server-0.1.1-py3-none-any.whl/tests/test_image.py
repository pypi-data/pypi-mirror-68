from unittest import TestCase

from .context import ImageBuilder


class ImageTest(TestCase):

    def test_file(self):
        file = open("resources/image.jpeg", "rb")
        builder = ImageBuilder("image.jpeg", file.read())
        image = builder.image
        self.assertIsNotNone(image)
