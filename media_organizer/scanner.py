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
                try:
                    rel_path = path.relative_to(self.input_path)
                except ValueError:
                    rel_path = path

                is_system_file = False
                for part in rel_path.parts:
                    if part.startswith('.'):
                        is_system_file = True
                        break

                if is_system_file:
                    continue

                if path.name.lower() in ['thumbs.db', 'desktop.ini']:
                    continue

                files.append(path)
        return files
