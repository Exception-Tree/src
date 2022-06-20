from report.common.report_item_common import ReportItemCommon


class ReportAppendixCommon(ReportItemCommon):
    def __init__(self, caption: str, reference: str):
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
        return ltx
