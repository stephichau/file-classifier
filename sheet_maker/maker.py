from PIL import Image
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from utils.log import progress

def png_template_exists(path: str) -> bool:
    return not os.path.exists(f'{path}.png') and os.path.exists(f'{path}.pdf')

def make_files(_file_data: dict, _save_file=False) -> list:
    ocr = _file_data['ocr']
    _files_list = list()
    _lower_bound = int(_file_data['lower_bound'])
    _upper_bound = int(_file_data['upper_bound'])
    _course = _file_data['course']
    _eval = _file_data['evaluation']
    partial_data = f'{_course}_{_eval}'
    if (ocr == 'qr'):
        _semester = _file_data['semester']
        _section = _file_data['section']
        _year = _file_data['year']
        _instructor = _file_data['instructor']
        partial_data = f'{partial_data}_{_year}_{_semester}_{_section}_{_instructor}'
    _template_path = _file_data['template']

    for idx in progress(range(_lower_bound, _upper_bound + 1)):
        _data = f'{partial_data}_{idx}' if ocr == 'qr' else f'{_course}__{idx}'
        _template = Image.open(_template_path)
        _files_list.append((_template, _data))

    return _files_list
