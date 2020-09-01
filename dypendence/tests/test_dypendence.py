from dypendence.dypendence import DY


class FizzBuzz(DY):
    FACTORY_PREFIX = 'SOME_DIFFERENT_PATH'

    @property
    def value(self) -> str:
        raise NotImplementedError

    @property
    def value_from_settings(self) -> str:
        raise NotImplementedError


class Buzz(FizzBuzz):

    @property
    def value(self) -> str:
        return 'Buzz Value'

    @property
    def value_from_settings(self) -> str:
        return self.settings.settings_value


class Fizz(FizzBuzz):

    @property
    def value(self) -> str:
        return 'Fizz Value'

    @property
    def value_from_settings(self) -> str:
        return self.settings.settings_value


def test_buzz_constructor(monkeypatch):
    monkeypatch.setenv('DYNACONF_DY__SOME_DIFFERENT_PATH__FIZZ__SETTINGS_VALUE', 'Fizz from dynaconf settings')
    monkeypatch.setenv('DYNACONF_DY__SOME_DIFFERENT_PATH__BUZZ__SETTINGS_VALUE', 'Buzz from dynaconf settings')
    monkeypatch.setenv('DYNACONF_DY__SOME_DIFFERENT_PATH__TYPE', 'Buzz')

    buzz = FizzBuzz(loaders=['dynaconf.loaders.env_loader'])

    assert isinstance(buzz, Buzz)
    assert buzz.value == 'Buzz Value'
    assert buzz.value_from_settings == 'Buzz from dynaconf settings'


def test_fizz_constructor(monkeypatch):
    monkeypatch.setenv('DYNACONF_DY__SOME_DIFFERENT_PATH__FIZZ__SETTINGS_VALUE', 'Fizz from dynaconf settings')
    monkeypatch.setenv('DYNACONF_DY__SOME_DIFFERENT_PATH__BUZZ__SETTINGS_VALUE', 'Buzz from dynaconf settings')
    monkeypatch.setenv('DYNACONF_DY__SOME_DIFFERENT_PATH__TYPE', 'Fizz')

    fizz = FizzBuzz(loaders=['dynaconf.loaders.env_loader'])

    assert isinstance(fizz, Fizz)
    assert fizz.value == 'Fizz Value'
    assert fizz.value_from_settings == 'Fizz from dynaconf settings'


class NotificationService(DY):

    def send_notification(self) -> str:
        raise NotImplementedError


class SMSService(NotificationService):

    def send_notification(self) -> str:
        return 'Sent SMS Notification'


class EmailService(NotificationService):

    def send_notification(self) -> str:
        return 'Sent Email Notification'


class PushService(NotificationService):

    def send_notification(self) -> str:
        return 'Sent Push Notification'


def test_notification_service_constructor(monkeypatch):
    monkeypatch.setenv('DYNACONF_DY__NOTIFICATIONSERVICE__TYPE', 'SMSService')

    sms_service = NotificationService(loaders=['dynaconf.loaders.env_loader'])

    assert isinstance(sms_service, SMSService)
    assert sms_service.send_notification() == 'Sent SMS Notification'
