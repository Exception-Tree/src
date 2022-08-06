import hashlib
import json
from _hashlib import HASH as Hash
from pathlib import Path
from typing import Union


class HashMaker(object):
    def __init__(self, path: Path, name: Path = 'src.hash'):
        self.__config = {}
        self.__filename = path / name
        try:
            with open(self.__filename) as json_file:
                self.__config = json.load(json_file)
        except FileNotFoundError:
            open(self.__filename, 'w')
        except Exception as e:  # TODO: Specify Exception
            print(e)

    def save(self):
        with open(self.__filename, mode='w') as json_file:
            json.dump(self.__config, json_file, indent=2)

    def md5_update_from_file(self, filename: Union[str, Path], hash: Hash) -> Hash:
        assert Path(filename).is_file()
        with open(str(filename), "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash.update(chunk)
        return hash

    def md5_file(self, filename: Union[str, Path]) -> str:
        return str(self.md5_update_from_file(filename, hashlib.md5()).hexdigest())

    def md5_update_from_dir(self, directory: Union[str, Path], hash: Hash) -> Hash:
        assert Path(directory).is_dir()
        for path in sorted(Path(directory).iterdir(), key=lambda p: str(p).lower()):
            hash.update(path.name.encode())
            if path.is_file():
                hash = self.md5_update_from_file(path, hash)
            elif path.is_dir():
                hash = self.md5_update_from_dir(path, hash)
        return hash

    def md5_dir(self, directory: Union[str, Path]) -> str:
        return str(self.md5_update_from_dir(directory, hashlib.md5()).hexdigest())

    def remove(self, name: Path):
        del self.__config[name.as_posix()]

    def calculate_file(self, name: Path):
        value = self.md5_file(name)
        self.__config[name.as_posix()] = value

    def compare_file(self, name: Path) -> bool:
        value = self.md5_file(name)
        try:
            return self.__config[name.as_posix()] == value
        except KeyError as e:
            print(e)
            self.__config[name.as_posix()] = value
        return False

    def compare_dir(self, name: Path) -> bool:
        value = self.md5_dir(name)
        try:
            return self.__config[name.as_posix()] == value
        except KeyError as e:
            print(e)
            self.__config[name.as_posix()] = value
        return False
