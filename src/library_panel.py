"""Library Panel Widget - Displays test pattern catalog"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QLineEdit, QLabel
)
from PySide6.QtCore import Qt, Signal


class LibraryPanel(QWidget):
    """Library panel showing available test patterns"""

    # Signal emitted when a pattern is selected
    pattern_selected = Signal(object)  # Will emit pattern object in Phase 3

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        """Initialize the library panel UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Title label
        title = QLabel("Pattern Library")
        title.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        layout.addWidget(title)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search patterns...")
        self.search_bar.setClearButtonEnabled(True)
        layout.addWidget(self.search_bar)

        # Pattern list
        self.pattern_list = QListWidget()
        self.pattern_list.setAlternatingRowColors(True)
        self.pattern_list.setSpacing(2)
        layout.addWidget(self.pattern_list)

        # Add placeholder items for Phase 2 visualization
        placeholder_items = [
            "SMPTE Color Bars",
            "EBU Color Bars",
            "Grayscale Ramp",
            "Grid Pattern",
            "Black Frame",
            "White Frame"
        ]
        for item_text in placeholder_items:
            self.pattern_list.addItem(f"📊 {item_text}")

        # Add Pattern button
        self.add_button = QPushButton("+ Add Pattern")
        self.add_button.setMinimumHeight(35)
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 3px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        layout.addWidget(self.add_button)

        # Connect signals (functionality will be implemented in later phases)
        self.pattern_list.currentRowChanged.connect(self._on_selection_changed)
        # Add button will be connected in Phase 5

    def _on_selection_changed(self, current_row):
        """Handle pattern selection change"""
        # Placeholder for Phase 3 - will emit signal with pattern object
        if current_row >= 0:
            item = self.pattern_list.item(current_row)
            print(f"Selected: {item.text()}")  # Debug output for Phase 2
