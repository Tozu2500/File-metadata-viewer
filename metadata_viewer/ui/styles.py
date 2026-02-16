# Application styling with dark/light theme support

from enum import Enum
from typing import Dict


class Theme(Enum):
    # Main application themes
    LIGHT = "light"
    DARK = "dark"


# Theme color palettes
THEME_COLORS: Dict[Theme, Dict[str, str]] = {
    Theme.LIGHT: {
        "primary": "#2C3E50",
        "secondary": "#34495E",
        "accent": "#3498DB",
        "accent_hover": "#2980B9",
        "accent_pressed": "#21618C",
        "success": "#27AE60",
        "warning": "#F39C12",
        "danger": "#E74C3C",
        "background": "#ECF0F1",
        "surface": "#FFFFFF",
        "surface_alt": "#F7F9FA",
        "text": "#2C3E50",
        "text_secondary": "#5D6D7E",
        "text_muted": "#7F8C8D",
        "border": "#BDC3C7",
        "border_light": "#D5DBDB",
        "header_bg": "#2C3E50",
        "header_fg": "#FFFFFF",
        "table_alt_row": "#F2F4F4",
        "scrollbar_bg": "#ECF0F1",
        "scrollbar_handle": "#BDC3C7",
        "scrollbar_hover": "#95A5A6",
        "splitter": "#BDC3C7",
        "preview_bg": "#34495E",
        "preview_fg": "#FFFFFF",
        "disabled_bg": "#BDC3C7",
        "disabled_fg": "#7F8C8D",
        "menu_bg": "#FFFFFF",
        "menu_fg": "#2C3E50",
        "item_hover": "#D5DBDB",
    },
    Theme.DARK: {
        "primary": "#1A1A2E",
        "secondary": "#16213E",
        "accent": "#0F95E8",
        "accent_hover": "#1DA1F2",
        "accent_pressed": "#0D7BC5",
        "success": "#2ECC71",
        "warning": "#F1C40F",
        "danger": "#E74C3C",
        "background": "#0F0F1A",
        "surface": "#1A1A2E",
        "surface_alt": "#222240",
        "text": "#E0E0E0",
        "text_secondary": "#A0A0B0",
        "text_muted": "#707080",
        "border": "#2A2A3E",
        "border_light": "#333350",
        "header_bg": "#16213E",
        "header_fg": "#E0E0E0",
        "table_alt_row": "#1E1E32",
        "scrollbar_bg": "#0F0F1A",
        "scrollbar_handle": "#333350",
        "scrollbar_hover": "#444468",
        "splitter": "#2A2A3E",
        "preview_bg": "#16213E",
        "preview_fg": "#E0E0E0",
        "disabled_bg": "#2A2A3E",
        "disabled_fg": "#555568",
        "menu_bg": "#1A1A2E",
        "menu_fg": "#E0E0E0",
        "item_hover": "#2A2A45",
    },
}

# Current theme state
_current_theme = Theme.LIGHT

def get_current_theme() -> Theme:
    return _current_theme

def set_current_theme(theme: Theme):
    global _current_theme
    _current_theme = theme

def get_colors(theme: Theme = None) -> Dict[str, str]:
    if theme is None:
        theme = _current_theme
    return THEME_COLORS[theme]

def get_stylesheet(theme: Theme = None) -> str:
    # Get application stylesheet for the given theme

    c = get_colors(theme)

    return f"""
        QMainWindow {{
            background-color: {c['background']};
        }}

        QWidget {{
            background-color: {c['background']};
            color: {c['text']};
        }}

        QTreeView {{
            background-color: {c['surface']};
            color: {c['text']};
            border: 1px solid {c['border']};
            border-radius: 4px;
            font-size: 13px;
            padding: 5px;
            selection-background-color: {c['accent']};
            selection-color: #FFFFFF;
        }}

        QTreeView::item {{
            padding: 5px;
            color: {c['text']};
        }}

        QTreeView::item:selected {{
            background-color: {c['accent']};
            color: #FFFFFF;
        }}

        QTreeView::item:hover {{
            background-color: {c['item_hover']};
        }}

        QTableWidget {{
            background-color: {c['surface']};
            color: {c['text']};
            border: 1px solid {c['border']};
            border-radius: 4px;
            gridline-color: {c['border_light']};
            font-size: 13px;
            alternate-background-color: {c['table_alt_row']};
        }}

        QTableWidget::item {{
            padding: 8px;
            color: {c['text']};
        }}

        QTableWidget::item:selected {{
            background-color: {c['accent']};
            color: #FFFFFF;
        }}

        QHeaderView::section {{
            background-color: {c['header_bg']};
            color: {c['header_fg']};
            padding: 10px;
            border: none;
            font-weight: bold;
            font-size: 13px;
        }}

        QPushButton {{
            background-color: {c['accent']};
            color: #FFFFFF;
            border: none;
            border-radius: 4px;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: bold;
        }}

        QPushButton:hover {{
            background-color: {c['accent_hover']};
        }}

        QPushButton:pressed {{
            background-color: {c['accent_pressed']};
        }}

        QPushButton:disabled {{
            background-color: {c['disabled_bg']};
            color: {c['disabled_fg']};
        }}

        QLineEdit {{
            background-color: {c['surface']};
            color: {c['text']};
            border: 1px solid {c['border']};
            border-radius: 4px;
            padding: 8px;
            font-size: 13px;
        }}

        QLineEdit:focus {{
            border: 2px solid {c['accent']};
        }}

        QLabel {{
            color: {c['text']};
            font-size: 13px;
            background-color: transparent;
        }}

        QGroupBox {{
            background-color: {c['surface']};
            color: {c['text']};
            border: 1px solid {c['border']};
            border-radius: 4px;
            margin-top: 10px;
            padding-top: 10px;
            font-weight: bold;
        }}

        QGroupBox::title {{
            color: {c['accent']};
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 5px 10px;
        }}

        QScrollArea {{
            background-color: {c['surface']};
            border: none;
        }}

        QScrollBar:vertical {{
            background-color: {c['scrollbar_bg']};
            width: 12px;
            border-radius: 6px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {c['scrollbar_handle']};
            border-radius: 6px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {c['scrollbar_hover']};
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        QScrollBar:horizontal {{
            background-color: {c['scrollbar_bg']};
            height: 12px;
            border-radius: 6px;
        }}

        QScrollBar::handle:horizontal {{
            background-color: {c['scrollbar_handle']};
            border-radius: 6px;
            min-width: 20px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background-color: {c['scrollbar_hover']};
        }}

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}

        QStatusBar {{
            background-color: {c['header_bg']};
            color: {c['header_fg']};
            font-size: 12px;
        }}

        QStatusBar QLabel {{
            color: {c['header_fg']};
        }}

        QMenuBar {{
            background-color: {c['header_bg']};
            color: {c['header_fg']};
            padding: 5px;
        }}

        QMenuBar::item {{
            background-color: transparent;
            color: {c['header_fg']};
            padding: 5px 10px;
        }}

        QMenuBar::item:selected {{
            background-color: {c['secondary']};
        }}

        QMenu {{
            background-color: {c['menu_bg']};
            color: {c['menu_fg']};
            border: 1px solid {c['border']};
        }}

        QMenu::item {{
            padding: 8px 25px;
            color: {c['menu_fg']};
        }}

        QMenu::item:selected {{
            background-color: {c['accent']};
            color: #FFFFFF;
        }}

        QSplitter::handle {{
            background-color: {c['splitter']};
        }}

        QSplitter::handle:hover {{
            background-color: {c['accent']};
        }}
    """
