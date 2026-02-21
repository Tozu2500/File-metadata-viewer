# Main application entry point

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui.main_window import MainWindow

def main():
    # Run the app
    app = QApplication(sys.argv)
    app.setApplicationName("Python Metadata Viewer")
    app.setOrganizationName("Tozu / Tomi Louhiniitty")

    # Set app icon
    icon_path = Path(__file__).parent / "assets" / "app_icon.png"
    if icon_path.exists():
        app_icon = QIcon(str(icon_path))
        app.setWindowIcon(app_icon)

    window = MainWindow()
    window.setWindowIcon(app_icon) if icon_path.exists() else None
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

