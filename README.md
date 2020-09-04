![Build Status](https://github.com/VaultVulp/dypendence/workflows/Main/badge.svg)
![Coverage Badge](https://minio.vaultvulp.dev/coverage/VaultVulp/dypendence/coverage.svg)

# Dypendence

Dependency Injection over Dynaconf

## Usage example

Example `settings.toml`

```toml
[DY.FileStorageService]
Type = "S3FileStorage"

[DY.FileStorageService.LocalFileStorage]
some_value = "This is Local File Storage"

[DY.FileStorageService.S3FileStorage]
some_value = "This is S3 File Storage"
```

Example application code:

```python
from dypendence import DY


class FileStorageService(DY):

    def save_file(self) -> str:
        raise NotImplementedError
    
    def get_value_from_settings(self):
        return self.settings.some_value


class LocalFileStorage(FileStorageService):

    def save_file(self) -> str:
        return 'Saved file to local file system'


class S3FileStorage(FileStorageService):

    def save_file(self) -> str:
        return 'Saved file to S3-like storage'


if __name__ == '__main__':
    file_storage = FileStorageService(settings_files=['settings.toml'])

    assert isinstance(file_storage, S3FileStorage)
    assert file_storage.save_file() == 'Saved file to S3-like storage'
    assert file_storage.get_value_from_settings() == 'This is S3 File Storage'
```
