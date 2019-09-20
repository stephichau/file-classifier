import json
import os

def get_params(file_data: str) -> dict:
    _data = {}
    with open(file_data) as file:
        _data = json.load(file)
    return _data
