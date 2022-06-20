import os
import shutil
import subprocess
from pathlib import Path

import requests

from mputils.nettools.Zipper import Zipper


class LocalTools(object):

    def __init__(self, *, output_directory=''):
        self.__output_directory = output_directory
        pass

    @classmethod
    def check_pandoc(cls) -> bool:
        try:
            p = subprocess.Popen(['pandoc', '-v'])
            p.wait()

            return True
        except FileNotFoundError as err:
            return False

    @classmethod
    def tex2pdf(cls, tex_file: str, folder_map=None, output_directory: str = None):
        """
        :param output_directory:
        :param extrn_folder:
        :param tex_file: Исходный tex-файл
        :param folder_map: Путь к папке с картинками
        :return:
        """
        iterations = 3
        silent = False

        path = os.path.abspath(tex_file)
        path = os.path.dirname(path)
        for i in range(iterations):
            if tex_file:
                try:
                    if os.path.dirname(tex_file):
                        p = subprocess.Popen(['pdflatex.exe', '-draftmode', '-interaction=nonstopmode',
                                              f'-output-directory={path}', os.path.abspath(tex_file)])
                        p.wait()
                    else:
                        p = subprocess.Popen(['pdflatex.exe', '-draftmode', '-interaction=nonstopmode',
                                              f'-output-directory={path}', tex_file])
                        p.wait()
                        #p = subprocess.Popen(['bibtex.exe', f'-output-directory={path}', tex_file])
                        #p = subprocess.Popen(['bibtex.exe', f'{Path(tex_file).stem}.aux'])
                        #p.wait()
                        p = subprocess.Popen(
                            ['makeindex.exe', f'-output-directory={path}', f'{Path(tex_file).stem}.idx'])
                            #['makeindex.exe'])
                        p.wait()
                        p = subprocess.Popen(
                            ['makeindex.exe', '-s', f'-output-directory={path}', tex_file])
                        p.wait()
                        p = subprocess.Popen(['pdflatex.exe', '-draftmode', '-interaction=nonstopmode',
                                              f'-output-directory={path}', tex_file])
                        p.wait()
                        p = subprocess.Popen(['pdflatex.exe', '-interaction=nonstopmode', tex_file])
                        p.wait()

                except IOError:
                    raise Exception(
                        "Невозвожно открыть файл '%s' для записи. Возможно, он открыт в другой программе." % tex_file)
        p = subprocess.Popen(
            ['pdflatex.exe', '-interaction=nonstopmode', f'-output-directory={path}', os.path.abspath(tex_file)])
        p.wait()
        if silent:
            shutil.move(tex_file, "%s/tex/%s" % (os.path.dirname(tex_file), os.path.basename(tex_file)))
            os.remove('%saux' % tex_file[:-3])
            os.remove('%slog' % tex_file[:-3])

    @classmethod
    def md2tex(cls, md_file: Path, output_directory: str = None) -> Path:
        md_file = Path(md_file)
        if not output_directory:
            output_directory = md_file.parent
        else:
            output_directory = Path(output_directory)

        # response = requests.post(f'{cls.PROCESSING_SERVER}:{cls.PROCESSING_PORT}/md_to_tex', files=files)
        result_file = output_directory / f'{md_file.stem}.tex'
        # pandoc --from markdown_strict+pipe_tables+multiline_tables+simple_tables+grid_tables+table_captions main.md --to latex -o main-test2.tex
        p = subprocess.Popen(['pandoc', '--from', 'markdown_strict+pipe_tables+multiline_tables+simple_tables+grid_tables+table_captions+tex_math_dollars+raw_tex', '-o', result_file.absolute().as_posix(),
                              md_file.absolute().as_posix()])
        p.wait()
        return result_file
