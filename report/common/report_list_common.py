from report.common.report_item_common import ReportItemCommon


class ReportListCommon(ReportItemCommon):
    def __init__(self):
        self.items = []

    def generate_latex(self, output_path: str, remote: bool) -> str:
        ltx =''
        for item in self.items:
            ltx += item.generate_latex(output_path, remote)
        return ltx

    def append(self, item):
        self.items.append(item)
