from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, Literal

from report.common.report_image_common import ReportImageCommon
from report.common.report_item_common import ReportItemCommon
from report.common.report_title_common import ReportTitleCommon
from report.utils.greek import greek_replace


class ReportTextCommon(ReportItemCommon):
    def __init__(self, filename: Path, template=None, landscape=False,
                 font_size: Literal['small', 'normal', 'large'] = 'normal'):
        self.__body = ''
        self.__landscape = landscape
        self.__font_size = font_size
        self.__ext = filename.suffix
        if template:
            filename = self.__find_and_replace(filename, template)

        if self.__ext == '.tex':
            self.__parse_tex(filename.as_posix())
        elif self.__ext == '.md':
            raise NotImplementedError
        elif self.__ext == '.txt':
            raise NotImplementedError
        else:
            raise NotImplementedError

    def generate_latex(self):
        ltx = self.__latex_fontsize if self.__font_size != 'normal' else ''
        ltx += '\\begin{landscape}' if self.__landscape else ''
        ltx += self.__body
        ltx += '\\end{landscape}' if self.__landscape else ''
        return ltx

    @property
    def __latex_fontsize(self):
        sizes = {
            'small': '\\scriptsize',
            'normal': '\\normalsize',
            'large': '\\large',
        }
        return sizes[self.__font_size]

    def __find_and_replace(self, filename: Path, template) -> Path:
        with filename.open('r', encoding='utf8') as f:
            lines = ''
            for line in f:
                line = greek_replace(line)
                for fr, to in template:
                    to = to.replace('_', '\\_')
                    line = line.replace(fr, to)
                lines += line
        replaced_file = filename.parent / f'{filename.stem}_copy{filename.suffix}'
        with replaced_file.open('w', encoding='utf8') as f:
            f.write(lines)
        return replaced_file

    def __parse_tex(self, filename: str):
        self.__body = '\\subfile{'
        self.__body += f'{filename}'
        self.__body += '}\n'


class ReportAppendixCommon(ABC):
    pass


class ReportCommon(ABC):
    def __init__(self):
        self.__items = {'title': None, 'items': []}

    @property
    def all_items(self):
        return self.__items

    def append(self, item: Union[ReportTitleCommon, ReportImageCommon,
                                 ReportTextCommon, ReportAppendixCommon]):
        if isinstance(item, ReportTitleCommon):
            self.__items['title'] = item
        else:
            self.__items['items'].append(item)

    @property
    def title(self):
        return self.__items['title']

    @property
    def items(self):
        return self.__items['items']

    @abstractmethod
    def generate_latex(self, remote=False):
        raise NotImplementedError
