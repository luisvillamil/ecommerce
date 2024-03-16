# Base libraries
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
        return str(file_path)

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
        file_path = self.local_dir / name
        if file_path.exists():
            await aiofiles.os.remove(file_path)
