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

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()