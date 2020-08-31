from dynaconf import Dynaconf


class DYException(Exception):
    pass


class DYNotFoundException(DYException):

    def __init__(self, dependency_name: str, allowed_values: str):
        message = f'Dependency {dependency_name} was not found. Available dependencies are: {allowed_values}.'
        super().__init__(message)


class DY:
    GLOBAL_PREFIX = 'DY'
    CLASS_PREFIX = None
    TYPE_POSTFIX = 'TYPE'
    settings = None

    def __init_subclass__(cls, **kwargs):
        print(f'Classname: {cls.__name__}')
        cls.settings = DY.settings.get(cls.__name__)
        # if not isinstance(cls.CLASS_PREFIX, str):
        #     raise DYException(f'Class-level variable `PREFIX` in class {cls.__name__} must be a dot separated path')

    def __new__(cls, **dynaconf_kwargs):
        global_settings = Dynaconf(**dynaconf_kwargs)
        cls.settings = settings = global_settings.get(f'{cls.GLOBAL_PREFIX}.{cls.CLASS_PREFIX}')

        subclasses = {klass.__name__.upper(): klass for klass in cls.__subclasses__()}

        if not settings.get(cls.TYPE_POSTFIX):
            raise DYException(
                f'Invalid configuration structure: '
                f'Key `{cls.GLOBAL_PREFIX}.{cls.CLASS_PREFIX}.{cls.TYPE_POSTFIX}` not present'
            )

        classname = str(settings.get(cls.TYPE_POSTFIX)).upper()

        if classname not in subclasses:
            raise DYNotFoundException(
                dependency_name=classname,
                allowed_values=', '.join(subclasses.keys()),
            )
        return super().__new__(subclasses[classname])


class DootFactory(DY):
    CLASS_PREFIX = 'DOOT'

    def __new__(cls, *args, **kwargs):
        return super(DootFactory, cls).__new__(cls, *args, **kwargs)

    @property
    def value(self):
        raise NotImplemented


class Dooter(DootFactory):

    @property
    def value(self):
        return 'Dooter'


class Buzz(DootFactory):

    @property
    def value(self):
        return 'Buzz'


class Fizz(DootFactory):

    @property
    def value(self):
        return 'Fizz'


if __name__ == '__main__':
    something = DootFactory(loaders=['dynaconf.loaders.env_loader'])
    print(f'Type: {type(something).__name__}')
    print(something.value)
