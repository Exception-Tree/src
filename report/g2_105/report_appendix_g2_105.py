from report.common.report_appendix_common import ReportAppendixCommon


class ReportAppendixG2105(ReportAppendixCommon):
    def __init__(self, caption: str, reference: str):
        super().__init__(caption, reference)

    def generate_latex(self, output_path: str = None, remote: bool = False) -> str:
        ltx = '\\ESKDappendix{обязательное}{'
        ltx += f'{self.caption}'
        ltx += f'\\label{{sec:{self.reference}}}}}\n'
        return ltx
