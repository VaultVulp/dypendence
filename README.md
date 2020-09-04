![Build Status](https://github.com/VaultVulp/dypendence/workflows/Main/badge.svg)
![Coverage Badge](https://minio.vaultvulp.dev/coverage/VaultVulp/dypendence/coverage.svg)

# Dypendence

Dependency Injection over Dynaconf

## Usage example

Example `settings.toml`

```toml
[DY.some_path]
type = "Buzz"

[DY.some_path.Buzz]
some_value = "Buzz from settings file"

[DY.some_path.Fizz]
some_value = "Fizz from settings file"
```

Example application code:

```python
from dypendence import DY

class FizzBuzz(DY):
    FACTORY_PREFIX = 'SOME_PATH'

    @property
    def value(self) -> str:
        raise NotImplementedError

    @property
    def value_from_settings(self) -> str:
        return str(self.settings.some_value)


class Buzz(FizzBuzz):

    @property
    def value(self) -> str:
        return 'Buzz Value'


class Fizz(FizzBuzz):

    @property
    def value(self) -> str:
        return 'Fizz Value'
    
if __name__ == '__main__':
    buzz = FizzBuzz(settings_files=['./tests/settings.toml'])

    assert isinstance(buzz, Buzz)
    assert buzz.value == 'Buzz Value'
    assert buzz.value_from_settings == 'Buzz from settings file'
```
