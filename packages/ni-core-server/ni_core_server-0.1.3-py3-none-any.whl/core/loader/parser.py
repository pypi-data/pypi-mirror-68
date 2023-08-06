import yaml
from logging_utils import Chronometer

from core.pipelining.pipeline import Step, StepBuilder


class Pipeline_Parser:

    def __init__(self, parse_file):
        self.__configuration_file = parse_file
        self.__steps = None

    def parse(self):
        docs = yaml.load_all(self.__configuration_file, Loader=yaml.FullLoader)

        for doc in docs:
            for key, value in doc.items():
                if key == 'steps':
                    self.__steps = value
                elif key == 'variables':
                    self.__global_variables = value

        return self.__extract_steps(self.__steps)

    @Chronometer('extract-steps-inspect')
    def __extract_steps(self, steps_configuration, global_variables=None):
        """
        ```
        - name: step_name
          variables:return
            - var1: value1
          allow-failure: true|false (false by default)
        ```
        :param steps_configuration:
        :return:
        """
        steps = []
        for item in steps_configuration:
            step = StepBuilder(item['name'])
            variables = []
            if global_variables:
                variables = global_variables

            if 'variables' in item:
                variables.extend(item['variables'])
                step.variables = variables
            if 'allow-failure' in item:
                step.allow_failure = item['allow-failure']

            steps.append(step)

        return steps