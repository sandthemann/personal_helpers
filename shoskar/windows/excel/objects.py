from io import BytesIO
import re
import pyxlsb
import xlrd
import openpyxl

from shoskar.windows.excel.functions import *
from shoskar.utils.functions import filter_kwargs

class ExcelObj:
    """This object holds the excel file and it's associated information"""
    def __init__(self, path):
        self.excel_file = ExcelFileObj(path)
        self.current_sheet = None
        self.available_sheets = {}

    def open_sheet(self, sheet_name, raw = False, **kwargs):
        """Uses the generated excel object, sheet name, and kwargs to open and process sheet based data"""

        sheet_name = normalize_sheet_name(sheet_name)

        if sheet_name in self.available_sheets and (kwargs is None and raw is False):
            self.current_sheet = self.available_sheets[sheet_name]
            return self.current_sheet
        
        if self.excel_file.check_sheet(sheet_name):
            sheet_name = self.excel_file.get_sheet_name(sheet_name)
            sheet = ExcelSheetObj(self.excel_file, sheet_name, **kwargs)
            self.available_sheets[sheet_name] = sheet
            self.current_sheet = self.available_sheets[sheet_name]
            return self.current_sheet
        else:
            pass

    def read_sheet(self, sheet_name = None, **kwargs):
        """Uses the generated excel object, sheet name, and kwargs to read sheet based data"""

        sheet_name = normalize_sheet_name(sheet_name)
        
        if sheet_name is None:
            if self.current_sheet is None:
                return None
            else:
                return self.current_sheet.read()
        sheet_name = self.excel_file.get_sheet_name(sheet_name)
        if kwargs is not None:
            if self.excel_file.check_sheet(sheet_name):
                sheet = ExcelSheetObj(self.excel_file, sheet_name, **kwargs)
        else:
            sheet = self.available_sheets[sheet_name]

        return sheet.read()
    
    def edit_sheet(self, sheet_name = None):
        """Returns an existing sheet"""

        sheet_name = normalize_sheet_name(sheet_name)

        if sheet_name is None:
            if self.current_sheet is None:
                return None
            else:
                return self.current_sheet
            
        sheet_name = self.excel_file.get_sheet_name(sheet_name)

        return self.available_sheets[sheet_name]
    
    def close(self):
        self.excel_file.close()
        self.available_sheets = {}
        self.current_sheet = None


class ExcelFileObj:
    """This object holds the open Excel file reference"""
    def __init__(self, path):
        self.base_path = path
        self.file_name, self.file_dir = split_file_path(self.base_path)
        #engine is needed to be determined due to different xls* versions
        self.engine = self._determine_engine()

        try:
            #attempts to open the file into bytes so it is not held open by this process and rendered unusable if a bug terminates the run.
            with open(self.base_path, "rb") as file:
                excel_binary_data = file.read()
            self.excel_io = BytesIO(excel_binary_data)
            self.excel_file = pd.ExcelFile(self.excel_io, engine=self.engine)
            self._sheet_names  = self.excel_file.sheet_names 
            #sheet names are normalized because they are case insensitive, and reduces errors related to extra spaces etc.
            self._normalized_sheet_names = list(map(normalize_sheet_name,  self._sheet_names))
        except Exception as e:
            #these exceptions and try/except loops are strictly Alteryx based debugging and should not be used outside of an Alteryx use-case.
            raise KeyError(f"Error opening Excel file: {e}")

    def check_sheet(self, sheet_name):

        normalized_sheet_name = normalize_sheet_name(sheet_name)

        if normalized_sheet_name not in self._normalized_sheet_names:
            raise KeyError(f'Sheet name cannot find match in current excel file')
        
        return True
    
    def get_sheet_name(self, sheet_name):

        normalized_sheet_name = normalize_sheet_name(sheet_name)
        found_sheet_name = dict(zip(self._normalized_sheet_names, self._sheet_names))[normalized_sheet_name]
        return found_sheet_name
    
    
    def get_sheet_names(self, normalized = False):

        if self._failed_object == 1:
            return None
        
        if normalized == True:
            return self._normalized_sheet_names
        return self._sheet_names
    

    def close(self):

        if self._failed_object == 0:
            self.excel_file.close()
        
    def _determine_engine(self):

        engine_dict = {'xlsb' : 'pyxlsb',
                       'xls': 'xlrd'}
        
        file_type = os.path.splitext(self.base_path)[1].strip('.')

        if file_type in engine_dict:
            return engine_dict[file_type]
        
        return 'openpyxl'
    

