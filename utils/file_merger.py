import os
from utils.log import progress

def pdf_merger(_img_list: list, _path_name: str) -> None:
    _img_list[0].save(_path_name, 'PDF', resolution=20,
        save_all=True, append_images=progress(_img_list[1:]))
