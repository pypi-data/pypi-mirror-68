from core.loader.parser import PipelineParser
from tests.common import BaseHttpTestCase


class ParserTest(BaseHttpTestCase):

    def test_should_parse_file(self):
        with open("resources/pipeline.yaml", "rb") as configuration:
            content = configuration.read()
            parser = PipelineParser(content)

        steps_builder = parser.parse()
        self.assertEqual(len(steps_builder), 3)

        step_tagger = steps_builder[0].build()

        self.assertEqual(step_tagger.name, 'tagger')
        self.assertEqual(len(step_tagger.variables), 0)
        self.assertFalse(step_tagger.allow_failure)

        step_resizer = steps_builder[1].build()

        self.assertEqual(step_resizer.name, 'resizer')
        self.assertEqual(len(step_resizer.variables), 1)
        self.assertFalse(step_resizer.allow_failure)
        self.assertEqual(step_resizer.variables[0], {'width_size': 100})

        step_cropper = steps_builder[2].build()

        self.assertEqual(step_cropper.name, 'crop-and-resize')
        self.assertEqual(len(step_cropper.variables), 0)
        self.assertTrue(step_cropper.allow_failure)

        BaseHttpTestCase.reset()

    def should_use_pipeline_file(self):
        pass
