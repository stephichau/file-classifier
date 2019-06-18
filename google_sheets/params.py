import json
import os

def get_params(file_data: str) -> dict:
    _data = {}
    with open(file_data) as file:
        _data = json.load(file)
    return _data

_path = os.path.abspath('google_sheets/sheets_data.txt')
params = get_params(file_data=_path)

EVALUATION_NAME, COURSE_NAME, SPREADSHEET_ID = (params[key] for key in ('evaluation_name', 'course', 'evaluation_sheet_id'))
