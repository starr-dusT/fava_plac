import datetime
import collections
import logging
import pandas as pd
import numpy as np
import re

from beancount.core.number import Decimal
from beancount.core import data
from beancount.core import prices
from beancount.core import convert
from beancount.core import inventory
from beancount.core import account_types
from beancount.query import query
from beancount.core.data import Custom
from beancount.parser import options

class beancount_plac:

    def __init__(self, entries, options_map):
        column_names = ["Account", "Budget", "Actual", "Difference"]
        self.plac_df = pd.DataFrame(columns=column_names)
        
        self.entries = entries
        self.options_map = options_map
        
        self.start_date,self.end_date = self.find_plac_settings()  
        self.accounts, self.budgets = self.find_plac_budgets()
        self.actuals = self.find_plac_actuals()

    def plac_tables(self):
        for index in range(len(self.accounts)):
            row = {"Account" : self.accounts[index], "Budget" : self.budgets[index], "Actual" : self.actuals[index], "Difference" : self.budgets[index]-self.actuals[index]}
            self.plac_df = self.plac_df.append(row, ignore_index=True)
        return self.plac_df

    def find_plac_settings(self):
        start_date = None
        end_date = None
        mappings = []
        for e in self.entries:
            if isinstance(e, Custom) and e.type == "plac":
                if e.values[0].value == "start date":
                    start_date = e.values[1].value
                if e.values[0].value == "end date":
                    end_date = e.values[1].value
        return start_date, end_date

    def find_plac_budgets(self):
        accounts = []
        budgets = []
        for e in self.entries:
            if isinstance(e, Custom) and e.type == "plac":
                if e.values[0].value == "budget":
                    accounts.append(e.values[1].value)
                    budgets.append(e.values[2].value)
        return accounts, budgets

    def find_plac_actuals(self):
        actuals = []
        for account in self.accounts:
            query_str = "select COST(SUM(position)) where account ~ \'" + str(account) + "\' and date >= " + str(self.start_date) + " and date <= " + str(self.end_date) + ";"
            query_temp = query.run_query(self.entries, self.options_map, query_str, numberify=True)
            actuals.append(query_temp[1][0][0])
        return actuals
