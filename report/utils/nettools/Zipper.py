import os
import zipfile
from io import BytesIO
from pathlib import Path
from typing import List, Union


class Zipper(object):
    def __init__(self, out_file: str = ''):
        self.__in_memory: bool = False if out_file else True
        self.__zip_file: Union[str, BytesIO] = out_file if out_file else BytesIO()

    def add_files(self, files: List[Path]) -> None:
        with zipfile.ZipFile(self.__zip_file, mode="a", compression=zipfile.ZIP_DEFLATED) as zipf:
            for f in files:
                zipf.write(f, f.name)

    def add_folder(self, folder: Path) -> None:
        with zipfile.ZipFile(self.__zip_file, mode="a", compression=zipfile.ZIP_DEFLATED) as zipf:
            for dirname, subdirs, files in os.walk(folder.resolve()):
                for filename in files:
                    zipf.write(filename=str(Path(dirname) / filename),
                               arcname=str(Path(dirname).relative_to(folder.absolute()) / filename))

    @property
    def generated_zip(self) -> bytes:
        if self.__in_memory:
            return self.__zip_file.getvalue()
        else:
            with open(self.__zip_file, mode='rb') as binary_zip_file:
                return binary_zip_file.read()
