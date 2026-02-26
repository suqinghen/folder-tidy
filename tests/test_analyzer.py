import pathlib
from media_organizer.analyzer import Analyzer

def test_analyzer_init():
    analyzer = Analyzer()
    assert isinstance(analyzer, Analyzer)

def test_analyzer_analyze():
    analyzer = Analyzer()
    path = pathlib.Path("test/song.mp3")
    metadata = analyzer.analyze(path)
    assert metadata["filename"] == "song.mp3"
    assert metadata["original_path"] == "test/song.mp3"
