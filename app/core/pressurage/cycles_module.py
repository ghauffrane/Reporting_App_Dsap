import pandas as pd
import sys
import os
thisDir = os.getcwd()
sys.path.append(thisDir)

from pathlib import Path
path = Path(thisDir)
sys.path.append(str(path.parent.absolute()))

class Cycles:
    def __init__(self, dataframe) -> None:
        self.dataframe = dataframe
    

    def separate_cycles(self, filling_status, press_status, dewater_status, dry_status):
        cycles_indices = []
        nbr_cycles = 0
        end_indices = []
        self.ordered_indices_cycles = []
        start = 0
        for row in range(len(self.dataframe)):
            if (int(self.dataframe.iloc[row][filling_status]) == 1) or (int(self.dataframe.iloc[row][press_status]) == 1) \
            or (int(self.dataframe.iloc[row][dewater_status]) == 1) or (int(self.dataframe.iloc[row][dry_status]) == 1):
                
                cycles_indices.append(row)

                if (len(cycles_indices)>1) and (row - cycles_indices[-2] > 1):
                    nbr_cycles += 1
                    end_indices.append(cycles_indices[-2])
                    self.ordered_indices_cycles.append(cycles_indices[start:-1])
                    start = cycles_indices.index(row)
        
        if len(self.ordered_indices_cycles) == 0 and len(cycles_indices)>0:
            nbr_cycles += 1
            self.ordered_indices_cycles.append(cycles_indices)
        
        self.nbr_cycles = nbr_cycles
        self.ordered_indices_cycles
        
        return self.ordered_indices_cycles, self.nbr_cycles
    
    def __getcycle__(self, cycle_nbr, ordered_indices_cycles):
        this_cycle_indices = ordered_indices_cycles[cycle_nbr]
        this_cycle_df = self.dataframe.iloc[this_cycle_indices, : ].reset_index()
        return this_cycle_df     