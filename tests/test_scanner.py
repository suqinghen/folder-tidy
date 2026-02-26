import pathlib
from media_organizer.scanner import Scanner

def test_scanner_init(tmp_path):
    scanner = Scanner(str(tmp_path))
    assert isinstance(scanner, Scanner)
    assert scanner.input_path == tmp_path

def test_scanner_scan_empty(tmp_path):
    scanner = Scanner(str(tmp_path))
    assert scanner.scan() == []

def test_scanner_scan_files(tmp_path):
    (tmp_path / "test.txt").touch()
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir/test2.mp3").touch()

    scanner = Scanner(str(tmp_path))
    files = scanner.scan()
    assert len(files) == 2
    assert pathlib.Path(tmp_path / "test.txt") in files
    assert pathlib.Path(tmp_path / "subdir/test2.mp3") in files
