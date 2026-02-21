# Image metadata extractor

from pathlib import Path
from typing import Dict, Any
from .base_extractor import BaseExtractor

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import exifread
    EXIFREAD_AVAILABLE = True
except ImportError:
    EXIFREAD_AVAILABLE = False


class ImageExtractor(BaseExtractor):
    # Extract metadata from image files

    def extract(self) -> Dict[str, Any]:
        metadata = {}

        if not PIL_AVAILABLE:
            metadata["Error"] = "PIL/Pillow not available"
            return metadata
        
        try:
            with Image.open(self.file_path) as img:
                # Basic image info
                metadata["Format"] = img.format
                metadata["Mode"] = img.mode
                metadata["Width"] = img.width
                metadata["Height"] = img.height
                metadata["Resolution"] = f"{img.width} x {img.height}"

                # Calculate MP
                megapixels = (img.width * img.height) / 1_000_000
                metadata["Megapixels"] = f"{megapixels:.2f} MP"

                # Get DPI if available
                if hasattr(img, 'info') and 'dpi' in img.info:
                    metadata["DPI"] = f"{img.info['dpi'][0]} x {img.info['dpi'][1]}"

                # Color palette info
                if img.mode == 'P':
                    metadata["Palette"] = f"{len(img.getpalette()) // 3} colors"

                # Extract EXIF data
                exif_data = self._extract_exif(img)
                if exif_data:
                    metadata.update(exif_data)

        except Exception as e:
            metadata["Error"] = f"Failed to extract metadata: {str(e)}"

        return metadata
    
    def _extract_exif(self, img: 'Image.Image') -> Dict[str, Any]:
        # Extract EXIF data from an image
        exif_data = {}

        try:
            exif = img.getexif()
            if exif:
                gps_found = False

                for tag_id, value in exif.items():
                    tag = TAGS.get(tag_id, tag_id)

                    # Handle GPS data
                    if tag == "GPSInfo":
                        gps_found = True
                        gps_data = self._extract_gps(value)
                        exif_data.update(gps_data)
                    else:
                        # Bytes to string conversion
                        if isinstance(value, bytes):
                            try:
                                value = value.decode('utf-8', errors='ignore')
                            except Exception:
                                value = str(value)

                        exif_data[f"EXIF {tag}"] = value

                # EXIF exists, but no GPS tags found
                if not gps_found:
                    exif_data["GPS Info"] = "No GPS data found"
            else:
                # No EXIF data at all
                exif_data["EXIF Info"] = "No EXIF data found"

        except Exception as e:
            exif_data["EXIF Error"] = str(e)

        return exif_data
    
    def _extract_gps(self, gps_info: Dict) -> Dict[str, Any]:
        # Extract GPS data from the EXIF info
        gps_data = {}

        try:
            for key in gps_info.keys():
                tag = GPSTAGS.get(key, key)
                gps_data[f"GPS {tag}"] = gps_info[key]

            # Calculate latitude and longitude if they're available
            if 1 in gps_info and 2 in gps_info and 3 in gps_info and 4 in gps_info:
                lat = self._convert_to_degrees(gps_info[2])
                lon = self._convert_to_degrees(gps_info[4])

                if gps_info[1] == 'S':
                    lat = -lat
                if gps_info[3] == 'W':
                    lon = -lon

                gps_data["GPS Latitude"] = f"{lat:.6f}"
                gps_data["GPS Longitude"] = f"{lon:.6f}"
                gps_data["GPS Coordinates"] = f"{lat:.6f}, {lon:.6f}"

        except Exception as e:
            gps_data["GPS Error"] = str(e)

        return gps_data
    
    @staticmethod
    def _convert_to_degrees(value):
        # Convert GPS coordinates to degrees
        d, m, s = value
        return float(d) + float(m) / 60.0 + float(s) / 3600.0

