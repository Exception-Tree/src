import re
from pathlib import Path

from report.common.report_image_common import ReportImageCommon
from report.common.report_item_common import ReportItemCommon
from report.utils.greek import greek_replace
from report.utils.localtools import LocalTools
from report.utils.nettools import NetTools


class ReportTextCommon(ReportItemCommon):
    def __init__(self, filename: Path, template: str = None):
        self.__filename = filename
        self.__template = template
        self.__items = []

    def append(self, item: ReportImageCommon):
        self.__items.append(item)

    def find_and_replace_ref(self, filename):
        with open(filename, 'r', encoding='utf8') as file:
            lines = ''
            for line in file:
                line = greek_replace(line)
                #line = line.replace('_', r'\_')
                line = re.sub('%(ref|label|cref)\(([^)]+)\)', r'\1{\2}', line)
                lines += line
        with open(filename, 'w', encoding='utf8') as file:
            file.write(lines)

    def __find_and_replace_item(self, filename, output_path, remote):
        with open(filename, 'r', encoding='utf8') as file:
            lines = ''
            for line in file:
                #line = re.sub('%(image)\(([^)]+)\)', r'\1{\2}', line)
                iter_items = re.finditer(r'\\%(image|table)\(([^)]+)\)', line)
                for match in iter_items:
                    ref = match[2]
                    for item in self.__items:
                        if item.reference == ref:
                            replace_text = item.generate_latex(output_path, remote)
                            line = line.replace(match[0], replace_text)
                lines += line
        with open(filename, 'w', encoding='utf8') as file:
            file.write(lines)

    def __find_and_replace(self, filename: Path, template) -> Path:
        with filename.open('r', encoding='utf8') as f:
            lines = ''
            for line in f:
                line = greek_replace(line)
                for fr, to in template:
                    to = to.replace('_', '\\_')
                    line = line.replace(fr, to)
                lines += line
        replaced_file = filename.parent / f'{filename.stem}_copy{filename.suffix}'
        with replaced_file.open('w', encoding='utf8') as f:
            f.write(lines)
        return replaced_file

    def generate_latex(self, output_path: Path, remote: bool) -> str:
        ltx = ''
        if self.__template:
            self.__filename = self.__find_and_replace(self.__filename, self.__template)

        if self.__filename.suffix == '.md':
            if remote:
                output_name = NetTools.md2tex(self.__filename, output_path)
                #output_name.relative_to(output_path)
            else:
                output_name = LocalTools.md2tex(self.__filename, output_path)

            if self.__items:
                self.__find_and_replace_item(output_name, output_path, remote)

            self.find_and_replace_ref(output_name)
            ltx += f'\\subfile{{{output_name}}}\n'
        elif self.__filename.suffix == '.tex':
            ltx += f'\\subfile{{{self.__filename}}}\n'
        else:
            raise Exception(f'unknown format:{self.__filename}')
        return ltx

# class ReportTextCommon(ReportItemCommon):
#     def __init__(self, filename: Path, template=None, landscape=False,
#                  font_size: Literal['small', 'normal', 'large'] = 'normal'):
#         self.__body = ''
#         self.__landscape = landscape
#         self.__font_size = font_size
#         self.__ext = filename.suffix
#         if template:
#             filename = self.__find_and_replace(filename, template)
#
#         if self.__ext == '.tex':
#             self.__parse_tex(filename.as_posix())
#         elif self.__ext == '.md':
#             raise NotImplementedError
#         elif self.__ext == '.txt':
#             raise NotImplementedError
#         else:
#             raise NotImplementedError
#
#     def generate_latex(self):
#         ltx = self.__latex_fontsize if self.__font_size != 'normal' else ''
#         ltx += '\\begin{landscape}' if self.__landscape else ''
#         ltx += self.__body
#         ltx += '\\end{landscape}' if self.__landscape else ''
#         return ltx
#
#     @property
#     def __latex_fontsize(self):
#         sizes = {
#             'small': '\\scriptsize',
#             'normal': '\\normalsize',
#             'large': '\\large',
#         }
#         return sizes[self.__font_size]
#
#     def __find_and_replace(self, filename: Path, template) -> Path:
#         with filename.open('r', encoding='utf8') as f:
#             lines = ''
#             for line in f:
#                 line = greek_replace(line)
#                 for fr, to in template:
#                     to = to.replace('_', '\\_')
#                     line = line.replace(fr, to)
#                 lines += line
#         replaced_file = filename.parent / f'{filename.stem}_copy{filename.suffix}'
#         with replaced_file.open('w', encoding='utf8') as f:
#             f.write(lines)
#         return replaced_file
#
#     def __parse_tex(self, filename: str):
#         self.__body = '\\subfile{'
#         self.__body += f'{filename}'
#         self.__body += '}\n'
