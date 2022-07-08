from dataclasses import dataclass
from pickle import NONE

@dataclass
class DataSession:
    pdf_charts_filenames = []
    required_variables = ["4300 Analog values - Inside membrane pressure", 
                        "16014 Computation values - press net weight", 
                        "16016 Computation values - sliding average of press net weight", 
                        "16026 Computation values - extracted must quantity", 
                        "16028 Computation values - loaded product quantity", 
                        "16034 Computation values - must extraction percentage"]
    chosen_file_path : str = None
    dataframe = None
    existing_vars: list = None
    NotFoundVars: list = None
    dir_path_excel: str = None
    dir_path_pdf: str = None
    ordered_cycles_indices : str = None
    update_current_chart_path : str = None

@dataclass
class SysDataSession: 
    fin: int = None
    chosen_file_path : str = None
    sys_dataframe = None
    sys_df = None
    sys_ddf = None
    ordered_cycles_indices: str = None
    existing_vars: list = None
    NotFoundVars: list = None
    required_variables = ["_id ", "ts ", "4300 Analog values - Inside membrane pressure", "1541.2 Pressing  cycle running status  (Pause = 0)", 
                "16018 Computation values - variation of sliding average of press net weight", "16020 Computation values - accelleration of sliding average of press net weight", 
                "16058 Computation vlaues - flow variation computation", "16046 Computation values - ratio between dewatered must liters and press net weight"]
    
    

