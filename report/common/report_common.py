from abc import ABC, abstractmethod
from pathlib import Path

from report.common.report_image_common import ReportImageCommon
from report.common.report_item_common import ReportItemCommon



class ReportCommon(ABC):

    @abstractmethod
    def append(self, item: ReportItemCommon):
        raise NotImplementedError

    @abstractmethod
    def generate_latex(self, out_path: Path, remote: bool):
        raise NotImplementedError
