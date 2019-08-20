from wand.image import Image
from wand.color import Color
from .directory_handler import path_exists, create_directory
from .log import progress

def pdf_to_png(f_name: str) -> None:
    image = Image(filename=f_name, resolution=250)
    with Image(image) as i:
        i.format = 'png'
        i.background_color = Color('white')
        i.alpha_channel = 'remove'
        i.save(filename=f_name.replace('pdf', 'png'))

def multiple_pdf_to_png(f_name='', save=False) -> list:
    create_directory('./TMP') if not path_exists('./TMP') else None
    img = Image(filename=f_name, resolution=300)
    converted = img.convert('png')
    list(map(lambda file: get_image(file[1]).save(filename=f'./TMP/page-{file[0]}.png'), enumerate(progress(converted.sequence)))) if save else None
    return converted

def get_image(img_instance):
    return Image(image=img_instance)

def crop_image(img_instance, _type='text'):
    width = img_instance.width
    height = img_instance.height
    if (_type == 'text'):
        img_instance.crop(int(width*0.7), int(height * 0.02), int(width*0.95), int(height * 0.076))
    return img_instance


if __name__ == '__main__':
    print(multiple_pdf_to_png('./SCANNED_FILES/mt-p1-2019-1.pdf', save=True))
