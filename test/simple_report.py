from pathlib import Path

from report import SimpleReportCreator
from report.common.report_common import ReportImageCommon
from report.common.report_image_common import ReportImageCommonParam
from report.common.report_text_common import ReportTextCommon
from report.g2_105.report_g2_105 import ReportG2105, ReportTitleG2105

report = ReportG2105()
title = ReportTitleG2105(title='Test Title', doc_name='Doc Name')
title.approvedBy('director', 'Ivanov I.I.')
report.append(title)

param = ReportImageCommonParam('full_width', 50)
report.append(ReportImageCommon(Path('./tester.png'), 'test caption', 'test_ref', param))

report.append(ReportTextCommon(Path('./test.md')))

src = SimpleReportCreator(report)
src.generate_pdf(remote=False)
