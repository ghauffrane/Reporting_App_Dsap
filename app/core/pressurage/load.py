from pkgutil import ImpImporter
from unicodedata import decimal
import pandas as pd
import sys
import os
thisDir = os.getcwd()
sys.path.append(thisDir)

from pathlib import Path
path = Path(thisDir)
sys.path.append(str(path.parent.absolute()))

class FileUnsupported(Exception): 
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

class LoadData:
    def __init__(self) -> None:
        self.columns = []
        self.status_indices = []

    def load_dt(self, data_path):

        if data_path.endswith('.csv'): 
            data = pd.read_csv(data_path, sep = ";", decimal = ",", low_memory=False)
            self.columns = list(data.columns)
            return data
            
        elif data_path.endswith('.xlsx'): 
            data = pd.read_excel(data_path, decimal = ".")
            self.columns = list(data.columns)
            return data

        

    def get_status_columns(self):
        
        filling_status_idx = self.columns.index("1521.2 Filling cycle running status  (Pause = 0)")
        dewater_status_idx = self.columns.index("1531.2 Dewatering cycle running status  (Pause = 0)")
        press_status_idx = self.columns.index("1541.2 Pressing  cycle running status  (Pause = 0)")
        dry_status_idx = self.columns.index("1551.2 Drying cycle running status  (Pause = 0)")

        self.status_indices = [filling_status_idx, dewater_status_idx, press_status_idx, dry_status_idx]

        filling_status = self.columns[filling_status_idx]
        dewater_status = self.columns[dewater_status_idx]
        press_status = self.columns[press_status_idx]
        dry_status = self.columns[dry_status_idx]
        
        return filling_status, dewater_status, press_status, dry_status

    def preprocess(self, DF): 
        
        DF.fillna(0, inplace = True)

        for col in self.existing_variables: 
            DF[col] = pd.to_numeric(DF[col], errors = 'coerce')

        return DF

    def check_variables(self, colnames2check: list):
        existing_variables = []
        NotFoundColumns = []
        for vr in colnames2check: 
            if vr in self.columns:
                existing_variables.append(vr)
            else:
                NotFoundColumns.append(vr) 

        return existing_variables, NotFoundColumns   