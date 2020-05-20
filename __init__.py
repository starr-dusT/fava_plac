from fava.ext import FavaExtensionBase
from beancount.core.number import Decimal, D
from .modules.beancount_plac import beancount_plac

class Plac(FavaExtensionBase):
    '''
    '''
    report_title = "Plac Budget"

    def table(self):
        budget = beancount_plac(self.ledger.entries, self.ledger.options)
        self.plac_df = budget.plac_tables() 
        types = []
        types.append(("Account", str(str)))
        types.append(("Budget", str(Decimal)))
        types.append(("Actual", str(Decimal)))
        types.append(("Difference", str(Decimal)))
        
        table = []
        for index, e_row in self.plac_df.iterrows():
            row = {}
            row["Account"] = e_row["Account"]
            row["Budget"] = e_row["Budget"]
            row["Actual"] = e_row["Actual"]
            row["Difference"] = e_row["Difference"]
            table.append(row)
        return types, table

