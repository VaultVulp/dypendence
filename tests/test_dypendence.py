import pytest

from dypendence import DY
from dypendence.dypendence import DYInvalidConfigurationException, DYNotFoundException


class FizzBuzz(DY):
    FACTORY_PREFIX = 'SOME_PATH'

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
    monkeypatch.setenv('DYNACONF_DY__SOME_PATH__BUZZ__SETTINGS_VALUE', 'Buzz from dynaconf settings')
    monkeypatch.setenv('DYNACONF_DY__SOME_PATH__TYPE', 'Buzz')

    buzz = FizzBuzz(loaders=['dynaconf.loaders.env_loader'])

    assert isinstance(buzz, Buzz)
    assert buzz.value == 'Buzz Value'
    assert buzz.value_from_settings == 'Buzz from dynaconf settings'


def test_fizz_constructor(monkeypatch):
    monkeypatch.setenv('DYNACONF_DY__SOME_PATH__FIZZ__SETTINGS_VALUE', 'Fizz from dynaconf settings')
    monkeypatch.setenv('DYNACONF_DY__SOME_PATH__TYPE', 'Fizz')

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


def test_not_found_exception(monkeypatch):
    monkeypatch.setenv('DYNACONF_DY__SOME_PATH__TYPE', 'NotFizzNotBuzz')

    with pytest.raises(DYNotFoundException) as raised_exception:
        FizzBuzz(loaders=['dynaconf.loaders.env_loader'])

    assert 'Dependency NOTFIZZNOTBUZZ was not found' in str(raised_exception.value)


def test_invalid_configuration_exception(monkeypatch):
    with pytest.raises(DYInvalidConfigurationException) as raised_exception:
        FizzBuzz(loaders=['dynaconf.loaders.env_loader'])

    assert 'Invalid configuration structure: Key `DY.SOME_PATH` is not present' == str(raised_exception.value)

    monkeypatch.setenv('DYNACONF_DY__SOME_PATH__WRONG_ELEMENT', 'NotFizzNotBuzz')

    with pytest.raises(DYInvalidConfigurationException) as raised_exception:
        FizzBuzz(loaders=['dynaconf.loaders.env_loader'])

    assert 'Invalid configuration structure: Key `DY.SOME_PATH.TYPE` is not present' == str(raised_exception.value)
