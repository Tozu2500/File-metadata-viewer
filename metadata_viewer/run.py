# Launcher script for the metadata viewer

# Checks dependencies and launches the app

import sys
import subprocess
from pathlib import Path


def check_dependencies():
    # Check all the required dependencies
    required_modules = {
        'PyQt6': 'PyQt6',
        'PIL': 'Pillow',
        'mutagen': 'mutagen',
        'PyPDF2': 'PyPDF2',
    }

    missing = []

    for module, package in required_modules.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    return missing

def install_dependencies(packages):
    # Try installing the possible missing dependencies

    print("\nMissing dependencies: ")
    for pkg in packages:
        print(f"  - {pkg}")

    res = input("\nWould you like to install them now? (y/n): ")

    if res.lower() == 'y':
        print("\nInstalling dependencies...")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install'
            ] + packages)
            print("\nDependencies installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("\nFailed to install dependencies.")
            print("Please run: pip install -r requirements.txt in the terminal")
            return False
        
    else:
        print("\nPlease install dependencies manually:")
        print("  pip install -r requirements.txt")
        return False
    
def main():
    # Main launcher function
    print("=" * 60)
    print("Python Metadata Viewer Launcher")
    print("=" * 60)

    print("\nChecking dependencies...")
    missing = check_dependencies()

    if missing:
        if not install_dependencies(missing):
            return 1
    else:
        print("All dependencies found!")

    # Launch app
    print("\nLaunching application...")
    try:
        from ui.main_window import MainWindow
        from PyQt6.QtWidgets import QApplication

        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()

        return app.exec()
    except Exception as e:
        print(f"\nError launching application: {e}")
        print("\nMake sure all the dependencies are installed from 'requirements.txt'")
        print("  pip install -r requirements.txt")
        return 1
    
if __name__ == "__main__":
    sys.exit(main())