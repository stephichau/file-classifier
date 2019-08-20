class Student:
    def __init__(self, student_id='', sheet_numbers=[], *args, **kw):
        self.student_id = student_id
        self.sheet_numbers = sheet_numbers

class File:
    def __init__(self):
        pass

class Files:
    def __init__(self, course_name='', evaluation_name= '', file_path='', question_name='', *args, **kw):
        self.course_name = course_name
        self.evaluation_name = evaluation_name
        self.file_path = file_path
        self.question_name = question_name
        self._file_list = None
        self.classified_file_list = []
    
    @property
    def file_list(self):
        return self._file_list
    
    @file_list.setter
    def file_list(self, f_list):
        self._file_list = f_list
        
    def set_file_list(self, f_list):
        self.file_list = f_list
        
    def add_classified_file_list(self, file: File):
        self.classified_file_list.append(file)