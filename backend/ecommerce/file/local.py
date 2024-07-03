# Base libraries
import os
from pathlib import Path
from typing import Iterable
# external libraries
import aiofiles
import aiofiles.os

# internal libraries

class LocalStorage:
    def __init__(self, directory: str):
        # Check if directory exists, if not, create it
        self.local_dir = Path(directory)
        self.local_dir.mkdir(parents=True, exist_ok=True)

    async def upload(self, file_stream:bytes, name: str):
        """Takes file stream and saves it to local.
        Returns the absolute path of the saved file.
        """
        file_path = self.local_dir / name
        if file_path.exists():
            raise FileExistsError
        async with aiofiles.open(file_path, 'wb') as outfile:
            await outfile.write(file_stream)
        return os.path.abspath(file_path)

    async def download(self, name_list: Iterable[str]):
        """
        Iterates over name list, opens, and yield file content.
        """
        for name in name_list:
            file_path = self.local_dir / name
            if file_path.exists():
                async with aiofiles.open(file_path, 'rb') as infile:
                    yield await infile.read()
            else:
                yield None

    async def delete(self, name: str):
        """Deletes file, must be idempotent.
        """
        # file_path = self.local_dir / name
        file_path = Path(name)
        # check file_path is safe
        if str(file_path) != str(
            os.path.abspath(self.local_dir / os.path.basename(name))):
            raise ValueError(f'image not in {self.local_dir}.')
        print(f"deleting {file_path}")
        if file_path.exists():
            await aiofiles.os.remove(file_path)
        else:
            raise FileNotFoundError(f"{file_path} not found.")
