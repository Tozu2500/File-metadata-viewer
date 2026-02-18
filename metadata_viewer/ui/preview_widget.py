# Preview widget for images and videos

from pathlib import Path
from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from utils.constants import MAX_PREVIEW_WIDTH, MAX_PREVIEW_HEIGHT
from core.file_handler import FileHandler
from ui.styles import (
    get_title_style, get_muted_text_style, get_preview_style,
    get_preview_video_style
)


class PreviewWidget(QWidget):
    # Widget for previewing images and videos

    def __init__(self, parent=None):
        # Initialize the preview widget

        super().__init__(parent)
        self.current_file: Optional[Path] = None
        self.init_ui()

    def init_ui(self):
        # Init UI
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Title
        self.title = QLabel("Preview")
        self.title.setStyleSheet(get_title_style())
        layout.addWidget(self.title)

        # Scroll area for preview
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Preview label
        self.preview_label = QLabel("No preview available")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet(get_preview_style())
        self.preview_label.setMinimumSize(400, 300)

        scroll.setWidget(self.preview_label)
        layout.addWidget(scroll)

        # Info label
        self.info_label = QLabel("")
        self.info_label.setStyleSheet(get_muted_text_style())
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)

    def apply_theme(self):
        # Re apply theme aware styles
        self.title.setStyleSheet(get_title_style())
        self.info_label.setStyleSheet(get_muted_text_style())

        # Re-Apply preview style only if no image is shown
        if self.preview_label.pixmap() is None or self.preview_label.pixmap().isNull():
            self.preview_label.setStyleSheet(get_preview_style())

    def preview_file(self, file_path: Path):
        # Preview a file
        self.current_file = file_path
        file_type = FileHandler.get_file_type(file_path)

        if file_type == 'image':
            self._preview_image(file_path)
        elif file_type == 'video':
            self._preview_video(file_path)
        else:
            self._show_no_preview(file_type)

    def _preview_image(self, file_path: Path):
        # Preview an image file
        try:
            # Load image
            pixmap = QPixmap(str(file_path))

            if pixmap.isNull():
                self.info_label.setText("Failed to load image")
                return
            
            # Scale image to fit properly
            scaled_pixmap = pixmap.scaled(
                MAX_PREVIEW_WIDTH,
                MAX_PREVIEW_HEIGHT,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            self.preview_label.setPixmap(scaled_pixmap)
            self.preview_label.setStyleSheet("")  # Bg removal

            # Update info
            self.info_label.setText(
                f"Image: {pixmap.width()} x {pixmap.height()} pixels"
            )

        except Exception as e:
            self.info_label.setText(f"Error loading image: {str(e)}")
            self._show_no_preview("image")

    def _preview_video(self, file_path: Path):
        # Show video info (TODO: actual playback full implementation (QMediaPlayer) )
        # This is a placeholder for basic info showing
        self.preview_label.setText(f"Video File\n\n{file_path.name}")
        self.preview_label.setStyleSheet(get_preview_video_style())
        self.info_label.setText("Video preview not implemented - view metadata for details")

    def _show_no_preview(self, file_type: str):
        # Show no preview msg

        icon_map = {
            'audio': '🎵',
            'document': '📄',
            'video': '🎬',
            'image': '🖼️'
        }

        icon = icon_map.get(file_type, '📁')
        type_name = file_type.title() if file_type != 'unknown' else 'File'

        self.preview_label.setPixmap(QPixmap())  # Clear existing pixmap
        self.preview_label.setText(f"{icon} {type_name}\n\nNo preview available")
        self.preview_label.setStyleSheet(get_preview_video_style())
        self.info_label.setText(f"Preview not supported for {type_name.lower()} files")

    def clear(self):
        # Clear preview
        self.current_file = None
        self.preview_label.setPixmap(QPixmap())
        self.preview_label.setText("No preview available")
        self.preview_label.setStyleSheet(get_preview_style())
        self.info_label.setText("")