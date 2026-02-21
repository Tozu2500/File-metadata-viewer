# Setup script

from setuptools import setup, find_packages
from pathlib import Path

readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

setup(
    name="metadata-viewer",
    version="1.0.0",
    author="Metadata Viewer Team",
    description="A comprehensive metadata viewer for images, videos, audio, and documents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "PyQt6>=6.6.0",
        "Pillow>=10.0.0",
        "mutagen>=1.47.0",
        "PyPDF2>=3.0.0",
        "exifread>=3.0.0",
    ],
    extras_require={
        "video": ["ffmpeg-python>=0.2.0"],
    },
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "metadata-viewer=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics :: Viewers",
        "Topic :: Multimedia :: Video",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)