from pathlib import Path
from typing import Union, Literal

from report.common.report_item_common import ReportItemCommon


class ReportImageCommonParam:
    def __init__(self, width: Union[float, str], height: Union[float, str],
                 position_on_page: Literal['top', 'bottom', 'center', 'here'] = 'center', landscape: Literal['None', 'page', 'picture', 'both'] = 'None'):
        self.__width = self.__size(width)
        self.__height = self.__size(height)
        self.__position = position_on_page
        self.__landscape = landscape

    @staticmethod
    def __size(param):
        size_types = {'full_width': '\\linewidth',
                      'full_height': '\\textheight',
                      'auto': None}
        if isinstance(param, float) or isinstance(param, int):
            return param
        else:
            if param in size_types:
                return size_types[param]
        raise Exception(f'unknown param = {param}')

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def position(self):
        return self.__position

    @property
    def landscape(self):
        return self.__landscape


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
        ltx = ''
        if self.__param.landscape == 'both' or self.__param.landscape == 'page':
            ltx += '\\begin{landscape}'
        ltx += '\\begin{figure}'
        if self.__param and self.__param.position != 'center':
            if self.__param.position == 'top':
                ltx += '[t]'
            elif self.__param.position == 'bottom':
                ltx += '[b]'
            elif self.__param.position == 'here':
                ltx += '[H]'

        if self.__param and self.__param.position == 'center':
            ltx += '\\centering'

        angle = 0
        if self.__param.landscape == 'picture' or self.__param.landscape == 'both':
            angle = 90
        if self.__param and self.__param.width is not None and self.__param.height is not None:
            ltx += f'\\includegraphics[angle={angle},width={self.__param.width},height={self.__param.height}]'
            ltx += '{'
        else:
            ltx += f'\\includegraphics[angle={angle}]'
            ltx += '{'
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

        if self.__param.landscape == 'both' or self.__param.landscape == 'page':
            ltx += '\\end{landscape}'
        return ltx
