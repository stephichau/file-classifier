import json
from .service import GoogleSheets
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from utils.directory_handler import path_exists, create_directories
from utils.log import cool_print_decoration

STUDENTS_FILE_NAME = 'students_data.txt'

def main(file_save_path='', sheets_data='', spreadsheet_id='') -> int:
    """
    :param: file_save_path: should include
        abspath/results/:course_name:/:evaluation_name:
    """
    if path_exists('{}/{}'.format(file_save_path, STUDENTS_FILE_NAME)):
        cool_print_decoration('Information already stored in {}/{}\n\nTo update data, delete previous file.'.format(
            file_save_path, STUDENTS_FILE_NAME), style='info')
        return 0
    google_sheets = GoogleSheets(_type='SHEETS', sheets_data=sheets_data, spreadsheet_id=spreadsheet_id)
    google_sheets.authorize_credentials()
    google_sheets.create_service()
    cool_print_decoration('Connection with API successful.', style='result')
    cool_print_decoration('Starting data recolection.', style = 'info')
    google_sheets.fetch_data()
    cool_print_decoration('Saving data in {}.'.format(file_save_path), style='info')
	
    if not path_exists('{}'.format(file_save_path)):
        _dir_list = file_save_path.split('/')
        create_directories(dir_list=_dir_list)
        cool_print_decoration('Creating path directory {} path.'.format(file_save_path), style = 'info')

    students_data = google_sheets.students_data
    cool_print_decoration('Storing information in {}/{}'.format(file_save_path, STUDENTS_FILE_NAME), style = 'info')
    with open("{}/{}".format(file_save_path, STUDENTS_FILE_NAME), 'w') as file:
        json.dump(students_data, file, indent=4)
    cool_print_decoration('Information stored!', style = 'result')
    return 1


if __name__ == '__main__':
    pass
