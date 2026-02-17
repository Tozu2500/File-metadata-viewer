# Metadata display widget

from typing import Dict, Any, Optional
from pathlib import Path
import json
import csv
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QHeaderView, QPushButton, QHBoxLayout, QFileDialog
)
from PyQt6.QtCore import Qt
from utils.formatters import format_metadata_value
from ui.styles import get_title_style, get_muted_text_style, get_file_label_style


class MetadataDisplay(QWidget):
    # Widget for metadata displayment

    def __init__(self, parent=None):
        # Initialize display

        super().__init__(parent)
        self.current_metadata: Optional[Dict[str, Any]] = None
        self.current_file: Optional[Path] = None
        self.init_ui()

    def init_ui(self):
        # Initialize UI
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Header
        header_layout = QHBoxLayout()

        self.title = QLabel("Metadata")
        self.title.setStyleSheet(get_title_style())
        header_layout.addWidget(self.title)

        header_layout.addStretch()

        # Export button
        self.export_button = QPushButton("Export")
        self.export_button.setMaximumWidth(100)
        self.export_button.clicked.connect(self.export_metadata)
        self.export_button.setEnabled(False)
        header_layout.addWidget(self.export_button)

        layout.addLayout(header_layout)

        # File info label
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet(get_file_label_style())
        self.file_label.setWordWrap(True)
        layout.addWidget(self.file_label)

        # Metadata table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Property", "Value"])

        # Config table
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        layout.addWidget(self.table)

        # Stats label
        self.stats_label = QLabel("")
        self.stats_label.setStyleSheet(get_muted_text_style())
        layout.addWidget(self.stats_label)

    def apply_theme(self):
        # Re apply theme aware styles
        self.title.setStyleSheet(get_title_style())
        self.file_label.setStyleSheet(get_file_label_style())
        self.stats_label.setStyleSheet(get_muted_text_style())

    def display_metadata(self, file_path: Path, metadata: Dict[str, Any]):
        # Display metadata for file

        self.current_file = file_path
        self.current_metadata = metadata

        # Update file label
        self.file_label.setText(f"File: {file_path.name}")

        # Clear the table
        self.table.setRowCount(0)

        # Populate the table
        self.table.setRowCount(len(metadata))

        for row, (key, value) in enumerate(metadata.items()):
            # Property name
            property_item = QTableWidgetItem(str(key))
            property_item.setFlags(property_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 0, property_item)

            # Property value
            formatted_value = format_metadata_value(key, value)
            value_item = QTableWidgetItem(formatted_value)
            value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            # Color-coding certain values
            if "Error" in key:
                value_item.setForeground(Qt.GlobalColor.red)
            elif "Warning" in key:
                value_item.setForeground(Qt.GlobalColor.darkYellow)

            self.table.setItem(row, 1, value_item)

        # Update stats
        self.stats_label.setText(f"{len(metadata)} properties")

        # Enable export button
        self.export_button.setEnabled(True)

    def clear(self):
        # Clear the metadata display
        self.current_file = None
        self.current_metadata = None
        self.file_label.setText("No file selected")
        self.table.setRowCount(0)
        self.stats_label.setText("")
        self.export_button.setEnabled(False)

    def export_metadata(self):
        # Export metadata
        if not self.current_metadata or not self.current_file:
            return
        
        # Get save file name
        default_name = f"{self.current_file.stem}_metadata.txt"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Metadata",
            str(Path.home() / default_name),
            "Text Files (*.txt);;JSON Files (*.json);;CSV Files (*.csv);;All Files (*)"
        )

        if not file_path:
            return
        
        try:
            file_path = Path(file_path)

            if file_path.suffix.lower() == '.json':
                self._export_json(file_path)
            elif file_path.suffix.lower() == '.csv':
                self._export_csv(file_path)
            else:
                self._export_text(file_path)

            self.stats_label.setText(f"Exported to {file_path.name}")
        except Exception as e:
            self.stats_label.setText(f"Export failed: {str(e)}")

    def _export_text(self, file_path: Path):
        # Export metadata to a text file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"Metadata for: {self.current_file}\n")
            f.write("=" * 80 + "\n\n")

            for key, value in self.current_metadata.items():
                formatted_value = format_metadata_value(key, value)
                f.write(f"{key}: {formatted_value}\n")

    def _export_json(self, file_path: Path):
        # Export metadata to a JSON File

        # Convert metadata to a JSON-serializable format
        serializable_metadata = {}
        for key, value in self.current_metadata.items():
            formatted_value = format_metadata_value(key, value)
            serializable_metadata[key] = formatted_value

        data = {
            "file": str(self.current_file),
            "metadata": serializable_metadata
        }

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def _export_csv(self, file_path: Path):
        # Export metadata to a CSV file
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Property', 'Value'])

            for key, value in self.current_metadata.items():
                formatted_value = format_metadata_value(key, value)
                writer.writerow([key, formatted_value])