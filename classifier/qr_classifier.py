import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from numpy import ones, asarray, uint8
from .models import File
from cv2 import imdecode, morphologyEx, IMREAD_GRAYSCALE, MORPH_CLOSE
from pyzbar.pyzbar import decode, ZBarSymbol
from utils.directory_handler import path_exists, create_directory
from utils.file_handler import get_qr_sheet_number
from utils.file_converter import get_image
from utils.log import progress, cool_print_decoration, cool_print


class QRClassifier:
    def __init__(self, student_list, files_instance):
        """
        :student_list: array of Students -- has student_id and an array of sheet_ids
        """
        self.student_list = student_list
        self.file_list = files_instance.file_list
        self.question = files_instance.question_name
        self.misclassified_path = f'{files_instance.result_path}/Misclassified'
        self.data_dict = {'missed': []}
    
    def decode_data(self):
        def is_backpage(index):
            return index % 2 == 1
    
        def cast_image_to_bytesarray(img_instance):
            return asarray(bytearray(img_instance.make_blob(format='png')), dtype=uint8)
        
        def _decode(img):
            last_number = None
            for qr in decode(img, symbols=[ZBarSymbol.QRCODE]):
                qr_data = qr.data.decode('utf-8')
                if (qr_data):
                    number = get_qr_sheet_number(qr_data)
                    if (not self.data_dict.get(number)):
                        self.data_dict[number] = []
                    self.update_data_dict(key=number, file_instance=file_instance)
                    last_number = number
                else:
                    self.update_data_dict(key='missed', file_instance=file_instance)
                    last_number = None
            return last_number
        ## REFACTOR
        last_number = None
        for index, _img in enumerate(progress(self.file_list.sequence)):          
            img_instance = get_image(_img)
            file_instance = File(img_instance, self.question, index)
            if is_backpage(index):
                self.update_data_dict(key=last_number, file_instance=file_instance) if (last_number) else None
                self.update_data_dict(key='missed', file_instance=file_instance) if (last_number is None) else None
                continue
            img_bytes = cast_image_to_bytesarray(img_instance)
            img = imdecode(img_bytes, IMREAD_GRAYSCALE)
            last_number = _decode(img)
            del img
            del img_bytes
    
    def update_data_dict(self, key, file_instance, **kw):
        self.data_dict[key].append(file_instance)
    
    
    def classify(self):
        for student in progress(self.student_list):
            if (not path_exists(student.directory)): create_directory(student.directory)
            for sheet_num in student.sheet_numbers:
                if not self.data_dict.get(sheet_num): continue
                self.move_files(self.data_dict[sheet_num], student.directory)
    
    def move_misclassified_sheets(self):
        if (not path_exists(self.misclassified_path)): create_directory(self.misclassified_path)
        self.move_files(self.data_dict['missing'], self.misclassified_path) if self.data_dict['missing'] else None
    
    def move_file(self, file_instance, student_directory):
        # cool_print_decoration(f'Saving file to {student_directory}', style='info')
        try:
            file_instance.save(student_directory)
        except Exception as e:
            cool_print('Error saving file: {}'.format(e), style='alert')
        else:
            pass
            # cool_print('File successfully saved!', style='result')
    
    def move_files(self, file_instances: list, student_directory: str):
        list(map(lambda files: self.move_file(files, student_directory), file_instances))
