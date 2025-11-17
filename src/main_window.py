"""
Main Window - Primary application window
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QSplitter
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence, QShortcut

from .library_panel import LibraryPanel
from .player_panel import PlayerPanel
from .pattern_manager import PatternManager
from .utils import init_builtin_patterns


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Pattern Player")
        self.setMinimumSize(1024, 768)

        # Initialize pattern manager
        self.pattern_manager = PatternManager()

        # Generate built-in patterns if needed
        init_builtin_patterns(self.pattern_manager)

        # Initialize UI
        self._init_ui()
        self._create_menu_bar()
        self._setup_shortcuts()

        # Load saved preferences
        self._load_preferences()

    def _init_ui(self):
        """Initialize the user interface"""
        # Create central widget with splitter layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create horizontal splitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # Create library panel (left side - 30%)
        self.library_panel = LibraryPanel(pattern_manager=self.pattern_manager)
        self.splitter.addWidget(self.library_panel)

        # Create player panel (right side - 70%)
        self.player_panel = PlayerPanel()
        self.splitter.addWidget(self.player_panel)

        # Connect library selection to player panel (ready for Phase 4)
        self.library_panel.pattern_selected.connect(self._on_pattern_selected)

        # Set initial splitter sizes (30% / 70%)
        self.splitter.setSizes([300, 700])
        self.splitter.setStretchFactor(0, 3)  # Library panel
        self.splitter.setStretchFactor(1, 7)  # Player panel

        # Set splitter as central widget's content
        from PySide6.QtWidgets import QVBoxLayout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.splitter)

    def _create_menu_bar(self):
        """Create the application menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("&View")

        # Library menu
        library_menu = menubar.addMenu("&Library")

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        help_menu.addAction(about_action)

    def _on_pattern_selected(self, pattern):
        """Handle pattern selection from library"""
        print(f"Pattern selected: {pattern.name} ({pattern.type})")
        # Display the pattern in the player panel
        self.player_panel.display_pattern(pattern)

    def _setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Space: Play/Pause
        play_pause_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Space), self)
        play_pause_shortcut.activated.connect(self._on_play_pause_shortcut)

        # L: Toggle loop
        loop_shortcut = QShortcut(QKeySequence(Qt.Key.Key_L), self)
        loop_shortcut.activated.connect(self._on_loop_shortcut)

        # F or F11: Fullscreen (will be implemented in Phase 8)
        # ESC: Exit fullscreen (will be implemented in Phase 8)

    def _on_play_pause_shortcut(self):
        """Handle Space key for play/pause"""
        # Trigger the play button click
        if self.player_panel.play_button.isEnabled():
            self.player_panel.play_button.click()

    def _on_loop_shortcut(self):
        """Handle L key for loop toggle"""
        # Toggle the loop button
        if self.player_panel.loop_button.isEnabled():
            self.player_panel.loop_button.toggle()
            # Save preference
            self._save_loop_preference()

    def _load_preferences(self):
        """Load saved preferences from pattern manager"""
        # Load loop preference (default is True)
        loop_enabled = self.pattern_manager.get_setting("default_loop", True)
        self.player_panel.set_loop_enabled(loop_enabled)
        print(f"Loaded loop preference: {loop_enabled}")

    def _save_loop_preference(self):
        """Save loop preference to pattern manager"""
        loop_enabled = self.player_panel.get_loop_enabled()
        self.pattern_manager.set_setting("default_loop", loop_enabled)
        print(f"Saved loop preference: {loop_enabled}")

    def closeEvent(self, event):
        """Handle window close event"""
        # Save loop preference before closing
        self._save_loop_preference()
        super().closeEvent(event)
