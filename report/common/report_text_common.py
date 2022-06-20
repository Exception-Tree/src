from pathlib import Path

from report.common.report_item_common import ReportItemCommon
from report.utils.localtools import LocalTools
from report.utils.nettools import NetTools


class ReportTextCommon(ReportItemCommon):
    def __init__(self, filename: Path):
        self.__filename = filename

    def generate_latex(self, remote) -> str:
        ltx = ''
        if self.__filename.suffix == '.md':
            if remote:
                output_name = NetTools.md2tex(self.__filename)
            else:
                output_name = LocalTools.md2tex(self.__filename)

            ltx += f'\\subfile{{{output_name}}}\n'
        return ltx
