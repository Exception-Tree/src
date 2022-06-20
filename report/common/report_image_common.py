from pathlib import Path
from typing import Union, Literal

from report.common.report_item_common import ReportItemCommon


class ReportImageCommonParam:
    def __init__(self, width: Union[float, str], height: Union[float, str],
                 position_on_page: Literal['top', 'bottom', 'center', 'here'] = 'center'):
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

        self.__position = position_on_page

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def position(self):
        return self.__position


class ReportImageCommon(ReportItemCommon):
    def __init__(self, filename: Path, caption: str, reference: str,
                 param: ReportImageCommonParam = None):
        self.__filename = filename
        self.__caption = caption
        self.__reference = reference
        self.__param = param

    @property
    def reference(self):
        return self.__reference

    def generate_latex(self, output_path, remote) -> str:
        ltx = '\\begin{figure}'
        if self.__param and self.__param.position != 'center':
            if self.__param.position == 'top':
                ltx += '[t]'
            elif self.__param.position == 'bottom':
                ltx += '[b]'
            elif self.__param.position == 'here':
                ltx += '[H]'

        if self.__param and self.__param.position == 'center':
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
