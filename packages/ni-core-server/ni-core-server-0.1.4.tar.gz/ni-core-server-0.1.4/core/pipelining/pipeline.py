import io
from datetime import datetime
from PIL import Image as PilImage
from uuid import uuid4


from logging_utils import LogDecorator

from .expression import GreaterThanExpression, GreaterOrEqualExpression, LikeExpression, LessOrEqualExpression, \
    LessThanExpression, TerminalExpression
from ..loader.image import Image


class Pipeline:

    objects = []

    def __init__(self, image: Image, operations: list) -> None:
        """
        Une pipeline est une succession d'étape

        """
        self.__pipeline_id = str(uuid4())
        self.__status = 'CREATED'
        self.__start_time = datetime.now()
        self.__end_time = None
        self.__image = image
        self.__steps = None
        self.__operations = operations
        self.__class__.objects.append(self)

    @staticmethod
    def find_by_id(pipeline_id):
        try:
            return next(item for item in Pipeline.objects if item.pipeline_id == pipeline_id)
        except StopIteration:
            return None

    @LogDecorator('pipeline_del_inspect')
    def __del__(self):
        self.__class__.objects.remove(self)

    def __dict__(self):
        return {'pipeline_id': self.__pipeline_id, 'start_time': self.__start_time.strftime("%m/%d/%Y, %H:%M:%S"),
                'end_time': self.__end_time.strftime("%m/%d/%Y, %H:%M:%S") if self.__end_time else None,
                'status': self.__status, 'steps': [step.__dict__() for step in self.__steps]}

    def stop_pipeline(self):
        self.__end_time = datetime.now()
        self.__status = 'FINISHED'

    @LogDecorator('failed-pipeline-inspect')
    def failed_pipeline(self):
        self.__end_time = datetime.now()
        self.__status = 'FAILED'

    @property
    def pipeline_id(self):
        return self.__pipeline_id

    @property
    def operations(self):
        return self.__operations

    @property
    def steps(self) -> list:
        return self.__steps

    @steps.setter
    def steps(self, values:list) -> None:
        self.__steps = values

    @property
    def image(self) -> Image:
        return self.__image

    @image.setter
    def image(self, value) -> None:
        self.__image = value

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, value: str) -> None:
        self.__status = value


class Step:

    objects = []

    def __init__(self, name):
        self.__step_id = str(uuid4())
        self.__status = 'CREATED'
        self.__submission_time = None
        self.__start_time = None
        self.__end_time = None
        self.__name = name
        self.__coid = None
        self.__error_message = None
        self.__class__.objects.append(self)
        self.__allow_failure = False
        self.__variables = []

    @staticmethod
    def find_by_id(step_id):
        try:
            return next(item for item in Step.objects if item.step_id == step_id)
        except StopIteration:
            return None

    @LogDecorator('step_del_inspect')
    def __del__(self):
        self.__class__.objects.remove(self)

    @property
    def status(self):
        return self.__status

    @property
    def step_id(self):
        return self.__step_id

    @property
    def name(self):
        return self.__name

    @property
    def variables(self):
        return self.__variables

    @property
    def allow_failure(self):
        return self.__allow_failure

    @allow_failure.setter
    def allow_failure(self, value):
        self.__allow_failure = value

    def add_variable(self, variable):
        self.__variables.append(variable)

    def add_variables(self, variables):
        self.__variables.extend(variables)

    def launch_job(self):
        self.__submission_time = datetime.now()
        self.__status = 'PENDING'

    def start_job(self, consumer_id):
        self.__start_time = datetime.now()
        self.__coid = consumer_id
        self.__status = 'IN PROGRESS'

    def stop_job(self):
        self.__end_time = datetime.now()
        self.__status = 'FINISHED'

    @LogDecorator('failed-job-inspect')
    def failed_job(self, reason):
        self.__end_time = datetime.now()
        self.__error_message = reason
        self.__status = 'FAILED'

    def __dict__(self):
        return {'step_id': self.__step_id, 'name': self.__name, 'consumer': self.__coid,
                'submission_time': self.__submission_time.strftime("%m/%d/%Y, %H:%M:%S") if self.__submission_time else
                None, 'start_time': self.__start_time.strftime("%m/%d/%Y, %H:%M:%S") if self.__start_time else None,
                'end_time': self.__end_time.strftime("%m/%d/%Y, %H:%M:%S") if self.__end_time else None,
                'status': self.__status, 'error_message': self.__error_message, 'variables': self.__variables}


def get_image_name(image):
    return f'{image.name}.{image.extension}'


def get_image_width(image):
    im = PilImage.open(io.BytesIO(image.content))
    w, _ = im.size
    return w


def get_image_height(image):
    im = PilImage.open(io.BytesIO(image.content))
    _, h = im.size
    return h


class StepBuilder:

    __operator = {'gt': GreaterThanExpression,
                'ge': GreaterOrEqualExpression,
                'like': LikeExpression,
                'lt': LessThanExpression,
                'le': LessOrEqualExpression}

    __left_item = {'name': get_image_name, 'width': get_image_width, 'height': get_image_height}

    def __init__(self, name):
        self.__name = name
        self.__variables = None
        self.__allow_failure = False
        self.__except_rules = None

    @property
    def variables(self):
        return self.__variables

    @property
    def name(self):
        return self.__name

    @variables.setter
    def variables(self, values):
        self.__variables = values

    @property
    def allow_failure(self):
        return self.__allow_failure

    @allow_failure.setter
    def allow_failure(self, value):
        self.__allow_failure = value

    @property
    def except_rules(self):
        return self.__except_rules

    @except_rules.setter
    def except_rules(self, values):
        self.__except_rules = values

    def build(self):
        step = Step(self.__name)
        if self.__variables:
            step.add_variables(self.__variables)
        step.allow_failure= self.__allow_failure

        return step

    def validate(self, image) -> bool:
        """
        {'l':'width', 'o'; 'gt', 'r': 100}
        :param image:
        :return:
        """
        if not self.__except_rules:
            return True

        result_calculus = []
        for item in self.__except_rules:
            # Get left value
            left_value = StepBuilder.__left_item[item['l']](image)
            left_expression = TerminalExpression(left_value)
            right_expression = TerminalExpression(item['r'])
            operator = StepBuilder.__operator[item['o']](left_expression, right_expression)
            result_calculus.append(operator.interpret())
        return not all(result_calculus)


class PipelineBuilder:

    def __init__(self) -> None:
        self.__pipeline = None

    def __reset(self):
        self.__pipeline = None

    def create(self, image: Image, operations: list, steps: list = None) -> None:
        self.__pipeline = Pipeline(image, operations)
        if not steps:
            self.__pipeline.steps = [Step(operation) for operation in operations]
        else:
            self.__pipeline.steps = steps

    @property
    def pipeline(self):
        pipeline = self.__pipeline
        self.__reset()
        return pipeline
