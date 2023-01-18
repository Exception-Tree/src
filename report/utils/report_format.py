import json
import re
from pathlib import Path
from typing import Optional, Union, List

from pydantic import BaseModel, validator


class TableJSON(BaseModel):
    type: str = 'table'
    body: List
    header: str = ''
    footer: str = ''
    columns: List[str]
    align: str = ''
    format: List = []

    @validator("format", always=True)
    @classmethod
    def validate_format(cls, value, values):
        if not value:
            return ['%s' for _ in values['columns']]


class ReportFileFormat:
    """
    """
    def __init__(self):
        self.__footer = ''

    def from_csv(self, input_file: Path, skip: int = 0, sep: str = '\s+', with_column_names: bool = False,
                 footer: str = '', header: str = '', header_line_from_file: Union[int, List[int]] = -1,
                 format: Optional[str] = None, encoding='utf8', columns=None, output_file: Optional[Path] = None):
        """Convert CSV to our format"""
        self.__body = []
        if not output_file:
            output_file = input_file.parent / f'{input_file.name}.json'
        elif output_file.is_dir():
            output_file = output_file / f'{input_file.name}.json'
        try:
            with input_file.open('r', encoding=encoding) as inp_file:
                lines = inp_file.readlines()

                if header:
                    self.__header = header
                elif isinstance(header_line_from_file, int) and header_line_from_file > 0:
                    self.__header = lines[header_line_from_file]
                elif isinstance(header_line_from_file, list):
                    self.__header = lines[header_line_from_file[0]: header_line_from_file[1] + 1]
                lines = lines[skip:]

                if columns:
                    self.__columns = columns

                elif with_column_names:
                    self.__columns = re.split(sep, lines.pop(0).strip())

                for row in lines:
                    self.__body.append(re.split(sep, row.strip()))
        except Exception as e:
            #logger.error(f'Error while reading {input_file.absolute()}')
            raise e

        tj = TableJSON(body=self.__body, header=self.__header, footer=self.__footer, columns=self.__columns)
        with output_file.open('w', encoding='utf8') as wf:
            #json.dump([tj.dict()], wf, indent=2, ensure_ascii=False)
            json.dump(tj.dict(), wf, indent=2, ensure_ascii=False)
        return output_file
