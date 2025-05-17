import json
import os
from dataclasses import dataclass, field

@dataclass
class Fstream:
    name: str
    path: str
    extension: str
    data_file: dict = field(init=False, default_factory=dict)

    @classmethod
    def load_json_files(cls, path: str) -> dict:
        """
        Read json files from a directory.

        Args:
             path the path for the json file to read.
        Returns:
             dict: A hash map with the json structure.
        """
        with open(path, "r") as data_file:
            data = json.load(data_file)

        return data
    
    @staticmethod
    def print_json_structure(data_file: dict):
       for id, item in data_file.get("items",{}).items():
           print(id, item)
