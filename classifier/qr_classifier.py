import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from numpy import ones
from cv2 import imread, morphologyEx, IMREAD_GRAYSCALE, MORPH_CLOSE
from pyzbar.pyzbar import decode, ZBarSymbol
from shutil import move
from utils.directory_handler import path_exists, create_directory
from utils.log import progress, cool_print_decoration


class QRClassifier:
    def __init__(self, student_list, file_list):
        """
        :student_list: array of Students -- has student_id and an array of sheet_ids
        """
        self.student_list = student_list
        self.file_list = file_list # [ Wand.Image instances ]
    
    def decode_data(self):
        pass
    
    def classify(self, data_dict={}):
        for student in progress(self.student_list):
            if (not path_exists(student.directory)): create_directory(student.directory)
            for sheet_num in student.sheet_numbers:
                if not data_dict.get(sheet_num): continue
                self.move_files(data_dict[sheet_num], student.directory)
    
    def move_file(self, file_path, student_directory):
        cool_print_decoration(f'Moving file from {file_path} to {student_directory}', style='info')
        try:
            move(file_path, student_directory)
        except Exception as e:
            cool_print_decoration('Error moving file: {}'.format(e), style='alert')
        else:
            cool_print_decoration('File successfully moved!', style='result')
    
    def move_files(self, file_paths: list, student_directory: str):
        list(map(lambda files: self.move_file(files, student_directory), file_paths))
