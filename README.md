![Build Status](https://github.com/VaultVulp/dypendence/workflows/Main/badge.svg)
![Coverage Badge](https://minio.vaultvulp.dev/coverage/VaultVulp/dypendence/coverage.svg)

# Dypendence

Dependency Injection over Dynaconf

## Usage example

Example `settings.toml`

```toml
[DY.NotificationService]
Type = "PushService"

[DY.NotificationService.SMSService]
some_value = "This is SMSService"

[DY.NotificationService.EmailService]
some_value = "This is EmailService"

[DY.NotificationService.PushService]
some_value = "This is PushService"
```

Example application code:

```python
from dypendence import DY


class NotificationService(DY):

    def send_notification(self) -> str:
        raise NotImplementedError
    
    def get_value_from_settings(self):
        return self.settings.some_value


class SMSService(NotificationService):

    def send_notification(self) -> str:
        return 'Sent SMS Notification'


class EmailService(NotificationService):

    def send_notification(self) -> str:
        return 'Sent Email Notification'


class PushService(NotificationService):

    def send_notification(self) -> str:
        return 'Sent Push Notification'


if __name__ == '__main__':
    notification_service = NotificationService(settings_files=['./tests/settings.toml'])

    assert isinstance(notification_service, PushService)
    assert notification_service.send_notification()
    assert notification_service.get_value_from_settings() == 'This is PushService'
```
