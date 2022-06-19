from report import SimpleReportCreator
from report.g2_105.report_g2_105 import ReportG2105, ReportTitleG2105

report = ReportG2105()
report.append(ReportTitleG2105('test', 'some'))
src = SimpleReportCreator(report)
src.generate_pdf(remote=False)