class ExcelSheetObj:
    """This object holds the sheet references assocated with an ExcelFileObj"""
    def __init__(self, excel_file_object:ExcelFileObj, sheet_name, **kwargs):
        if not type(excel_file_object) == ExcelFileObj:
            raise ValueError('Parameter excel_file_object must be of type ExcelFileObj.')
        self.efo = excel_file_object
        self.kwargs = kwargs
        self.sheet_name = sheet_name
        self.normalized_sheet_name = normalize_sheet_name(sheet_name)
        self.starting_cols = []
        self.current_cols = []
        self.duplicate_cols = {}
        self.df = self._read().copy()
    
    def read(self):
        return self.df
    
    #FIND WAY TO SPECIFY THAT READ_EXCEL IS HAVING ISSUE WITH COLUMN INDEXES
    def _read(self):
        #pd.read_excel doesn't except all kwargs and ignore unused ones, so filtering them is required
        read_excel_kwargs = filter_kwargs(pd.read_excel, self.kwargs)

        # print(read_excel_kwargs)
        sheet_data = pd.read_excel(self.efo.excel_file, sheet_name = self.sheet_name, **read_excel_kwargs)

        #changes column headers from using default .\d+ setup to using _\d+ setup, and recognizes and logs duplicate headers
        sheet_data.columns = self._clean_incoming_headers(sheet_data.columns, **self.kwargs)
        sheet_data.columns = self._make_headers_unique(sheet_data.columns, sheet_name = self.normalized_sheet_name, **self.kwargs)
        #store the starting cleaned cols as start cols to revert future manipulations before returning
        self.starting_cols = sheet_data.columns
        #provides option to additionally cleanse headers after base updates above
        sheet_data.columns = self._clean_outgoing_headers(sheet_data.columns, **self.kwargs)
        self.current_cols = sheet_data.columns
        if self.duplicate_cols:
            raise Warning(f'duplicate columns present: {self.duplicate_cols}')
        return sheet_data
    
    
    def get_cols(self):
        return self.df.columns
    
    def update_cols(self, cols):
        self.df.columns = cols
        self.current_cols = cols
   
    #FIND WAY TO CREATE ERROR IF INCOMING HEADERS ARE ALL NULL
    def _clean_incoming_headers(self, cols, **kwargs):
        """remove duplicate columns named like .1, .2, .3 etc and then strip spaces"""
        pattern = f"(\.\d+)$"
        cols = [re.sub(pattern, '', i).strip() for i in cols]
        return cols

    def _make_headers_unique(self, cols, sheet_name = None, **kwargs):
        """add _1, _2, _3 etc. and log duplicate column records"""
        if len(cols) == len(set(cols)):
            return cols

        col_unique_counter = {col:0 for col in set(cols)}

        columns_new = []
        for col in cols:
            col_counter = col_unique_counter[col]
            if col_counter != 0:
                columns_new.append(f"{col}_{col_counter}")
                if sheet_name is not None:
                    self.duplicate_cols[col] = f"{col}_{col_counter}"
            else:
                columns_new.append(col)
            col_unique_counter[col] = col_unique_counter[col] + 1

        return columns_new
    
    def _clean_outgoing_headers(self, cols, clean = None, **kwargs):
        """if a clean kwarg is passed into the sheet object, it will apply in this function"""
        if clean is not None:
            cols = list(map(clean, cols))
        return cols
    