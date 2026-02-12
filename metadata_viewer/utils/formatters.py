# Utility functions for data formatting

from datetime import datetime
from typing import Any

def format_file_size(size_bytes: int) -> str:
    # Format file size in a human readable format
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def format_duration(seconds: float) -> str:
    # Format duration in a human readable format
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours}h {minutes}m {secs}s"
    
def format_bitrate(bitrate: int) -> str:
    # Format bitrate to a human readable format
    if bitrate < 1000:
        return f"{bitrate} bps"
    elif bitrate < 1000000:
        return f"{bitrate / 1000:.2f} Kbps"
    else:
        return f"{bitrate / 1000000:.2f} Mbps"
    
def format_timestamp(timestamp: Any) -> str:
    # Format timestampts to readable dates and times
    if isinstance(timestamp, (int, float)):
        try:
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except (OSError, ValueError, OverflowError):
            return str(timestamp)
    elif isinstance(timestamp, str):
        return timestamp
    return "Unknown"

def format_resolution(width: int, height: int) -> str:
    # Format resolution
    return f"{width} x {height}"

def format_aspect_ratio(width: int, height: int) -> str:
    # Format aspect ratio
    from math import gcd
    divisor = gcd(width, height)
    return f"{width // divisor}:{height // divisor}"

def format_metadata_value(key: str, value: Any) -> str:
    # Format the metadata value based on the key
    if value is None:
        return "N/A"
    
    key_lower = key.lower()

    if 'size' in key_lower and isinstance(value, (int, float)):
        return format_file_size(int(value))
    elif 'duration' in key_lower and isinstance(value, (int, float)):
        return format_duration(float(value))
    elif 'bitrate' in key_lower and isinstance(value, (int, float)):
        return format_bitrate(int(value))
    elif any(term in key_lower for term in ['date', 'time', 'modified', 'created']):
        return format_timestamp(value)
    elif isinstance(value, (list, tuple)):
        return ', '.join(str(v) for v in value)
    elif isinstance(value, dict):
        return str(value)
    else:
        return str(value)