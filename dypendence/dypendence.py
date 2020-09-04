from pprint import pprint

from dynaconf import Dynaconf
from dynaconf.utils.boxing import DynaBox


class DYException(Exception):
    pass


class DYInvalidConfigurationException(DYException):

    def __init__(self, required_path: str):
        super().__init__(f'Invalid configuration structure: Key `{required_path.upper()}` is not present')


class DYNotFoundException(DYException):

    def __init__(self, dependency_name: str, allowed_values: str):
        super().__init__(f'Dependency {dependency_name} was not found: available dependencies are {allowed_values}')


class DY:
    GLOBAL_PREFIX: str = 'dy'
    FACTORY_PREFIX: str = None
    TYPE_POSTFIX: str = 'type'

    global_settings: Dynaconf = None
    factory_settings: DynaBox = None

    def __init_subclass__(cls, **kwargs):
        if cls.FACTORY_PREFIX is None:
            cls.FACTORY_PREFIX = cls.__name__

    def __new__(cls, **dynaconf_kwargs):
        cls.global_settings: Dynaconf = Dynaconf(**dynaconf_kwargs)
        cls.factory_settings: DynaBox = cls.global_settings.get(f'{cls.GLOBAL_PREFIX}.{cls.FACTORY_PREFIX}')

        if cls.factory_settings is None:
            pprint(dict(cls.global_settings))
            path = f'{cls.GLOBAL_PREFIX}.{cls.FACTORY_PREFIX}'
            raise DYInvalidConfigurationException(path)

        if not cls.factory_settings.get(cls.TYPE_POSTFIX):
            path = f'{cls.GLOBAL_PREFIX}.{cls.FACTORY_PREFIX}.{cls.TYPE_POSTFIX}'
            raise DYInvalidConfigurationException(path)

        requested_classname = str(cls.factory_settings.get(cls.TYPE_POSTFIX)).upper()

        subclasses = {klass.__name__.upper(): klass for klass in cls.__subclasses__()}

        requested_class = subclasses.get(requested_classname)

        if not requested_class:
            raise DYNotFoundException(
                dependency_name=requested_classname,
                allowed_values=', '.join(subclasses.keys()),
            )
        return super().__new__(requested_class)

    @property
    def settings(self) -> DynaBox:
        classname = type(self).__name__
        return self.factory_settings.get(classname, DynaBox(box_settings={}))
