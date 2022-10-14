from pathlib import Path

from report import SimpleReportCreator, SimpleReportCreatorCallback
from report.common.report_appendix_common import ReportAppendixCommon
from report.common.report_common import ReportImageCommon
from report.common.report_image_common import ReportImageCommonParam
from report.common.report_text_common import ReportTextCommon
from report.g2_105.report_appendix_g2_105 import ReportAppendixG2105
from report.g2_105.report_g2_105 import ReportG2105, ReportTitleG2105
from report.utils.hashmaker import HashMaker


class TestSRCCallback(SimpleReportCreatorCallback):
    def progress(self, caption: str, position: int):
        pass

    def warning(self, text: str) -> bool:
        print(text)
        return False

    def message(self, text: str):
        print(text)

    def error(self, text: str) -> bool:
        print(text)
        return False

    def exception(self, ex: Exception) -> bool:
        print(ex)
        return False


report = ReportG2105()
title = ReportTitleG2105(title='Test Title', doc_name='Doc Name')
title.approvedBy('director', 'Ivanov I.I.')
report.append(title)

text = ReportTextCommon(Path('./test.md'))
text.append(ReportImageCommon(Path('./horse.jpg'), 'test caption', 'horseref'))
report.append(text)

report.append(ReportImageCommon(Path('./horse.jpg'), 'test caption', 'testref1'))

appendix = ReportAppendixG2105('обязательное', 'test', 'ref')

param = ReportImageCommonParam('full_width', 50, position_on_page='here')
appendix.append(ReportImageCommon(Path('./tester.png'), 'test caption', 'apnd_testref', param))
report.append(appendix)

param = ReportImageCommonParam('full_width', 50)
report.append(ReportImageCommon(Path('./tester.png'), 'test caption', 'testref', param))

callback = TestSRCCallback()
src = SimpleReportCreator(report, callback)
src.generate_pdf(remote=False)
