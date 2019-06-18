import os

def path_exists(path: str) -> bool:
    return os.path.exists(path)

def create_directory(path: str) -> None:
    os.mkdir(path)

def create_directories(dir_list: list, **kwargs):
    _path = ''
    for dir_name in dir_list:
        _path += '{}/'.format(dir_name)
        create_directory(_path) if not path_exists(_path) else None
