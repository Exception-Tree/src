from typing import Literal

from report.common.report_appendix_common import ReportAppendixCommon


class ReportAppendixG2105(ReportAppendixCommon):
    def __init__(self, type: Literal['обязательное','информационное'],  caption: str, reference: str):
        super().__init__(caption, reference)
        self.__type = type

    def generate_latex(self, output_path: str = None, remote: bool = False) -> str:
        ltx = f'\\ESKDappendix{{{self.__type}}}{{'
        ltx += f'{self.caption}'
        ltx += f'\\label{{sec:{self.reference}}}}}\n'
        ltx += super().generate_latex(output_path, remote)
        return ltx
