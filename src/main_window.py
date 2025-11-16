"""
Main Window - Primary application window
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QSplitter
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from .library_panel import LibraryPanel
from .player_panel import PlayerPanel


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Pattern Player")
        self.setMinimumSize(1024, 768)

        # Initialize UI
        self._init_ui()
        self._create_menu_bar()

    def _init_ui(self):
        """Initialize the user interface"""
        # Create central widget with splitter layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create horizontal splitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # Create library panel (left side - 30%)
        self.library_panel = LibraryPanel()
        self.splitter.addWidget(self.library_panel)

        # Create player panel (right side - 70%)
        self.player_panel = PlayerPanel()
        self.splitter.addWidget(self.player_panel)

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
