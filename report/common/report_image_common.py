from pathlib import Path
from typing import Union

from report.common.report_item_common import ReportItemCommon


class ReportImageCommonParam:
    def __init__(self, width: Union[float, str], height: Union[float, str]):
        size_types = {'full_width': '\\linewidth',
                      'full_height': '\\textheight'}
        if isinstance(width, float):
            self.__width = width
        else:
            if width in size_types:
                self.__width = size_types[width]
            else:
                raise Exception(f'unknown width = {width}')
        self.__height = height

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height


class ReportImageCommon(ReportItemCommon):
    def __init__(self, filename: Path, caption: str, reference: str,
                 param: ReportImageCommonParam = None):
        self.__filename = filename
        self.__caption = caption
        self.__reference = reference
        self.__param = param

    def generate_latex(self, remote) -> str:
        ltx = '\\begin{figure}\n'
        ltx += '\\centering'
        if self.__param:
            ltx += f'\\includegraphics[width={self.__param.width},height={self.__param.width}]'
            ltx += '{'
        else:
            ltx += '\\includegraphics{'
        ltx += f'{self.__filename.as_posix()}'
        ltx += '}'
        # self.ltx+='\\href{http://commons.wikimedia.org/wiki/File:Pachydyptes_ponderosus.jpg}'
        # self.ltx+='{\\includegraphics[width=\\textwidth]{'
        # self.ltx+=f'{self.image}'
        # self.ltx+='}}'
        ltx += '\\caption{'
        ltx += f'{self.__caption}'
        ltx += '}\n'
        ltx += f'\\label{{img:{self.__reference}}}\n'
        ltx += '\\end{figure}\n'
        return ltx
