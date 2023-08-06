from datetime import date, datetime
from uuid import uuid4

from logging_utils import LogDecorator

from ..loader.image import Image


class Pipeline:

    objects = []

    def __init__(self, image: Image) -> None:
        """
        Une pipeline est une succession d'étape

        """
        self.__pipeline_id = str(uuid4())
        self.__status = 'CREATED'
        self.__start_time = datetime.now()
        self.__end_time = None
        self.__image = image
        self.__steps = None
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

    @property
    def pipeline_id(self):
        return self.__pipeline_id

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


class Step:

    objects = []

    def __init__(self, name):
        self.__step_id = str(uuid4())
        self.__status = 'CREATED'
        self.__start_time = None
        self.__end_time = None
        self.__name = name
        self.__coid = None
        self.__class__.objects.append(self)

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

    def launch_job(self):
        self.__start_time = datetime.now()
        self.__status = 'IN PROGRESS'

    def stop_job(self, consumer_id):
        self.__end_time = datetime.now()
        self.__coid = consumer_id
        self.__status = 'FINISHED'

    def __dict__(self):
        return {'step_id': self.__step_id, 'name': self.__name, 'consumer': self.__coid,
                'start_time': self.__start_time.strftime("%m/%d/%Y, %H:%M:%S") if self.__start_time else None,
                'end_time': self.__end_time.strftime("%m/%d/%Y, %H:%M:%S") if self.__end_time else None,
                'status': self.__status}


class PipelineBuilder:

    def __init__(self) -> None:
        self.__pipeline = None

    def __reset(self):
        self.__pipeline = None

    def create(self, image: Image) -> None:
        self.__pipeline = Pipeline(image)
        self.__pipeline.steps = [Step(operation) for operation in image.operations]

    @property
    def pipeline(self):
        pipeline = self.__pipeline
        self.__reset()
        return pipeline
