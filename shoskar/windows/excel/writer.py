import tempfile
import os
import pandas as pd
import xlsxwriter

def file_writer(file_name, file_type = 'xlsx', sheets = {}, auto_fit_headers = True, max_col_width = 50, file_path = 'temp'):

    if file_path == 'temp':
        file_path = tempfile.gettempdir()
    write_path = os.path.join(file_path, f'{file_name}.{file_type}')
    check_sheet_name = {}
    writer = pd.ExcelWriter(write_path, engine='xlsxwriter')

    for sheet_name, data in sheets.items():
        if sheet_name in check_sheet_name.keys():
            check_sheet_name[sheet_name] += 1
            sheet_name += str(check_sheet_name[sheet_name])
        else:
            check_sheet_name[sheet_name] = 1

        data.to_excel(writer, sheet_name=sheet_name, index = False)

        if auto_fit_headers:

            work_sheet = writer.sheets[sheet_name]

            for i, col in enumerate(data):
                series = data[col]
                max_len = max((
                            series.astype(str).map(len).max(),  # len of largest item
                            len(str(series.name))  # len of column name/header
                            )) + 5 #adds a buffer - max_len alone is crowded
                col_len = min(max_col_width, max_len)
                work_sheet.set_column(i, i, col_len)
    
    writer.close()

    return file_path
