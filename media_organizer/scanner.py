import pathlib
from typing import List

class Scanner:
    def __init__(self, input_path: str):
        self.input_path = pathlib.Path(input_path)

    def scan(self) -> List[pathlib.Path]:
        """
        Recursively scans the input path and returns a list of file paths.
        """
        files = []
        if not self.input_path.exists():
            return files

        for path in self.input_path.rglob('*'):
            if path.is_file():
                files.append(path)
        return files
