from report.common.report_list_common import ReportListCommon

class ReportConclusionG732(ReportListCommon):
    def __init__(self):
        super().__init__()

    def generate_latex(self, output_path, remote) -> str:
        ltx = ''
        ltx += '\\NirConclusion'
        ltx += super().generate_latex(output_path, remote)

        return ltx