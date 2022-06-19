from report.common import ReportCommon
from report.common.report_title_common import ReportTitleCommon


class ReportTitleG2105(ReportTitleCommon):
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
        self.__agreedBy = []
        self.__designedBy = []
        self.__title = title
        self.__docName = doc_name
        # self.__signature = signature
        # self.__classCode = classCode

    def generate_latex(self):
        ltx = self.__auto_title_font_size()
        if self.__departament:
            ltx += fr'\\ESKDdepartment{{{self.__departament}}}\n'
        ltx += fr'\\ESKDcompany{{{self.__company}}}\n'
        ltx += fr'\\ESKDdocName{{{self.__docName}}}\n'
        # if len(self.__docName) > 10:
        #     ltx += fr'\\ESKDcolumnI{{\\ESKDfontII {self.__docName}}}\n'
        # self.ltx += fr'\\ESKDsignature{{{self.__signature}}}\n'
        # self.ltx += fr'\\ESKDtitle{{{self.__title}}}\n'
        # if self.__classCode:
        #     self.ltx += fr'\\ESKDclassCode{{{self.__classCode}}}\n'
        # if self.__approved:
        #     self.ltx += fr'\\ESKDtitleApprovedBy{{{self.approved[0]}}}{{{self.approved[1]}}}\n'
        #
        # for status, name in self.__agreedBy:
        #     self.ltx += rf'\\ESKDtitleAgreedBy{{{status}}}{{{name}}}\n'
        #
        # index = 0
        # for status, name in self.__designedBy:
        #     self.ltx += fr'\\ESKDtitleDesignedBy{{{status}}}{{{name}}}\n'
        #     if index > 5:
        #         self.ltx += fr'\\clearpage\n'
        #     index += 1
        return ltx

    def __auto_title_font_size(self):
        amount = max(len(self.agreed_by), len(self.designed_by))
        if amount > 11:
            return r'\\renewcommand{\\ESKDtitleFontVIII}{\\ESKDfontIII}'
        else:
            return r'\\renewcommand{\\ESKDtitleFontVIII}{\\ESKDfontII}'

    @property
    def company(self):
        return self.__company

    @company.setter
    def company(self, company):
        self.__company = company

    @property
    def approved(self):
        return self.__approved

    @property
    def agreed_by(self):
        return self.__agreedBy

    @property
    def designed_by(self):
        return self.__designedBy

    @property
    def max_signers(self):
        return max(self.agreed_by, self.designed_by)


class ReportG2105(ReportCommon):
    def generate_latex(self):
        ltx = f"\\documentclass[russian,utf8,oneside]"+"{eskdtext}"
        ltx += r"""
\usepackage[OT1]{fontenc}
\newcommand{\No}{\textnumero}
\usepackage[utf8]{inputenc}
\usepackage[russian]{babel}"""
        ltx += '\n'
        if 'title' in self.items:
            ltx += self.items['title'].generate_latex()
        ltx += "\n\\begin{document}\\maketitle\\tableofcontents"
        #if ReportTitleG105 in super().__items:
        #    ltx =
        ltx += "\\end{document}"
        return ltx
