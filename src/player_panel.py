"""Player Panel Widget - Displays and plays test patterns"""

from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QSlider, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap


class PlayerPanel(QWidget):
    """Player panel for displaying images and videos"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_pattern = None
        self.current_pixmap = None
        self._init_ui()

    def _init_ui(self):
        """Initialize the player panel UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Display area (main content area)
        self.display_frame = QFrame()
        self.display_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.display_frame.setStyleSheet("background-color: #1e1e1e;")

        # Display layout (will hold QLabel for images or QVideoWidget for videos)
        display_layout = QVBoxLayout(self.display_frame)
        display_layout.setContentsMargins(0, 0, 0, 0)

        # Display label (shows images or placeholder text)
        self.display_label = QLabel("Select a pattern from the library")
        self.display_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display_label.setStyleSheet("""
            QLabel {
                color: #888;
                font-size: 18px;
                padding: 20px;
            }
        """)
        self.display_label.setScaledContents(False)  # We'll handle scaling manually
        display_layout.addWidget(self.display_label)

        layout.addWidget(self.display_frame)

        # Control panel
        self.control_panel = self._create_control_panel()
        layout.addWidget(self.control_panel)

    def _create_control_panel(self):
        """Create the playback control panel"""
        control_widget = QFrame()
        control_widget.setFrameStyle(QFrame.Shape.StyledPanel)
        control_widget.setMaximumHeight(120)
        control_widget.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border-top: 1px solid #444;
            }
        """)

        layout = QVBoxLayout(control_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Seek slider
        self.seek_slider = QSlider(Qt.Orientation.Horizontal)
        self.seek_slider.setEnabled(False)  # Disabled until Phase 6
        layout.addWidget(self.seek_slider)

        # Time display
        time_layout = QHBoxLayout()
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setStyleSheet("color: #ccc; font-size: 11px;")
        time_layout.addWidget(self.time_label)
        time_layout.addStretch()
        layout.addLayout(time_layout)

        # Playback controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        # Play/Pause button
        self.play_button = QPushButton("▶ Play")
        self.play_button.setMinimumSize(80, 35)
        self.play_button.setEnabled(False)  # Disabled until Phase 6
        self.play_button.setStyleSheet(self._get_button_style())
        controls_layout.addWidget(self.play_button)

        # Loop button
        self.loop_button = QPushButton("🔁 Loop")
        self.loop_button.setMinimumSize(80, 35)
        self.loop_button.setCheckable(True)
        self.loop_button.setChecked(True)  # Default: loop enabled
        self.loop_button.setEnabled(False)  # Disabled until Phase 7
        self.loop_button.setStyleSheet(self._get_button_style())
        controls_layout.addWidget(self.loop_button)

        controls_layout.addStretch()

        # Volume slider
        volume_layout = QHBoxLayout()
        volume_label = QLabel("🔊")
        volume_label.setStyleSheet("color: #ccc;")
        volume_layout.addWidget(volume_label)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMaximumWidth(100)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(70)
        self.volume_slider.setEnabled(False)  # Disabled until Phase 7
        volume_layout.addWidget(self.volume_slider)

        controls_layout.addLayout(volume_layout)

        # Fullscreen button
        self.fullscreen_button = QPushButton("⛶ Fullscreen")
        self.fullscreen_button.setMinimumSize(100, 35)
        self.fullscreen_button.setEnabled(False)  # Disabled until Phase 8
        self.fullscreen_button.setStyleSheet(self._get_button_style())
        controls_layout.addWidget(self.fullscreen_button)

        layout.addLayout(controls_layout)

        return control_widget

    def _get_button_style(self):
        """Get consistent button styling"""
        return """
            QPushButton {
                background-color: #3d3d3d;
                color: #fff;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton:hover:enabled {
                background-color: #4d4d4d;
                border-color: #666;
            }
            QPushButton:pressed:enabled {
                background-color: #2d2d2d;
            }
            QPushButton:disabled {
                color: #666;
                background-color: #2a2a2a;
                border-color: #444;
            }
            QPushButton:checked {
                background-color: #0078d4;
                border-color: #0078d4;
            }
        """

    def display_pattern(self, pattern):
        """
        Display a pattern (image or video)

        Args:
            pattern: Pattern object to display
        """
        if not pattern:
            self._show_placeholder("No pattern selected")
            return

        self.current_pattern = pattern

        # Check if file exists
        if not pattern.file_exists():
            self._show_placeholder(f"File not found:\n{pattern.path}")
            print(f"Error: Pattern file not found: {pattern.path}")
            return

        # Handle based on pattern type
        if pattern.is_image():
            self._display_image(pattern.path)
        elif pattern.is_video():
            # Video playback will be implemented in Phase 6
            self._show_placeholder(f"Video playback coming in Phase 6\n{pattern.name}")
            print(f"Video pattern selected: {pattern.name} (playback in Phase 6)")
        else:
            self._show_placeholder(f"Unknown pattern type:\n{pattern.type}")

    def _display_image(self, image_path):
        """
        Display an image file

        Args:
            image_path: Path to the image file
        """
        try:
            # Load the image
            pixmap = QPixmap(str(image_path))

            if pixmap.isNull():
                self._show_placeholder(f"Failed to load image:\n{image_path}")
                print(f"Error: Failed to load image: {image_path}")
                return

            # Store the original pixmap
            self.current_pixmap = pixmap

            # Scale and display
            self._update_scaled_image()

            print(f"Displaying image: {image_path} ({pixmap.width()}x{pixmap.height()})")

        except Exception as e:
            self._show_placeholder(f"Error loading image:\n{str(e)}")
            print(f"Error displaying image: {e}")

    def _update_scaled_image(self):
        """Update the displayed image with proper scaling"""
        if not self.current_pixmap:
            return

        # Get available size (subtract some margin)
        available_size = self.display_frame.size()
        available_size.setWidth(available_size.width() - 20)
        available_size.setHeight(available_size.height() - 20)

        # Scale pixmap to fit while maintaining aspect ratio
        scaled_pixmap = self.current_pixmap.scaled(
            available_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        # Display the scaled image
        self.display_label.setPixmap(scaled_pixmap)
        self.display_label.setText("")  # Clear any placeholder text

    def _show_placeholder(self, message):
        """
        Show a placeholder message

        Args:
            message: Message to display
        """
        self.current_pixmap = None
        self.display_label.setPixmap(QPixmap())  # Clear any image
        self.display_label.setText(message)

    def resizeEvent(self, event):
        """Handle resize events to rescale the image"""
        super().resizeEvent(event)

        # Rescale the current image if one is displayed
        if self.current_pixmap:
            self._update_scaled_image()

    def clear_display(self):
        """Clear the display and show placeholder"""
        self.current_pattern = None
        self.current_pixmap = None
        self._show_placeholder("Select a pattern from the library")
