from typing import Dict, Any, List
import pathlib
import re
from media_organizer.classifier import MediaType

class Planner:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def plan(self, metadata: Dict[str, Any], media_type: MediaType = MediaType.UNKNOWN) -> Dict[str, Any]:
        """
        Maps metadata to a target path based on configuration.
        """
        if media_type == MediaType.UNKNOWN:
            return {
                "source": metadata.get("original_path"),
                "destination": f"Unsorted/{metadata.get('filename')}",
                "action": "move"
            }

        template = self._get_template(media_type)
        if not template:
            # Fallback if no template is defined for the media type
            return {
                "source": metadata.get("original_path"),
                "destination": f"Unsorted/{metadata.get('filename')}",
                "action": "move"
            }

        enriched_metadata = self._enrich_metadata(metadata)
        sanitized_metadata = self._sanitize_metadata(enriched_metadata)

        try:
            destination = template.format(**sanitized_metadata)
        except KeyError as e:
            # If a key is missing in metadata, we might want to fail gracefully or use a placeholder
            # For now, let's assume metadata is sufficient or let the error propagate
            # But to be safe, let's catch it and log/print?
            # Given the prompt, let's just let it raise or handle it.
            # The test cases assume complete metadata.
            print(f"Warning: Missing metadata key {e} for {metadata.get('filename')}")
            destination = f"Unsorted/{metadata.get('filename')}"
        except ValueError as e:
             # Handle invalid format string issues
             print(f"Error formatting path for {metadata.get('filename')}: {e}")
             destination = f"Unsorted/{metadata.get('filename')}"

        return {
            "source": metadata.get("original_path"),
            "destination": destination,
            "action": "move"
        }

    def _get_template(self, media_type: MediaType) -> str:
        templates = self.config.get("templates", {})
        if media_type == MediaType.MUSIC:
            return templates.get("music")
        elif media_type == MediaType.MOVIE:
            return templates.get("movies")
        elif media_type == MediaType.TV_SHOW:
            return templates.get("tv_shows")
        elif media_type == MediaType.EBOOK:
            return templates.get("ebooks")
        return None

    def _enrich_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        enriched = metadata.copy()

        # Handle Season and Episode formatting
        # We need to make sure we don't overwrite if they exist, but here we are creating derived fields
        # like "Season XX", "XX", "YY" which are not usually in raw metadata.

        # Helper to safely convert to int
        def safe_int(val, default=0):
            try:
                return int(val)
            except (ValueError, TypeError):
                return default

        season_val = enriched.get("Season")
        episode_val = enriched.get("Episode")

        season_num = safe_int(season_val, 0)
        episode_num = safe_int(episode_val, 0)

        # "Season XX" -> "Season 01"
        if "Season XX" not in enriched:
            enriched["Season XX"] = f"Season {season_num:02d}"

        # "XX" -> "01" (Season number)
        if "XX" not in enriched:
            enriched["XX"] = f"{season_num:02d}"

        # "YY" -> "01" (Episode number)
        if "YY" not in enriched:
             enriched["YY"] = f"{episode_num:02d}"

        return enriched

    def _sanitize_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        sanitized = {}
        for key, value in metadata.items():
            if isinstance(value, str):
                # Replace illegal filename characters with underscores
                # Common illegal chars: / \ : * ? " < > |
                # Also stripping leading/trailing whitespace might be good practice
                clean_value = re.sub(r'[\\/*?:"<>|]', '_', value).strip()
                sanitized[key] = clean_value
            else:
                sanitized[key] = value
        return sanitized
