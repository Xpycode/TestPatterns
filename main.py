#!/usr/bin/env python3
"""
Test Pattern Display Application
Professional test pattern player for broadcast and video production
"""

import sys
from PySide6.QtWidgets import QApplication
from src.main_window import MainWindow


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Test Pattern Player")
    app.setOrganizationName("TestPatternApp")
    app.setApplicationVersion("1.0.0")

    # Create and show main window
    window = MainWindow()
    window.show()

    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
