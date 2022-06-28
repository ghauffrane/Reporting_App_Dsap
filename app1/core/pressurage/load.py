import pandas as pd
import sys
import os
thisDir = os.getcwd()
sys.path.append(thisDir)

from pathlib import Path
path = Path(thisDir)
sys.path.append(str(path.parent.absolute()))

class LoadData:
    def __init__(self) -> None:
        self.columns = []
        self.status_indices = []
        self.orig_variables = ["4300 Analog values - Inside membrane pressure", 
                        "16014 Computation values - press net weight", 
                        "16016 Computation values - sliding average of press net weight", 
                        "16026 Computation values - extracted must quantity", 
                        "16028 Computation values - loaded product quantity", 
                        "16034 Computation values - must extraction percentage"]
        self.existing_variables = []


    def load_dt(self, data_path):
        if data_path.endswith('.csv'): 
            data = pd.read_csv(data_path, sep = ";", decimal = ",", low_memory=False)
        elif data_path.endswith('.xlsx'): 
            data = pd.read_excel(data_path)
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

    def check_variables(self):

        for vr in self.orig_variables: 
            if vr in self.columns:
                self.existing_variables.append(vr)

        return self.existing_variables      