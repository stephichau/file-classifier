import io
import os
import pytesseract
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from utils.file_converter import get_image, crop_image
from utils.log import cool_print_decoration, progress
from PIL import Image
from pytesseract import image_to_string
import pyocr

class ClassifierWrapper:
    def __init__(self, student_list=[], file_list=[],*args, **kw):
        self.student_list = student_list
        self.file_list = file_list
    
    def classify_data(self, _type):
        """
        Applies pytesseract.image_to_string for each Image instance found if _type == text
        Applies other classifier depending on _type
        """
        if (_type == 'text'):
            self.pytesseract_classifier()
        elif (_type == 'qr'):
            self.qr_classifier()
    
    def pytesseract_classifier(self):
        student_list = []
        img_blobs = []
        for index, img_instance in enumerate(progress(self.file_list.sequence)):
            if index % 2 == 1:
                continue
            img = get_image(img_instance)
            img = crop_image(img)
            blob = img.make_blob('png')
            new_image = Image.open(io.BytesIO(blob)).convert('L')
            # text = pyocr.get_available_tools()[0].image_to_string(new_image, builder=pyocr.builders.TextBuilder())
            # print(text)
            img.save(filename=f'blob-{index}.png')
            # print(image_to_string(new_image))
    
    def qr_classifier(self):
        pass
