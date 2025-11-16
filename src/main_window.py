"""
Main Window - Primary application window
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction


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
        # Create central widget with basic layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Placeholder label for Phase 1
        label = QLabel("Test Pattern Player - Phase 1")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 24px; color: #666;")
        layout.addWidget(label)

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
