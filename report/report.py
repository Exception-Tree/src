from abc import ABC, abstractmethod
from pathlib import Path

from report.common import ReportCommon
from report.utils.localtools import LocalTools
from report.utils.nettools import NetTools


class SimpleReportCreatorCallback(ABC):
    def __init__(self):
        self.__total = 0

    @property
    def total(self):
        return self.__total

    @total.setter
    def total(self, value):
        self.__total = value

    @abstractmethod
    def progress(self, caption: str, position: int):
        raise NotImplementedError

    @abstractmethod
    def warning(self, text: str) -> bool:
        """
        Get warning message from SRC
        :param text:
        :return: True if you need stop process
        """
        raise NotImplementedError

    @abstractmethod
    def error(self, text: str) -> bool:
        """
        Get error message from SRC
        :param text:
        :return: True if you need stop process
        """
        raise NotImplementedError

    @abstractmethod
    def message(self, text: str):
        """
        Get message from SRC
        :param text:
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def exception(self, ex: Exception) -> bool:
        """
        Get exception from SRC
        :param ex:
        :return: True if you need stop process
        """
        raise NotImplementedError


class SimpleReportCreator(object):
    def __init__(self, report_common: ReportCommon, callback: SimpleReportCreatorCallback):
        self.__report = report_common
        self.__callback = callback

    @property
    def report(self):
        return self.__report

    @property
    def callback(self):
        return self.__callback

    def generate_latex(self, name: str = 'report', out_path: Path = None, remote: bool = False):
        ltx = self.__report.generate_latex(out_path, remote)
        if out_path:
            filename = f'{out_path.as_posix()}/{name}.tex'
        else:
            filename = f'{name}.tex'
        with open(filename, 'w', encoding='utf8') as f:
            f.write(ltx)
        return filename

    def generate_pdf(self, name: str = 'report', out_path: Path = None, remote=False):
        fname = self.generate_latex(name, out_path, remote)

        if remote:
            NetTools.tex2pdf(fname, output_directory=out_path)#, folder_map=folder_map)
        else:
            LocalTools.tex2pdf(fname, output_directory=out_path)
