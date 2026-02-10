# Application wide constants and configurations

# Supported file types
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.ico', '.svg'}
VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg'}
AUDIO_EXTENSIONS = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus'}
DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'}

ALL_SUPPORTED_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS | AUDIO_EXTENSIONS | DOCUMENT_EXTENSIONS

# UI Constants
WINDOW_TITLE = "Metadata viewer 1.0"
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
SPLITTER_SIZES = [400, 1000]

# Preview settings
MAX_PREVIEW_WIDTH = 800
MAX_PREVIEW_HEIGHT = 600
THUMBNAIL_SIZE = 200

# Colors
COLOR_PRIMARY = "#2C3E50"
COLOR_SECONDARY = "#34495E"
COLOR_ACCENT = "#3498DB"
COLOR_SUCCESS = "#27AE60"
COLOR_WARNING = "#F39C12"
COLOR_DANGER = "#E74C3C"
COLOR_BACKGROUND = "#ECF0F1"
COLOR_TEXT = "#2C3E50"
COLOR_TEXT_LIGHT = "#7F8C8D"