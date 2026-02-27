import pytest
from media_organizer.planner import Planner
from media_organizer.classifier import MediaType

@pytest.fixture
def config():
    return {
        "templates": {
            "music": "Music/{Artist}/{Album} ({Year})/{Track} - {Title}.{ext}",
            "movies": "Movies/{Title} ({Year})/{Title} ({Year}).{ext}",
            "tv_shows": "TV Shows/{Series}/{Season XX}/{Series} - S{XX}E{YY} - {Episode Title}.{ext}",
            "ebooks": "Books/{Author}/{Series}/{Index} - {Title}.{ext}"
        }
    }

def test_plan_music(config):
    planner = Planner(config)
    metadata = {
        "original_path": "/downloads/song.mp3",
        "filename": "song.mp3",
        "Artist": "The Beatles",
        "Album": "Abbey Road",
        "Year": "1969",
        "Track": "01",
        "Title": "Come Together",
        "ext": "mp3"
    }
    plan = planner.plan(metadata, MediaType.MUSIC)
    expected_dest = "Music/The Beatles/Abbey Road (1969)/01 - Come Together.mp3"
    assert plan["destination"] == expected_dest
    assert plan["source"] == "/downloads/song.mp3"
    assert plan["action"] == "move"

def test_plan_movie(config):
    planner = Planner(config)
    metadata = {
        "original_path": "/downloads/movie.mkv",
        "filename": "movie.mkv",
        "Title": "Inception",
        "Year": "2010",
        "ext": "mkv"
    }
    plan = planner.plan(metadata, MediaType.MOVIE)
    expected_dest = "Movies/Inception (2010)/Inception (2010).mkv"
    assert plan["destination"] == expected_dest

def test_plan_tv_show(config):
    planner = Planner(config)
    metadata = {
        "original_path": "/downloads/tv_show.mkv",
        "filename": "tv_show.mkv",
        "Series": "Breaking Bad",
        "Season": "1",
        "Episode": "1",
        "Episode Title": "Pilot",
        "ext": "mkv"
    }
    # The template uses {Season XX}, {XX}, {YY}
    # Planner needs to generate these from Season and Episode if not present, or if logic dictates
    plan = planner.plan(metadata, MediaType.TV_SHOW)

    # Expected: "TV Shows/Breaking Bad/Season 01/Breaking Bad - S01E01 - Pilot.mkv"
    expected_dest = "TV Shows/Breaking Bad/Season 01/Breaking Bad - S01E01 - Pilot.mkv"
    assert plan["destination"] == expected_dest

def test_plan_ebook(config):
    planner = Planner(config)
    metadata = {
        "original_path": "/downloads/book.epub",
        "filename": "book.epub",
        "Author": "J.K. Rowling",
        "Series": "Harry Potter",
        "Index": "1",
        "Title": "The Sorcerer's Stone",
        "ext": "epub"
    }
    plan = planner.plan(metadata, MediaType.EBOOK)
    expected_dest = "Books/J.K. Rowling/Harry Potter/1 - The Sorcerer's Stone.epub"
    assert plan["destination"] == expected_dest

def test_sanitization(config):
    planner = Planner(config)
    metadata = {
        "original_path": "/downloads/song.mp3",
        "filename": "song.mp3",
        "Artist": "AC/DC",  # Contains slash
        "Album": "Highway to Hell",
        "Year": "1979",
        "Track": "01",
        "Title": "Highway to Hell",
        "ext": "mp3"
    }
    plan = planner.plan(metadata, MediaType.MUSIC)
    # AC/DC should be sanitized to AC_DC or similar to avoid directory creation
    # Let's assume replacement with underscore for now
    expected_dest = "Music/AC_DC/Highway to Hell (1979)/01 - Highway to Hell.mp3"
    assert plan["destination"] == expected_dest
