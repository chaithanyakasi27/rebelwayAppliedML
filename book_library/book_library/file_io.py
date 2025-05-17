import json

class Fstream:
    @staticmethod
    def load_json_file(path: str) -> dict:
        """
        Read a json file from the given path.

        Args:
            path (str): Path to the json file.

        Returns:
            dict: Parsed json data.
        """
        with open(path, "r") as data_file:
            data = json.load(data_file)
        return data

    @staticmethod
    def print_json_structure(data_file: dict):
        for id, item in data_file.get("items", {}).items():
            print(id, item)

