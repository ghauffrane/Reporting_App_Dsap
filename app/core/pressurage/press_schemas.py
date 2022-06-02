from dataclasses import dataclass

@dataclass
class DataSession:
    pdf_charts_filenames = set
    chosen_file_path : str = None
    dataframe = None
    existing_vars: list = None
    dir_path_excel: str = None
    dir_path_pdf: str = None
    ordered_cycles_indices : str = None
    update_current_chart_path : str = None
    

