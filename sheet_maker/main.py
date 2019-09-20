from time import time, asctime, localtime
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from utils.log import cool_print_decoration, cool_print, print_invalid_file
from utils.file_merger import pdf_merger
from utils.file_converter import pdf_to_png
from utils.json_reader import check_file, read_data
from utils.file_copies import make_copies
from utils import create_directory

from .maker import png_template_exists, make_files
from .img_handler import composite_multiple_images

from PIL import Image

TEMPLATE_DIRECTORY = 'TEMPLATES'

def main(_file='', _data={}) -> int:

    if (_file):
        _data = read_data(_file) if check_file(_file) else {}
        
        if not _data:
            print_invalid_file(_file)
            return 0
    
    COURSE_NAME = _data['course']
    EVALUATION = _data['evaluation']
    OCR = _data['ocr']
    COPIES = _data['copies'] if _data.get('copies') else 1

    create_directory(f'{os.getcwd()}/ANSWER_SHEETS/') if not os.path.exists(f'{os.getcwd()}/ANSWER_SHEETS/') else None

    ANSWER_SHEETS_DIR_PATH = f'{os.getcwd()}/ANSWER_SHEETS/{COURSE_NAME}_{EVALUATION}'

    cool_print(f'\nAnswer sheets will be available in: {ANSWER_SHEETS_DIR_PATH}', style='result')

    _current_time = asctime(localtime(time()))
    cool_print(f'\n\nInitializing program...[{_current_time}]', style='info')
    
    if png_template_exists(f'{TEMPLATE_DIRECTORY}/{_data["template"]}'):
        cool_print_decoration('ERROR: Found template in .pdf format.\nConverting template to .png format...', 'danger')
        pdf_to_png(f'{TEMPLATE_DIRECTORY}/{_data["template"]}.pdf')

    create_directory(ANSWER_SHEETS_DIR_PATH) if not os.path.exists(ANSWER_SHEETS_DIR_PATH) else None

    _data['template'] = f'{TEMPLATE_DIRECTORY}/{_data["template"]}.png'
    cool_print(f'\nPreparing data...', style='info')
    _files = make_files(_data, _save_file=False)

    cool_print(f'\nAdding texts to templates...', style='info')
    _answer_sheets = composite_multiple_images(_files, _save_pages=False, _save_path=ANSWER_SHEETS_DIR_PATH, ocr=OCR)
    
    _answer_sheets = _answer_sheets if COPIES == 1 else make_copies(_answer_sheets, COPIES)
    
    cool_print(f'\nMerging files...[could take a while]', style='info')
    pdf_merger(_answer_sheets, f'{ANSWER_SHEETS_DIR_PATH}/compilation.pdf')

    cool_print(f'\nDone!', style='info')

    return 1


if __name__ == '__main__':
    pass