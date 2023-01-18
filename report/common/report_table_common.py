import json
import pandas as pd

from report.common.report_item_common import ReportItemCommon


class ReportTableCommon(ReportItemCommon):
    def __init__(self, json_dict: dict, body: list = None, columns: list = None, align=None,
                 header: str = None, footer: str = None, format: list = None, landscape=False):
        self.__body = body if body else json_dict['body']
        self.__columns = columns if columns else json_dict['columns']
        self.__landscape = landscape
        self.__ref = None
        self.__title = header if header else json_dict['header']
        self.__footer = footer if footer else json_dict['footer']
        self.__format = format if format else json_dict['format']
        try:
            self.align = align if align else json_dict['align']
        except Exception as e:
            self.align = ["l"] * self.col_amount

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, val):
        if val:
            self.__title = val

    @property
    def col_amount(self):
        return len(self.__columns)

    @property
    def data_frame(self):
        return pd.DataFrame(self.__body, columns=self.__columns)

    @property
    def align(self):
        return self.__align

    @align.setter
    def align(self, values):
        #if not all([x in ('r', 'l', 'c') for x in set(values)]):
        #    raise Exception(f'Wrong align format (it should be `r` or `l` or `c`): {values}')
        if len(values) == 1:
            values = values * self.col_amount
        if self.col_amount != len(values):
            raise Exception(f'number of column({self.col_amount}) not equ number of align({len(values)})')
        self.__align = f'|{"|".join(values)}|'

    @property
    def reference(self):
        return self.__ref

    @reference.setter
    def reference(self, val):
        self.__ref = val

    def set_wide_body_align(self, max_width=70, one_letter=2.05):
        df = self.data_frame

        salt = "d12dj0fjf38f2d12ds"
        indicies_list = {}
        for i, col in enumerate(df.columns):
            indicies_list[f'{col}{salt}_{i}'] = i
            df[f'{col}{salt}_{i}'] = df.iloc[:, i].apply(lambda x: len(f'{x}'))
            if df[f'{col}{salt}_{i}'].max() < len(col):
                df[f'{col}{salt}_{i}'] = len(col)
        df_len = df[list(indicies_list.keys())]

        #print(df_len.max())
        #print(len(self.data_frame.columns.max()))
        total_width = df_len.max().sum()
        #print(f'{self.__title}:{total_width}, {max_width}')
        if total_width > max_width:
            max_col = df_len.max().where(df_len.max() == df_len.max().max()).dropna()
            max_col_title = max_col.index.to_list()[0]
            max_col_value = max_col.values[0]
            aligns = self.align.split('|')[1:-1]
            aligns[indicies_list[max_col_title]] = \
                f'p{{{round((max_col_value - (total_width - max_width)) * one_letter + 0.5, 1)}mm}}'
            self.align = aligns

    def generate_latex(self, output_path: str, remote: bool) -> str:
        ltx = ""
        if self.__landscape:
            ltx += '\\begin{landscape}\n'
            self.set_wide_body_align(max_width=100)
        else:
            self.set_wide_body_align()  # Проверяем, умещается ли весь текст на страницу.

        ltx += f'\\begin{{longtable}}{{{self.align}}}\n'
        if self.reference:
            ltx += f'\\caption{{{self.title}}} \\label{{tab:{self.reference}}}\\\\ \\hline\n'
        else:
            ltx += f'\\caption{{{self.title}}} \\\\ \\hline\n'
        if any(self.__columns):
            ltx += ' & '.join(self.__columns) + '\\\\\n\\hline\n'
            ltx += '\\endhead \n'
        if self.__footer:
            ltx += '\\\\ \\\\\n \multicolumn{%i}{l}{%s}\\\\\n' % (self.col_amount, self.__footer)
            ltx += '\\endfoot\n'

        for row in self.__body:
            if self.__format:
                ltx += ' & '.join(list(map(lambda x, f: f % x, row, self.__format))) + '\\\\\n\\hline '
            else:
                ltx += ' & '.join([f'{x}' for x in row]) + '\\\\\n\\hline '

        ltx += '\\end{longtable}\n'
        if self.__landscape:
            ltx += '\\end{landscape}\n'
        return ltx
