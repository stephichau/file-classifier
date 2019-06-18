from .directory_handler import *
from .file_converter import *
from .file_merger import *
from .json_reader import *
from .log import *
from .parse_arguments import *

def create_directory(dir_path: str) -> None:
    os.mkdir(dir_path)
