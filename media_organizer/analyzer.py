import pathlib
from typing import Dict, Any
import mutagen

class Analyzer:
    def analyze(self, file_path: pathlib.Path) -> Dict[str, Any]:
        """
        Analyzes the file and returns metadata.
        This will eventually use LLMs.
        """
        metadata = {
            "original_path": str(file_path),
            "filename": file_path.name,
        }

        # Basic extension check to attempt audio metadata extraction
        if file_path.suffix.lower() in {'.mp3', '.flac', '.m4a', '.ogg'}:
            try:
                audio = mutagen.File(str(file_path))
                if audio and audio.tags:
                    # Generic mapping of common ID3/Vorbis/MP4 tags
                    # For MP3 (ID3v2)
                    if 'TIT2' in audio.tags:
                        metadata['Title'] = str(audio.tags['TIT2'])
                    if 'TPE1' in audio.tags:
                        metadata['Artist'] = str(audio.tags['TPE1'])
                    if 'TALB' in audio.tags:
                        metadata['Album'] = str(audio.tags['TALB'])
                    if 'TDRC' in audio.tags:
                        metadata['Year'] = str(audio.tags['TDRC'])

                    # For FLAC/Ogg (Vorbis Comments)
                    if 'title' in audio.tags:
                        metadata['Title'] = str(audio.tags['title'][0]) if isinstance(audio.tags['title'], list) else str(audio.tags['title'])
                    if 'artist' in audio.tags:
                        metadata['Artist'] = str(audio.tags['artist'][0]) if isinstance(audio.tags['artist'], list) else str(audio.tags['artist'])
                    if 'album' in audio.tags:
                        metadata['Album'] = str(audio.tags['album'][0]) if isinstance(audio.tags['album'], list) else str(audio.tags['album'])
                    if 'date' in audio.tags:
                        metadata['Year'] = str(audio.tags['date'][0]) if isinstance(audio.tags['date'], list) else str(audio.tags['date'])

                    # For MP4 (M4A) keys
                    if '\xa9nam' in audio.tags:
                        metadata['Title'] = str(audio.tags['\xa9nam'][0]) if isinstance(audio.tags['\xa9nam'], list) else str(audio.tags['\xa9nam'])
                    if '\xa9ART' in audio.tags:
                        metadata['Artist'] = str(audio.tags['\xa9ART'][0]) if isinstance(audio.tags['\xa9ART'], list) else str(audio.tags['\xa9ART'])
                    if '\xa9alb' in audio.tags:
                        metadata['Album'] = str(audio.tags['\xa9alb'][0]) if isinstance(audio.tags['\xa9alb'], list) else str(audio.tags['\xa9alb'])
                    if '\xa9day' in audio.tags:
                        metadata['Year'] = str(audio.tags['\xa9day'][0]) if isinstance(audio.tags['\xa9day'], list) else str(audio.tags['\xa9day'])
            except Exception as e:
                # If extraction fails, we just fall back to filename metadata
                pass

        return metadata
