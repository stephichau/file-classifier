from .classifiers import ClassifierWrapper
import io
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from utils.directory_handler import path_exists, create_directories
from utils.log import cool_print_decoration, progress


def main(files_instance, student_list=[], _type=''):
    classifier = ClassifierWrapper(file_list=files_instance.file_list, student_list=student_list)
    classifier.classify_data(_type=_type)

if __name__ == '__main__':
    pass
