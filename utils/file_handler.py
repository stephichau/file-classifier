import os
from json import load

def check_downloaded_google_sheet_data(g_sheets_file) -> bool:
    file = f'{g_sheets_file}/students_data.txt'
    return os.path.exists(file)

def get_student_data(results_path) -> list:
    file = f'{results_path}/students_data.txt'
    with open(file, 'r') as _f:
        f = load(_f)
    return f

def create_student_instance(student_class, student_id: str, sheet_numbers: list, student_path: str):
    return student_class(student_id, sheet_numbers, student_path)

def create_student_instances(results_path, student_class) -> list:
    student_data = get_student_data(results_path)
    return [create_student_instance(student_class, student_id, student_data[student_id], results_path) for student_id in student_data]

def get_qr_sheet_number(qr_data: str) -> str:
    return qr_data.split('_')[-1]