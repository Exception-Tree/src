from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, Literal

from report.common.report_appendix_common import ReportAppendixCommon
from report.common.report_image_common import ReportImageCommon
from report.common.report_text_common import ReportTextCommon
from report.common.report_title_common import ReportTitleCommon


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
    def generate_latex(self, out_path: Path = None, remote: bool = False):
        raise NotImplementedError
