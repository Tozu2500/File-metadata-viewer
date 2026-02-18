# Main app window

from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QStatusBar, QMenuBar, QFileDialog,
    QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QActionGroup
from ui.file_browser import FileBrowser
from ui.metadata_display import MetadataDisplay
from ui.preview_widget import PreviewWidget
from ui.styles import (
    get_stylesheet, Theme, get_current_theme, set_current_theme
)
from core.metadata_extractor import MetadataExtractor
from utils.constants import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, SPLITTER_SIZES


class MainWindow(QMainWindow):
    # Main application window

    def __init__(self):
        # Initialize the main window
        super().__init__()
        self.metadata_extractor = MetadataExtractor()
        self.init_ui()

    def init_ui(self):
        # Initialize the user interface
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Apply the stylesheet
        self.setStyleSheet(get_stylesheet())

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Creating the main splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel - File browser
        self.file_browser = FileBrowser()
        self.file_browser.file_selected.connect(self.on_file_selected)
        splitter.addWidget(self.file_browser)

        # Right panel - Vertical splitter for preview and metadata
        right_splitter = QSplitter(Qt.Orientation.Vertical)

        # Preview widget
        self.preview_widget = PreviewWidget()
        right_splitter.addWidget(self.preview_widget)

        # Metadata display
        self.metadata_display = MetadataDisplay()
        right_splitter.addWidget(self.metadata_display)

        # Set sizes for right splitter
        right_splitter.setSizes([400, 500])

        splitter.addWidget(right_splitter)

        # Set splitter sizes
        splitter.setSizes(SPLITTER_SIZES)

        main_layout.addWidget(splitter)

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Create menu bar (After metadata_display is created)
        self.create_menu_bar()

    def create_menu_bar(self):
        # Create the menubar
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        open_action = QAction("Open File...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        open_folder_action = QAction("Open Folder...", self)
        open_folder_action.setShortcut("Ctrl+Shift+O")
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)

        file_menu.addSeparator()

        export_action = QAction("Export Metadata...", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.metadata_display.export_metadata)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("View")

        refresh_action = QAction("Refresh", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.refresh_view)
        view_menu.addAction(refresh_action)

        view_menu.addSeparator()

        # Theme submenu
        theme_menu = view_menu.addMenu("Theme")
        theme_group = QActionGroup(self)
        theme_group.setExclusive(True)

        light_action = QAction("Light", self, checkable=True)
        light_action.setChecked(get_current_theme() == Theme.LIGHT)
        light_action.triggered.connect(lambda: self.apply_theme(Theme.LIGHT))
        theme_group.addAction(light_action)
        theme_menu.addAction(light_action)

        dark_action = QAction("Dark", self, checkable=True)
        dark_action.setChecked(get_current_theme() == Theme.DARK)
        dark_action.triggered.connect(lambda: self.apply_theme(Theme.DARK))
        theme_group.addAction(dark_action)
        theme_menu.addAction(dark_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
