from report.common.report_item_common import ReportItemCommon
from report.common.report_list_common import ReportListCommon


class ReportAppendixCommon(ReportListCommon):
    def __init__(self, caption: str, reference: str):
        super().__init__()
        self.__caption = caption
        self.__reference = reference

    @property
    def caption(self):
        return self.__caption

    @property
    def reference(self):
        return self.__reference

    def generate_latex(self, output_path: str = None, remote: bool = False) -> str:
        ltx = '\\appendix{'
        ltx += f'{self.__caption}'
        ltx += f'\\label{{sec:{self.__reference}}}}}\n'
        ltx += super().generate_latex(output_path, remote)
        return ltx
