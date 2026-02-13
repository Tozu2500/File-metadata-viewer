# Audio metadata extractor

from pathlib import Path
from typing import Dict, Any
from .base_extractor import BaseExtractor

try:
    from mutagen import File as MutagenFile
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False


class AudioExtractor(BaseExtractor):
    # Extract metadata from audio-files

    def extract(self) -> Dict[str, Any]:
        # Extract audio metadata

        metadata = {}

        if not MUTAGEN_AVAILABLE:
            metadata["Error"] = "Mutagen not available"
            return metadata
        
        try:
            audio = MutagenFile(str(self.file_path))

            if audio is None:
                metadata["Error"] = "Unsupported audio format"
                return metadata
            
            # Basic audio info
            if hasattr(audio.info, 'length'):
                metadata["Duration"] = audio.info.length

            if hasattr(audio.info, 'bitrate'):
                metadata["Bitrate"] = audio.info.bitrate

            if hasattr(audio.info, 'sample_rate'):
                metadata["Sample Rate"] = f"{audio.info.sample_rate} Hz"

            if hasattr(audio.info, 'channels'):
                metadata["Channels"] = audio.info.channels

            if hasattr(audio.info, 'bits_per_sample'):
                metadata["Bits Per Sample"] = audio.info.bits_per_sample

            # Codec info
            if hasattr(audio, 'mime'):
                metadata["MIME Type"] = '; '.join(audio.mime)

            # Extract tags
            if audio.tags:
                tag_data = self._extract_tags(audio.tags)
                metadata.update(tag_data)

        except Exception as e:
            metadata["Error"] = f"Failed to extract metadata: {str(e)}"

        return metadata
    
    def _extract_tags(self, tags) -> Dict[str, Any]:
        # Extract tags from audio files
        tag_data = {}
        seen_raw_keys = set()

        try:
            # Common tag mappings
            tag_mappings = {
                'title': 'Title',
                'artist': 'Artist',
                'album': 'Album',
                'albumartist': 'Album Artist',
                'date': 'Date',
                'genre': 'Genre',
                'composer': 'Composer',
                'performer': 'Performer',
                'conductor': 'Conductor',
                'organization': 'Organization',
                'copyright': 'Copyright',
                'comment': 'Comment',
                'lyrics': 'Lyrics',
                'tracknumber': 'Track Number',
                'discnumber': 'Disc Number',
                'bpm': 'BPM',
                'isrc': 'ISRC',
                'language': 'Language',
            }

            # Try to extract common tags
            for key, display_name in tag_mappings.items():
                # Try case variations
                for tag_key in [key, key.upper(), key.title()]:
                    if tag_key in tags:
                        value = tags[tag_key]
                        if isinstance(value, list):
                            value = ', '.join(str(v) for v in value)
                        tag_data[display_name] = str(value)
                        seen_raw_keys.add(tag_key)
                        break

            # Extract all other tags
            for key in tags.keys():
                if key in seen_raw_keys:
                    continue
                value = tags[key]
                if isinstance(value, list):
                    value = ', '.join(str(v) for v in value)

                # Clean up key name
                display_key = str(key).replace(':', ' ').title()
                tag_data[f"Tag {display_key}"] = str(value)

        except Exception as e:
            tag_data["Tag Error"] = str(e)

        return tag_data