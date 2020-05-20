import re
from datetime import date
import pandas as pd
from fava.ext import FavaExtensionBase


class Plac(FavaExtensionBase):  # pragma: no cover
    
    report_title = 'lel'
    
    def get_month(self):
        self.month = date.today().year

    def table(self):
        table_types = []
        table_types.append(('col1', str(int)))
        table_types.append(('col2', str(int)))
       
        df = pd.DataFrame({'col1': [1,2],
                           'col2': [4,5.66]})
        table = []
        for index, e_row in df.iterrows():
            row = {}
            row['col1'] = e_row['col1']
            row['col2'] = e_row['col2']
            table.append(row)
        return (table_types, table)
