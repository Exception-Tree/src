from pathlib import Path
from typing import Union
from report.common.report_text_common import ReportTextCommon

class ReportSymbolsG732(ReportTextCommon):
    def __init__(self, value: Union[Path, str], template: str = None):
        super().__init__(value, template)

    def generate_latex(self, output_path, remote) -> str:
        ltx = ''
        ltx += '\\NirSymbol'
        ltx += super().generate_latex(output_path, remote)
        ltx+='\\newpage\n'

        return ltx