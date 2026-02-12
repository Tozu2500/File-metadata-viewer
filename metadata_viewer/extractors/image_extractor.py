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
                for tag_id, value in exif.items():
                    tag = TAGS.get(tag_id, tag_id)

                    # Handle GPS data
                    if tag == "GPSInfo":
                        gps_data = self._extract_gps(value)
                        exif_data.update(gps_data)
                    else:
                        # Convert bytes to string
                        if isinstance(value, bytes):
                            try:
                                value = value.decode('utf-8', errors='ignore')
                            except Exception:
                                value = str(value)

                        exif_data[f"EXIF {tag}"] = value
        except Exception as e:
            exif_data["EXIF Error"] = str(e)

        return exif_data
    
    