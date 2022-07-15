import pandas as pd
import numpy as np
from datetime import datetime
import json


class SIS:

    def __init__(self) -> None:

        with open("./core/SIS/sis_metadata.json", "r") as f: 
            self.metadata = json.loads(f.read())
        self.last_matrix = self.get_last_matrix()
        
        
    
    def get_sys_matrix(self, fin_df, df, ddf):
        
        update_status = False
        if fin_df ==0: 
            fin_df +=1
        self.Class = self.last_matrix.copy()  
        for i in range(fin_df):
            
            rslt = ddf.loc[ddf['NP'] == i+1]
            rslt1 = df.loc[(df['Phase3'] == 1) & (df['NP'] == i+1)]
            RR1 = rslt1.RR[0:9].mean()
            if RR1 < 1.220472517 : 
                Classe = 0
            elif RR1 <  1.544326425 :
                Classe = 1
            else :
                Classe = 2
            XX = rslt.DM.quantile(0.2) # 20th percentile
            YY = rslt.DM.quantile(0.4) # 40th percentile
            ZZ = rslt.DM.quantile(0.6) # 60th percentile
            WW = rslt.DM.quantile(0.8) # 80th percentile
            ZLL = rslt.DDM.quantile(0.33) # 33rd percentile
            ZHH = rslt.DDM.quantile(0.66) # 66th percentile
            FLL = rslt.DFlux.quantile(0.33) # 33rd percentile
            FHH = rslt.DFlux.quantile(0.66) # 66th percentile
            if ((rslt.RR.max()-rslt.RR.min()) > 1) :# & (Density>=1.05)) : # In case of good press, and conform density update Classe's parameters and increment counter
                self.Class['X'][Classe] = (self.Class['Cpt'][Classe] * self.Class['X'][Classe] + XX)/ (self.Class['Cpt'][Classe] + 1)
                self.Class['Y'][Classe] = (self.Class['Cpt'][Classe] * self.Class['Y'][Classe] + YY)/ (self.Class['Cpt'][Classe] + 1)
                self.Class['Z'][Classe] = (self.Class['Cpt'][Classe] * self.Class['Z'][Classe] + ZZ)/ (self.Class['Cpt'][Classe] + 1)
                self.Class['W'][Classe] = (self.Class['Cpt'][Classe] * self.Class['W'][Classe] + WW)/ (self.Class['Cpt'][Classe] + 1)
                self.Class['ZL'][Classe] = (self.Class['Cpt'][Classe] * self.Class['ZL'][Classe] + ZLL)/ (self.Class['Cpt'][Classe] + 1)
                self.Class['ZH'][Classe] = (self.Class['Cpt'][Classe] * self.Class['ZH'][Classe] + ZHH)/ (self.Class['Cpt'][Classe] + 1)
                self.Class['FL'][Classe] = (self.Class['Cpt'][Classe] * self.Class['FL'][Classe] + FLL)/ (self.Class['Cpt'][Classe] + 1)
                self.Class['FH'][Classe] = (self.Class['Cpt'][Classe] * self.Class['FH'][Classe] + FHH)/ (self.Class['Cpt'][Classe] + 1)
                self.Class['Cpt'][Classe] = self.Class['Cpt'][Classe] + 1
                
        self.Class = self.Class.round(6)
        
        if np.array_equal(np.array(self.Class[["X", "Y" , "Z", "W", "ZL", "ZH", "FL", "FH"]]), np.array(self.last_matrix[["X", "Y" , "Z", "W", "ZL", "ZH", "FL", "FH"]])):
            update_status = False
            return self.last_matrix, update_status
        
        else: 
            update_status = True
            return self.Class, update_status



    def get_last_matrix(self):
  
        if len(self.metadata["matrix_history"]) == 0:
            last_matrix = pd.DataFrame(self.metadata["default_matrix"])

        elif len(self.metadata["matrix_history"])>= 1: 
            sorted_metadata_list = sorted(self.metadata["matrix_history"], key=lambda d: d['creation_time']) 
            last_meta = sorted_metadata_list[-1]
            last_matrix = pd.DataFrame(last_meta["update_matrix"])
        
        desired_cols = ["X", "Y" , "Z", "W", "ZL", "ZH", "FL", "FH", "Cpt"]
        last_matrix =last_matrix[desired_cols]
        return last_matrix


    def save_update_matrix(self, update_matrix, date: str, data_filepath): 

        update_matrix_metadata = {"creation_time": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "data_date": date,
            "data_filepath": data_filepath , "update_matrix": update_matrix.to_dict()}
        self.metadata["matrix_history"].append(update_matrix_metadata)

        with open("./core/SIS/sis_metadata.json", "w") as f: 
            json.dump(self.metadata, f)
       