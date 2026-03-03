import typer
from media_organizer.scanner import Scanner
from media_organizer.classifier import Classifier
from media_organizer.analyzer import Analyzer
from media_organizer.planner import Planner
from media_organizer.executor import Executor
from media_organizer.config import Config

app = typer.Typer()

@app.command()
def run(config_path: str = "config.yaml", dry_run: bool = True):
    """
    Main entry point for the media organizer.
    """
    config = Config(config_path)
    try:
        config.load()
    except FileNotFoundError:
        print("Config file not found. Using defaults.")
        # Create a default config or exit
        return

    scanner = Scanner(config.data.get("input_dir", "."))
    classifier = Classifier()
    analyzer = Analyzer()
    planner = Planner(config.data)
    executor = Executor(dry_run=dry_run)

    files = scanner.scan()
    for file_path in files:
        media_type = classifier.classify(file_path)
        metadata = analyzer.analyze(file_path)
        plan = planner.plan(metadata, media_type)
        executor.execute(plan)

if __name__ == "__main__":
    app()
