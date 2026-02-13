# Video metadata extractor

from pathlib import Path
from typing import Dict, Any
import subprocess
import json
from .base_extractor import BaseExtractor


class VideoExtractor(BaseExtractor):
    # Extract metadata from video files

    def extract(self) -> Dict[str, Any]:
        # Extract video metadata
        metadata = {}

        # Try ffprobe first
        ffprobe_data = self._extract_with_ffprobe()
        if ffprobe_data:
            metadata.update(ffprobe_data)
        else:
            metadata["Note"] = "FFmpeg not available - limited metadata"

        return metadata
    
    def _extract_with_ffprobe(self) -> Dict[str, Any]:
        # Extract metadata using ffprobe

        metadata = {}

        try:
            # Run ffprobe command
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                str(self.file_path)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                data = json.loads(result.stdout)

                # Extract format info
                if 'format' in data:
                    fmt = data['format']
                    metadata["Format Name"] = fmt.get('format_long_name', 'Unknown')
                    metadata["Format"] = fmt.get('format_name', 'Unknown')

                    if 'duration' in fmt:
                        metadata["Duration"] = float(fmt['duration'])

                    if 'size' in fmt:
                        metadata["Stream Size"] = int(fmt['size'])

                    if 'bit_rate' in fmt:
                        metadata["Overall Bitrate"] = int(fmt['bit_rate'])

                    # Extract tags
                    if 'tags' in fmt:
                        for key, value in fmt['tags'].items():
                            metadata[f"Tag {key.title()}"] = value

                # Extract stream information
                if 'streams' in data:
                    video_streams = [s for s in data['streams'] if s.get('codec_type') == 'video']
                    audio_streams = [s for s in data['streams'] if s.get('codec_type') == 'audio']
                    subtitle_streams = [s for s in data['streams'] if s.get('codec_type') == 'subtitle']

                    metadata["Video Streams"] = len(video_streams)
                    metadata["Audio Streams"] = len(audio_streams)
                    metadata["Subtitle Streams"] = len(subtitle_streams)

                    # Extract video stream info
                    for idx, stream in enumerate(video_streams):
                        prefix = f"Video Stream {idx + 1}" if len(video_streams) > 1 else "Video"

                        metadata[f"{prefix} Codec"] = stream.get('codec_long_name', 'Unknown')
                        metadata[f"{prefix} Codec Name"] = stream.get('codec_name', 'Unknown')

                        if 'width' in stream and 'height' in stream:
                            width = stream['width']
                            height = stream['height']
                            metadata[f"{prefix} Resolution"] = f"{width} x {height}"
                            metadata[f"{prefix} Width"] = width
                            metadata[f"{prefix} Height"] = height

                            # Aspect ratio calculation
                            from math import gcd
                            divisor = gcd(width, height)
                            metadata[f"{prefix} Aspect Ratio"] = f"{width // divisor}:{height // divisor}"

                        if 'bit_rate' in stream:
                            metadata[f"{prefix} Bitrate"] = int(stream['bit_rate'])

                        if 'avg_frame_rate' in stream:
                            fps_str = stream['avg_frame_rate']
                            if '/' in fps_str:
                                num, den = map(float, fps_str.split('/'))
                                if den != 0:
                                    metadata[f"{prefix} FPS"] = f"{num / den:.2f}"

                        if 'pix_fmt' in stream:
                            metadata[f"{prefix} Pixel Format"] = stream['pix_fmt']

                        if 'color_space' in stream:
                            metadata[f"{prefix} Color Space"] = stream['color_space']

                        if 'nb_frames' in stream:
                            metadata[f"{prefix} Frame Count"] = int(stream['nb_frames'])

                    # Extract audio stream info
                    for idx, stream in enumerate(audio_streams):
                        prefix = f"Audio Stream {idx + 1}" if len(audio_streams) > 1 else "Audio"

                        metadata[f"{prefix} Codec"] = stream.get('codec_long_name', 'Unknown')
                        metadata[f"{prefix} Codec Name"] = stream.get('codec_name', 'Unknown')

                        if 'sample_rate' in stream:
                            metadata[f"{prefix} Sample Rate"] = f"{stream['sample_rate']} Hz"

                        if 'channels' in stream:
                            metadata[f"{prefix} Channels"] = stream['channels']

                        if 'channel_layout' in stream:
                            metadata[f"{prefix} Channel Layout"] = stream['channel_layout']

                        if 'bit_rate' in stream:
                            metadata[f"{prefix} Bitrate"] = int(stream['bit_rate'])

                        if 'bits_per_sample' in stream:
                            metadata[f"{prefix} Bits Per Sample"] = stream['bits_per_sample']

        except FileNotFoundError:
            metadata["Error"] = "ffprobe not found - please install FFmpeg"
        except subprocess.TimeoutExpired:
            metadata["Error"] = "Timeout extracting metadata"
        except Exception as e:
            metadata["Error"] = f"Failed to extract metadata: {str(e)}"

        return metadata