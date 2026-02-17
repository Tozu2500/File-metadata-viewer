# File browser widget

from pathlib import Path
from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeView,
    QPushButton, QLineEdit, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal, QDir
from PyQt6.QtGui import QIcon, QFileSystemModel
from ui.styles import get_title_style, get_muted_text_style


class FileBrowser(QWidget):
    # Widget for browsing file paths and dirs

    file_selected = pyqtSignal(Path)

    def __init__(self, parent=None):
        # Initialize

        super().__init__(parent)
        self.current_path = Path.home()
        self.init_ui()

    def init_ui(self):
        # Initialize UI
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Title
        self.title = QLabel("File Browser")
        self.title.setStyleSheet(get_title_style())
        layout.addWidget(self.title)

        # Path navigation
        nav_layout = QHBoxLayout()

        self.path_edit = QLineEdit()
        self.path_edit.setText(str(self.current_path))
        self.path_edit.returnPressed.connect(self.navigate_to_path)
        nav_layout.addWidget(self.path_edit)

        self.home_button = QPushButton("Home")
        self.home_button.setMaximumWidth(80)
        self.home_button.clicked.connect(self.go_home)
        nav_layout.addWidget(self.home_button)

        layout.addLayout(nav_layout)

        # File system tree
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())

        # Set filters to show all the files
        self.model.setFilter(
            QDir.Filter.AllDirs |
            QDir.Filter.Files |
            QDir.Filter.NoDotAndDotDot
        )

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(str(self.current_path)))

        # Configure columns
        self.tree.setColumnWidth(0, 250)
        self.tree.hideColumn(1)
        self.tree.hideColumn(2)

        # Connect selection
        self.tree.clicked.connect(self.on_item_clicked)
        self.tree.doubleClicked.connect(self.on_item_double_clicked)

        layout.addWidget(self.tree)

        # Stats label
        self.stats_label = QLabel("Select a file to view metadata")
        self.stats_label.setStyleSheet(get_muted_text_style())
        layout.addWidget(self.stats_label)

    def apply_theme(self):
        # Re apply theme aware styles
        self.title.setStyleSheet(get_title_style())
        self.stats_label.setStyleSheet(get_muted_text_style())

    def navigate_to_path(self):
        # Navigate to the path in the line edit
        path_str = self.path_edit.text()
        path = Path(path_str)

        if path.exists() and path.is_dir():
            self.current_path = path
            self.tree.setRootIndex(self.model.index(str(path)))
            self.update_stats()
        else:
            self.path_edit.setText(str(self.current_path))

    def go_home(self):
        # Navigate to the home directory
        self.current_path = Path.home()
        self.path_edit.setText(str(self.current_path))
        self.tree.setRootIndex(self.model.index(str(self.current_path)))

    def on_item_clicked(self, index):
        # Handle item click

        path = Path(self.model.filePath(index))

        if path.is_file():
            self.file_selected.emit(path)
            self.stats_label.setText(f"Selected {path.name}")

    def on_item_double_clicked(self, index):
        # Handle item double clicks

        path = Path(self.model.filePath(index))

        if path.is_dir():
            self.current_path = path
            self.path_edit.setText(str(path))
            self.tree.setRootIndex(index)
            self.update_stats()

    def update_stats(self):
        # Update stats qlabel
        try:
            items = list(self.current_path.iterdir())
            file_count = sum(1 for item in items if item.is_file())
            dir_count = sum(1 for item in items if item.is_dir())
            self.stats_label.setText(f"{dir_count} folders, {file_count} files")
        except PermissionError:
            self.stats_label.setText("Permission was denied")

    def set_path(self, path: Path):
        # Set the current path
        if path.exists():
            if path.is_file():
                path = path.parent

            self.current_path = path
            self.path_edit.setText(str(path))
            self.tree.setRootIndex(self.model.index(str(path)))
            self.update_stats()