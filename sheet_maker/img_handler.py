from PIL import Image, ImageDraw, ImageFont
from .qr_handler import new_qr
from utils.log import progress

FONT_SIZE = 65
FONT_STYLE = { 'CourierNew' : 'Courier New.ttf', 'Arial': 'arial.ttf' }
QR_POSITION_PONDERATOR = 1.8
QR_SIZE = 150
TEXT_POSITION_PONDERATOR = 1.65

def add_text_img(_template: Image, left: int, _data: str, ocr: str) -> Image:
    draw = ImageDraw.Draw(_template)
    fnt = ImageFont.truetype(FONT_STYLE['CourierNew'], int(FONT_SIZE/1.5))
    height = QR_SIZE + 100 if ocr == 'qr' else FONT_SIZE
    draw.text((left, height), _data, font=fnt, fill='black')
    return _template

def add_qr_img(_template: Image, left: int, _data: str) -> Image:
    qr = new_qr(_data)
    resized_qr = qr.resize((QR_SIZE, QR_SIZE), Image.ANTIALIAS)
    _left = int(_template.width - resized_qr.width * QR_POSITION_PONDERATOR)
    _top = 80
    qr_number = _data.split('_')[-1]
    _text_left = int(_template.width - resized_qr.width * TEXT_POSITION_PONDERATOR)
    _template_with_text = add_text_img(_template, _text_left, qr_number, 'qr')
    _template_with_text.paste(resized_qr, (_left, _top))
    return _template_with_text

def composite_img(_template: Image, _data: str, _save_page=False, _save_path='', ocr='qr') -> Image:
    _left = int(_template.width - FONT_SIZE * (len(_data)//1.5))
    _template = add_text_img(_template, _left, _data, ocr=ocr) if ocr != 'qr' else add_qr_img(_template, _left, _data)
    _template.save(f'{_save_path}/{_data}.png') if _save_page else None
    return _template

def composite_multiple_images(_files: list, _save_pages=False, _save_path='', ocr='qr') -> list:    
    return list(map(lambda _img_tuple:
        composite_img(*_img_tuple, _save_page=_save_pages, _save_path=_save_path, ocr=ocr), progress(_files)))
