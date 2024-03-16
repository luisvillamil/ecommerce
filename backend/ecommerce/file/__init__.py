# Base libraries
import abc
from typing import Iterable
# external libraries

# internal libraries
from ecommerce.config import settings
from ecommerce.file.local import LocalStorage

def get_storage():
    if settings.FILE_BACKEND == "local":
        return LocalStorage(settings.FILE_DIRECTORY)
    raise NotImplementedError
