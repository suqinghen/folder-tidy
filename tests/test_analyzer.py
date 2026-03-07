import os
import pathlib
import unittest.mock
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

def test_analyzer_audio_metadata(tmp_path):
    audio_path = tmp_path / "test_audio.mp3"
    audio_path.touch()

    class MockTag:
        def __init__(self, text):
            self.text = [text]
        def __str__(self):
            return self.text[0]

    mock_audio = unittest.mock.MagicMock()
    mock_audio.tags = {
        'TIT2': MockTag("Mock Title"),
        'TPE1': MockTag("Mock Artist"),
        'TALB': MockTag("Mock Album"),
        'TDRC': MockTag("2024")
    }

    with unittest.mock.patch('mutagen.File', return_value=mock_audio):
        analyzer = Analyzer()
        metadata = analyzer.analyze(audio_path)

    assert metadata["filename"] == "test_audio.mp3"
    assert metadata["original_path"] == str(audio_path)
    assert metadata.get("Title") == "Mock Title"
    assert metadata.get("Artist") == "Mock Artist"
    assert metadata.get("Album") == "Mock Album"
    assert metadata.get("Year") == "2024"
