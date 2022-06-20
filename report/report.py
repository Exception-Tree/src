from pathlib import Path

from report.common import ReportCommon
from report.utils.localtools import LocalTools
from report.utils.nettools import NetTools


class SimpleReportCreator(object):
    def __init__(self, report_common: ReportCommon):
        self.__report = report_common

    def generate_latex(self, name: str = 'report', out_path: Path = None, remote: bool = False):
        ltx = self.__report.generate_latex(out_path, remote)
        if out_path:
            filename = f'{out_path.as_posix()}/{name}.tex'
        else:
            filename = f'{name}.tex'
        with open(filename, 'w', encoding='utf8') as f:
            f.write(ltx)
        return filename

    def generate_pdf(self, name: str = 'report', out_path: Path = None, remote=False):
        fname = self.generate_latex(name, out_path, remote)

        if remote:
            NetTools.tex2pdf(fname, output_directory=out_path)#, folder_map=folder_map)
        else:
            LocalTools.tex2pdf(fname, output_directory=out_path)
