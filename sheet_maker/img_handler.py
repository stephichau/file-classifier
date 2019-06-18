from PIL import Image, ImageDraw, ImageFont
from utils.log import progress

FONT_SIZE = 80
FONT_STYLE = { 'CourierNew' : 'Courier New.ttf', 'Arial': 'arial.ttf' }

def add_text_img(_template: Image, left: int, _data: str) -> Image:
    draw = ImageDraw.Draw(_template)
    fnt = ImageFont.truetype(FONT_STYLE['CourierNew'], int(FONT_SIZE/1.5))
    draw.text((left, FONT_SIZE), _data, font=fnt, fill="black")
    return _template

def composite_img(_template: Image, _data:str, _save_page=False, _save_path='') -> Image:
    _left = int(_template.width - FONT_SIZE * (len(_data)//1.5))
    _template = add_text_img(_template, _left, _data)
    _template.save(f'{_save_path}/{_data}.png') if _save_page else None
    return _template

def composite_multiple_images(_files: list, _save_pages=False, _save_path='') -> list:    
    return list(map(lambda _img_tuple:
        composite_img(*_img_tuple, _save_page=_save_pages, _save_path=_save_path), progress(_files)))
