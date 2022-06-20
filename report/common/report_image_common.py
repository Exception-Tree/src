from pathlib import Path

from report.common.report_item_common import ReportItemCommon


class ReportImageCommon(ReportItemCommon):
    def __init__(self, filename: Path, caption: str, reference: str):
        self.__filename = filename
        self.__caption = caption
        self.__reference = reference

    def generate_latex(self) -> str:
        ltx = '\\begin{figure}\n'
        ltx += '\\centering'
        ltx += '\\includegraphics[width=\\linewidth,height=\\textheight]{'
        ltx += f'{self.__filename.as_posix()}'
        ltx += '}'
        # self.ltx+='\\href{http://commons.wikimedia.org/wiki/File:Pachydyptes_ponderosus.jpg}'
        # self.ltx+='{\\includegraphics[width=\\textwidth]{'
        # self.ltx+=f'{self.image}'
        # self.ltx+='}}'
        ltx += '\\caption{'
        ltx += f'{self.__caption}'
        ltx += '}'
        ltx += f'\\label{{img:{self.__reference}}}\\\\'
        ltx += '\\end{figure}\n'
        return ltx
