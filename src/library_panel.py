"""Library Panel Widget - Displays test pattern catalog"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QLineEdit, QLabel
)
from PySide6.QtCore import Qt, Signal


class LibraryPanel(QWidget):
    """Library panel showing available test patterns"""

    # Signal emitted when a pattern is selected
    pattern_selected = Signal(object)  # Emits Pattern object

    def __init__(self, pattern_manager=None, parent=None):
        super().__init__(parent)
        self.pattern_manager = pattern_manager
        self._init_ui()

        # Load patterns from manager if available
        if self.pattern_manager:
            self.load_patterns()

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

        # Connect signals
        self.pattern_list.currentRowChanged.connect(self._on_selection_changed)
        self.search_bar.textChanged.connect(self._on_search_changed)
        # Add button will be connected in Phase 5

    def load_patterns(self):
        """Load patterns from pattern manager into the list"""
        if not self.pattern_manager:
            return

        self.pattern_list.clear()
        patterns = self.pattern_manager.get_all_patterns()

        for pattern in patterns:
            self.pattern_list.addItem(pattern.get_display_name())

        print(f"Loaded {len(patterns)} patterns into library panel")

    def _on_selection_changed(self, current_row):
        """Handle pattern selection change"""
        if current_row >= 0 and self.pattern_manager:
            pattern = self.pattern_manager.get_pattern_by_index(current_row)
            if pattern:
                print(f"Selected: {pattern.name}")
                self.pattern_selected.emit(pattern)

    def _on_search_changed(self, text):
        """Handle search text change"""
        if not self.pattern_manager:
            return

        # Clear and reload based on search
        self.pattern_list.clear()

        if text.strip():
            # Search for matching patterns
            patterns = self.pattern_manager.search_patterns(text)
        else:
            # Show all patterns
            patterns = self.pattern_manager.get_all_patterns()

        for pattern in patterns:
            self.pattern_list.addItem(pattern.get_display_name())

    def refresh(self):
        """Refresh the pattern list display"""
        self.load_patterns()

    def set_pattern_manager(self, pattern_manager):
        """Set the pattern manager and load patterns"""
        self.pattern_manager = pattern_manager
        self.load_patterns()
