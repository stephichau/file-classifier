from .classifiers import ClassifierWrapper
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


def main(files_instance, student_list=[], ocr=''):
    classifier = ClassifierWrapper(files_instance=files_instance, student_list=student_list)
    classifier.classify_data(ocr=ocr)

if __name__ == '__main__':
    pass
