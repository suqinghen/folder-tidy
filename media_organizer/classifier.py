import pathlib
from enum import Enum

class MediaType(Enum):
    MUSIC = "music"
    MOVIE = "movie"
    TV_SHOW = "tv_show"
    EBOOK = "ebook"
    UNKNOWN = "unknown"

class Classifier:
    def __init__(self):
        pass

    def classify(self, file_path: pathlib.Path) -> MediaType:
        """
        Determines the media type of the given file.
        """
        # Placeholder implementation
        suffix = file_path.suffix.lower()
        if suffix in {'.mp3', '.flac', '.m4a'}:
            return MediaType.MUSIC
        elif suffix in {'.mp4', '.mkv', '.avi'}:
            # Naive distinction between movies and TV shows often requires more context
            return MediaType.MOVIE
        elif suffix in {'.epub', '.pdf', '.mobi'}:
            return MediaType.EBOOK

        return MediaType.UNKNOWN
