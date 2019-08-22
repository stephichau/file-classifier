from argparse import ArgumentParser
from classifier import main as file_classifier
from classifier.models import Files, Student
from google_sheets import main as g_sheets
import json
from utils.directory_handler import path_exists
import utils.parse_arguments as p
from utils.json_reader import read_data
from utils.file_converter import multiple_pdf_to_png
from utils.file_handler import check_downloaded_google_sheet_data, create_student_instances
from utils.log import cool_print_decoration, cool_print
from sheet_maker import main as make
from sys import argv
# from testing.setup import *

def classify(file_name: str):
    ## Set initial params
    with open(file_name, 'r') as f:
        f = json.load(f)
    year = f['year']
    semester = f['semester']
    course = f['course']
    evaluation = f['evaluation']
    files = f['files']
    ocr = f['ocr']
    sheet_id = f['evaluation_sheet_id']
    g_sheets_file = f'results/{course}/{year}-{semester}/{evaluation}'
    if (not check_downloaded_google_sheet_data(g_sheets_file)):
        g_sheets(file_save_path=g_sheets_file, sheets_data='sheets_data.txt', spreadsheet_id=sheet_id)
    student_list = create_student_instances(g_sheets_file, Student)
    # Iterate for each file === one question P1 / P2 ... PN
    for info in files:
        question = list(info.keys())[0]
        path = info[question]
        file = Files(course_name=course, evaluation_name=evaluation, file_path=path, question_name=question)
        cool_print_decoration(f'Processing question:{question}\nOCR: {ocr}', style='info')
        cool_print('Transforming .pdf into .png', style='info')
        file_list = multiple_pdf_to_png(f_name=path, save=False)
        cool_print('Finished transforming .pdf into .png!', style='info')
        file.set_file_list(file_list)
        file_classifier(file, student_list=student_list, ocr=ocr)

OPTIONS = {
    1: 'Setup test',
    2: make.main,
    3: classify
}

def main():
    _parser = ArgumentParser()
    _args = p.create_arguments_main(_parser).parse_args(argv[1:])
    _opt = p.check_option(_args)

    OPTIONS[_opt] if _opt == 1 else None
    OPTIONS[_opt](_args.filename) if _opt > 1 and path_exists(_args.filename) else print_invalid_options()
    

def print_invalid_options():
    _msg = 'Error.\nPlease check available flags commands for CLI or check file path and name'
    cool_print_decoration(_msg, 'danger')

if __name__ == '__main__':
    main()
