"""Library Panel Widget - Displays test pattern catalog"""

from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QLineEdit, QLabel, QFileDialog,
    QMessageBox, QInputDialog, QMenu
)
from PySide6.QtCore import Qt, Signal

from .models import Pattern


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
        self.pattern_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.pattern_list.customContextMenuRequested.connect(self._show_context_menu)

        # Enable drag-and-drop reordering
        self.pattern_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.pattern_list.setDefaultDropAction(Qt.DropAction.MoveAction)

        # Connect model changed signal for drag-and-drop
        self.pattern_list.model().rowsMoved.connect(self._on_rows_moved)

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
        self.add_button.clicked.connect(self._on_add_pattern)

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

    def _on_add_pattern(self):
        """Handle Add Pattern button click"""
        if not self.pattern_manager:
            return

        # Open file dialog for selecting patterns
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Add Test Patterns")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)  # Multiple files

        # Set file filters for supported formats
        filters = (
            "All Supported Files (*.png *.jpg *.jpeg *.tiff *.bmp *.mp4 *.mov *.mkv *.avi *.webm);;"
            "Images (*.png *.jpg *.jpeg *.tiff *.bmp);;"
            "Videos (*.mp4 *.mov *.mkv *.avi *.webm);;"
            "All Files (*.*)"
        )
        file_dialog.setNameFilter(filters)

        # Show dialog and get selected files
        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            self._add_files_to_library(file_paths)

    def _add_files_to_library(self, file_paths):
        """
        Add selected files to the pattern library

        Args:
            file_paths: List of file paths to add
        """
        if not file_paths:
            return

        added_count = 0
        for file_path in file_paths:
            path = Path(file_path)

            # Determine pattern type based on extension
            ext = path.suffix.lower()
            image_exts = {'.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
            video_exts = {'.mp4', '.mov', '.mkv', '.avi', '.webm'}

            if ext in image_exts:
                pattern_type = "image"
            elif ext in video_exts:
                pattern_type = "video"
            else:
                print(f"Unsupported file type: {file_path}")
                continue

            # Create pattern with file name (without extension) as name
            pattern_name = path.stem

            # Create new pattern
            pattern = Pattern.create(
                name=pattern_name,
                path=str(path),
                pattern_type=pattern_type,
                is_builtin=False
            )

            # Add to manager
            if self.pattern_manager.add_pattern(pattern):
                added_count += 1
                print(f"Added pattern: {pattern_name} ({pattern_type})")
            else:
                print(f"Failed to add pattern: {pattern_name}")

        # Refresh the display
        if added_count > 0:
            self.refresh()
            QMessageBox.information(
                self,
                "Patterns Added",
                f"Successfully added {added_count} pattern(s) to the library."
            )

    def _show_context_menu(self, position):
        """Show context menu for pattern list"""
        # Get the item at the clicked position
        item = self.pattern_list.itemAt(position)
        if not item:
            return

        # Get the pattern index
        row = self.pattern_list.row(item)
        pattern = self.pattern_manager.get_pattern_by_index(row)
        if not pattern:
            return

        # Create context menu
        menu = QMenu(self)

        # Rename action
        rename_action = menu.addAction("Rename...")
        rename_action.triggered.connect(lambda: self._on_rename_pattern(pattern, row))

        # Delete action (only if not builtin)
        if not pattern.is_builtin:
            delete_action = menu.addAction("Delete")
            delete_action.triggered.connect(lambda: self._on_delete_pattern(pattern, row))
        else:
            # Show grayed out delete option for builtin patterns
            delete_action = menu.addAction("Delete (Built-in)")
            delete_action.setEnabled(False)

        menu.addSeparator()

        # Move up/down actions
        if row > 0:
            move_up_action = menu.addAction("Move Up")
            move_up_action.triggered.connect(lambda: self._on_move_pattern(row, row - 1))

        if row < self.pattern_list.count() - 1:
            move_down_action = menu.addAction("Move Down")
            move_down_action.triggered.connect(lambda: self._on_move_pattern(row, row + 1))

        # Show the menu at the cursor position
        menu.exec(self.pattern_list.mapToGlobal(position))

    def _on_rename_pattern(self, pattern, row):
        """
        Rename a pattern

        Args:
            pattern: Pattern object to rename
            row: Row index in the list
        """
        # Show input dialog
        new_name, ok = QInputDialog.getText(
            self,
            "Rename Pattern",
            "Enter new name:",
            QLineEdit.EchoMode.Normal,
            pattern.name
        )

        if ok and new_name.strip():
            # Update pattern name
            if self.pattern_manager.update_pattern(pattern.id, name=new_name.strip()):
                print(f"Renamed pattern: {pattern.name} -> {new_name.strip()}")
                self.refresh()
            else:
                QMessageBox.warning(
                    self,
                    "Rename Failed",
                    "Failed to rename the pattern."
                )

    def _on_delete_pattern(self, pattern, row):
        """
        Delete a pattern with confirmation

        Args:
            pattern: Pattern object to delete
            row: Row index in the list
        """
        # Don't allow deleting builtin patterns
        if pattern.is_builtin:
            QMessageBox.warning(
                self,
                "Cannot Delete",
                "Built-in patterns cannot be deleted."
            )
            return

        # Show confirmation dialog
        reply = QMessageBox.question(
            self,
            "Delete Pattern",
            f"Are you sure you want to delete '{pattern.name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Delete the pattern
            if self.pattern_manager.remove_pattern(pattern.id):
                print(f"Deleted pattern: {pattern.name}")
                self.refresh()
            else:
                QMessageBox.warning(
                    self,
                    "Delete Failed",
                    "Failed to delete the pattern."
                )

    def _on_move_pattern(self, from_row, to_row):
        """
        Move a pattern from one position to another

        Args:
            from_row: Source row index
            to_row: Destination row index
        """
        if self.pattern_manager.move_pattern(from_row, to_row):
            print(f"Moved pattern from row {from_row} to {to_row}")
            self.refresh()
            # Reselect the moved item
            self.pattern_list.setCurrentRow(to_row)
        else:
            QMessageBox.warning(
                self,
                "Move Failed",
                "Failed to move the pattern."
            )

    def _on_rows_moved(self, parent, start, end, destination, row):
        """
        Handle drag-and-drop reordering of patterns

        Args:
            parent: Parent index (unused for list)
            start: Starting row that was moved
            end: Ending row that was moved
            destination: Destination parent index
            row: Destination row
        """
        # Calculate the actual destination row
        # Qt's rowsMoved signal uses row as the position before the move
        if row > start:
            # Moving down: adjust for the removed item
            to_row = row - 1
        else:
            # Moving up: use row as-is
            to_row = row

        # Update the pattern manager
        if self.pattern_manager:
            # Move the pattern in the manager
            if self.pattern_manager.move_pattern(start, to_row):
                print(f"Drag-drop moved pattern from row {start} to {to_row}")
            else:
                print(f"Failed to update pattern order after drag-drop")

    def sort_by_name(self):
        """Sort patterns alphabetically by name"""
        if self.pattern_manager:
            self.pattern_manager.sort_patterns("name")
            self.refresh()
            print("Sorted patterns by name")

    def sort_by_type(self):
        """Sort patterns by type (images, then videos)"""
        if self.pattern_manager:
            self.pattern_manager.sort_patterns("type")
            self.refresh()
            print("Sorted patterns by type")

    def sort_by_custom(self):
        """Sort patterns by custom order"""
        if self.pattern_manager:
            self.pattern_manager.sort_patterns("custom")
            self.refresh()
            print("Sorted patterns by custom order")
