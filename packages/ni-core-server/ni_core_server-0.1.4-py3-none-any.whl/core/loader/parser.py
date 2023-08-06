import yaml
from logging_utils import Chronometer

from core.pipelining.pipeline import Step, StepBuilder


def context_except(item_except):
    """
    {'width': { 'le': 100 }}
    where
    width is left_expression (not calculate now)
    le operator
    100 is right_expression
    """
    except_rules = []
    for item in item_except:
        to_calculate = next(iter(item))
        next_calculus = item[to_calculate]
        operator = next(iter(next_calculus))
        right_value = next_calculus[operator]

        except_rules.append({'l': to_calculate, 'o': operator, 'r': right_value})

    print(except_rules)
    return except_rules


class PipelineParser:

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
            if 'except' in item:
                except_rules = context_except(item['except'])
                step.except_rules = except_rules

            steps.append(step)

        return steps