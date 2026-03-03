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

def test_scanner_ignores_hidden_files(tmp_path):
    (tmp_path / "test.txt").touch()
    (tmp_path / ".DS_Store").touch()
    (tmp_path / ".hidden_file.txt").touch()

    scanner = Scanner(str(tmp_path))
    files = scanner.scan()
    assert len(files) == 1
    assert pathlib.Path(tmp_path / "test.txt") in files

def test_scanner_ignores_hidden_directories(tmp_path):
    (tmp_path / "test.txt").touch()
    hidden_dir = tmp_path / ".git"
    hidden_dir.mkdir()
    (hidden_dir / "config").touch()
    (hidden_dir / "HEAD").touch()

    scanner = Scanner(str(tmp_path))
    files = scanner.scan()
    assert len(files) == 1
    assert pathlib.Path(tmp_path / "test.txt") in files

def test_scanner_ignores_windows_system_files(tmp_path):
    (tmp_path / "test.txt").touch()
    (tmp_path / "Thumbs.db").touch()
    (tmp_path / "desktop.ini").touch()
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "thumbs.db").touch()

    scanner = Scanner(str(tmp_path))
    files = scanner.scan()
    assert len(files) == 1
    assert pathlib.Path(tmp_path / "test.txt") in files
