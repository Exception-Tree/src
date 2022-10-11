from report.common.report_appendix_common import ReportAppendixCommon


class ReportAppendixG732(ReportAppendixCommon):
    def __init__(self, caption: str, reference: str):
        super().__init__(caption, reference)

    def generate_latex(self, output_path: str = None, remote: bool = False) -> str:
        ltx = '\\appendix{'
        ltx += f'{self.caption}'
        ltx += f'\\label{{sec:{self.reference}}}}}'
        #ltx+='{обязательное}\n'
        ltx += '{обязательное}\n'
        return ltx
