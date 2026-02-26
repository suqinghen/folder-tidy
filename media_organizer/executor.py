from typing import Dict, Any
import pathlib
import shutil

class Executor:
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run

    def execute(self, plan: Dict[str, Any]):
        """
        Executes the plan (moves/renames files).
        """
        source = pathlib.Path(plan["source"])
        destination = pathlib.Path(plan["destination"])

        if self.dry_run:
            print(f"[DRY RUN] Would move {source} to {destination}")
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))
            print(f"Moved {source} to {destination}")
