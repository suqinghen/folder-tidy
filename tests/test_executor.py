import pathlib
from media_organizer.executor import Executor

def test_executor_init():
    executor = Executor()
    assert isinstance(executor, Executor)

def test_executor_execute_dry_run(capsys):
    executor = Executor(dry_run=True)
    plan = {
        "source": "test/song.mp3",
        "destination": "organized/song.mp3"
    }
    executor.execute(plan)
    captured = capsys.readouterr()
    assert "Would move" in captured.out
