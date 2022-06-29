import pandas as pd
import numpy as np   

class SIS:

    def __init__(self) -> None:
        self.Class = pd.DataFrame({'X': [0.0, 0.0, 0.0],
                    'Y': [0.0, 0.0, 0.0],
                    'Z': [0.0, 0.0, 0.0],
                    'W': [0.0, 0.0, 0.0],
                    'ZL': [0.0, 0.0, 0.0],
                    'ZH': [0.0, 0.0, 0.0],
                    'FL': [0.0, 0.0, 0.0],
                    'FH': [0.0, 0.0, 0.0],
                     'Cpt': [0.0, 0.0, 0.0]})
    
    def get_sys_matrix(self, fin_df, df, ddf):
        
              
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
                update_costants = True

        return self.Class

    def get_clean_data(self):

        # return original dataframe
        # return start and end time of the whole press
        # return df selected by column names
        # handle non existing column names
        # rename df
        # filter rows for press==1
        # return ddf
        # return fin variable
        pass