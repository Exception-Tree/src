from report.common import ReportCommon
from report.common.report_title_common import ReportTitleCommon
from report.g7_32.report_referat_g7_32 import ReportReferatG732
from report.g7_32.report_terms_g7_32 import ReportTermsG732
from report.g7_32.report_symbols_g7_32 import ReportSymbolsG732
from report.g7_32.report_introduction_g7_32 import ReportIntroductionG732
from report.g7_32.report_conclusion_g7_32 import ReportConclusionG732
from report.g7_32.report_sources_g7_32 import ReportSourcesG732
from report.g7_32.report_appendix_g7_32 import ReportAppendixG732


class ReportTitleG732(ReportTitleCommon):
    def __init__(self, title: str, doc_name: str, departament=None, company=None):
        if departament:
            self.__departament = departament
        else:
            self.__departament = ''
        if company:
            self.__company = company
        else:
            self.__company = ''
        self.__approved = None
        self.__agreed = ''
        self.__manager = ('','')
        self.__designed = []
        self.__title = title
        self.__docName = doc_name

    @property
    def doc_name(self):
        return self.__docName

    @property
    def company(self):
        return self.__company

    @company.setter
    def company(self, company):
        self.__company = company.replace('\n', '\\\\\\')

    @property
    def departament(self):
        return self.__departament

    @property
    def approved(self):
        return self.__approved

    @property
    def agreed(self):
        return self.__agreed

    @property
    def designed(self):
        return self.__designed

    def departamenBy(self, name: str):
        self.__departament = name

    def companyBy(self, name: str):
        self.__company = name

    def approvedBy(self, status: str, name: str):
        self.__approved = [status, name]

    def agreedBy(self, status: str, name: str):
        self.__agreed = [status, name]

    def managerBy(self, status: str, name: str):
        self.__manager = [status, name]

    def designedBy(self, status: str, name: str, work: str):
        self.__designed.append([status, name, work])


    def generate_latex(self, out_path: str, remote: bool)->str:
        ltx = ""
        if (len(self.departament)!=0):
            ltx += fr'\NirTitleCompany{{\textsc{{{self.departament}}}{{{self.company}}}}}'
            ltx += '\n'
        ltx += fr'\NirTitleOrder{{{self.doc_name}}}{{}}{{}}'
        ltx += '\n'
        ltx += fr'\NirManager{{{self.__manager[0]}}}{{{self.__manager[1]}}}'
        ltx += '\n'
        if self.approved:
            ltx += fr'\NirTitleConfirm{{{self.approved[0]}}}{{{self.approved[1]}}}'
            ltx += '\n'
        if self.agreed:
            ltx += rf'\NirTitleAgreed{{{self.agreed[0]}}}{{{self.agreed[1]}}}'
            ltx += '\n'
        for status, name, work in self.designed:
            ltx += fr'\NirDesigner{{{status}}}{{{name}}}'
            ltx += '{('
            ltx += fr'{{{work}}}'
            ltx += ')}'
            ltx += '\n'
        return ltx



class ReportG732(ReportCommon):
    def __init__(self):
        self.__items = {'items': []}

    def append(self, item):
        if isinstance(item, ReportTitleG732) and 'title' not in self.__items:
            self.__items['title'] = item
        elif isinstance(item, ReportReferatG732) and 'referat' not in self.__items:
            self.__items['referat'] = item
        elif isinstance(item, ReportTermsG732) and 'terms' not in self.__items:
            self.__items['terms'] = item
        elif isinstance(item, ReportSymbolsG732) and 'symbols' not in self.__items:
            self.__items['symbols'] = item
        elif isinstance(item, ReportIntroductionG732) and 'introduction' not in self.__items:
            self.__items['introduction'] = item
        elif isinstance(item, ReportConclusionG732) and 'conclusion' not in self.__items:
            self.__items['conclusion'] = item
        elif isinstance(item, ReportSourcesG732) and 'sources' not in self.__items:
            self.__items['sources'] = item
        elif isinstance(item, ReportAppendixG732) and 'appendix' not in self.__items:
            self.__items['appendix'] = item


    def generate_latex(self, out_path: str, remote: bool) -> str:
        ltx = f"\\documentclass[12pt, a4, russian,utf8,oneside]"+"{G7-32}"

        ltx += r"""
\newcommand{\No}{\textnumero}
\usepackage[utf8]{inputenc}
\usepackage[russian]{babel}
\usepackage{subfiles}
\usepackage{hyperref}
\usepackage{cleveref}
\usepackage{graphicx,float}
\sloppy
\def\tightlist{}
"""
        ltx += '\n'
        if 'title' in self.__items:
            ltx += self.__items['title'].generate_latex(out_path, remote)
            ltx += '\n'
        ltx += "\n\\begin{document}\\maketitle\\makedesigner\n"
        if 'referat' in self.__items:
            ltx += self.__items['referat'].generate_latex(out_path, remote)
            ltx += '\n'
        ltx += '\\tableofcontents\\newpage\n'
        if 'terms' in self.__items:
            ltx += self.__items['terms'].generate_latex(out_path, remote)
            ltx += '\n'
            ltx += '\\newpage'
        if 'symbols' in self.__items:
            ltx += self.__items['symbols'].generate_latex(out_path, remote)
            ltx += '\n'
            ltx += '\\newpage'
        if 'introduction' in self.__items:
            ltx += self.__items['introduction'].generate_latex(out_path, remote)
            ltx += '\n'
        if 'conclusion' in self.__items:
            ltx += self.__items['conclusion'].generate_latex(out_path, remote)
            ltx += '\n'
        if 'sources' in self.__items:
            ltx += self.__items['sources'].generate_latex(out_path, remote)
            ltx += '\n'
            ltx += '\\newpage'
        if 'appendix' in self.__items:
            ltx += self.__items['appendix'].generate_latex(out_path, remote)
            ltx += '\n'

        for item in self.__items['items']:
            ltx += item.generate_latex(out_path, remote)
        ltx += "\\end{document}"
        return ltx
