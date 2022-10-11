from report.common.report_list_common import ReportListCommon

class ReportReferatG732(ReportListCommon):
    def __init__(self):
        super().__init__()

    def generate_latex(self, output_path, remote) -> str:
        ltx = '\\NirReferat\n'
        ltx += super().generate_latex(output_path, remote)
        ltx+='\\newpage\n'

        return ltx
