from pathlib import Path

from report import SimpleReportCreator, SimpleReportCreatorCallback
from report.common.report_appendix_common import ReportAppendixCommon
from report.common.report_common import ReportImageCommon
from report.common.report_image_common import ReportImageCommonParam
from report.common.report_text_common import ReportTextCommon
from report.g7_32.report_appendix_g7_32 import ReportAppendixG732
from report.g7_32.report_referat_g7_32 import ReportReferatG732
from report.g7_32.report_terms_g7_32 import ReportTermsG732
from report.g7_32.report_symbols_g7_32 import ReportSymbolsG732
from report.g7_32.report_introduction_g7_32 import ReportIntroductionG732
from report.g7_32.report_conclusion_g7_32 import ReportConclusionG732
from report.g7_32.report_sources_g7_32 import ReportSourcesG732
from report.g7_32.report_g7_32 import ReportG732, ReportTitleG732
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

report = ReportG732()
title = ReportTitleG732(title='Test Title', doc_name='Doc Name')

_referat = ReportTextCommon(Path("./referat.md"))
referat = ReportReferatG732()
referat.append(_referat)

title.departamenBy('КОРПОРАЦИЯ «ABC»')
title.companyBy('\\\\  \\\\(АО «  »)')

title.agreedBy("Директор B", "М.М. Степанов")
title.approvedBy("Директор A", "И.И. Иванов")
title.managerBy("Директор C", "Д.Д. Романов")

title.designedBy('Инженер', 'Е.Е. Петров', 'все разделы')
title.designedBy('Старший научный сотрудник', 'К.С. Дмитриев', 'приложения A, B, C, D, E, R, T')
title.designedBy('Инженер-конструктор', 'П.П. Павлов', 'приложение G')

symbols = ReportSymbolsG732(Path('./ShortList.md'))
terms = ReportTermsG732(Path('./terms.md'))

_introduction = ReportTextCommon(Path('./introduction.md'))
introduction = ReportIntroductionG732()
introduction.append(_introduction)

#introduction.append(ReportImageCommon(Path('./horse.jpg'), 'test caption', 'horseref'))

_conclusion = ReportTextCommon(Path('./conclusion.md'))
conclusion = ReportConclusionG732()
conclusion.append(_conclusion)

sources = ReportSourcesG732(Path('./sources.md'))

report.append(terms)
report.append(conclusion)
report.append(title)
report.append(introduction)
report.append(sources)
report.append(referat)
report.append(symbols)

text = ReportTextCommon(Path('./test.md'))
text.append(ReportImageCommon(Path('./horse.jpg'), 'test caption', 'horseref'))
report.append(text)

report.append(ReportImageCommon(Path('./horse.jpg'), 'test caption', 'testref1'))

report.append(ReportAppendixG732('test', 'ref'))

param = ReportImageCommonParam('full_width', 50)
report.append(ReportImageCommon(Path('./tester.png'), 'test caption', 'testref', param))

callback = TestSRCCallback()
src = SimpleReportCreator(report, callback)
src.generate_pdf(remote=False)
