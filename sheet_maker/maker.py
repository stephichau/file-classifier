from PIL import Image, ImageDraw, ImageFont
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from utils.log import progress

def png_template_exists(path: str) -> bool:
    return not os.path.exists(f'{path}.png') and os.path.exists(f'{path}.pdf')

def make_files(_file_data: dict, _save_file=False) -> list:
    _files_list = list()
    _lower_bound = int(_file_data['lower_bound'])
    _upper_bound = int(_file_data['upper_bound'])
    _course = _file_data['course']
    _eval = _file_data['evaluation']
    _template_path = _file_data['template']

    for idx in progress(range(_lower_bound, _upper_bound + 1)):
        # _data = f'{_course}_{_eval}__{idx}'
        _data = f'{_course}__{idx}'
        _template = Image.open(_template_path)
        _files_list.append((_template, _data))

    return _files_list
