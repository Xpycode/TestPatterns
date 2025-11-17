"""Player Panel Widget - Displays and plays test patterns"""

from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QSlider, QFrame
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget


class PlayerPanel(QWidget):
    """Player panel for displaying images and videos"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_pattern = None
        self.current_pixmap = None

        # Video playback components
        self.media_player = None
        self.audio_output = None
        self.video_widget = None
        self.is_playing_video = False

        self._init_ui()
        self._init_video_player()

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
        self.display_layout = QVBoxLayout(self.display_frame)
        self.display_layout.setContentsMargins(0, 0, 0, 0)

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
        self.display_layout.addWidget(self.display_label)

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

    def _init_video_player(self):
        """Initialize video playback components"""
        # Create media player
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

        # Create video widget (hidden initially)
        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)

        # Connect media player signals
        self.media_player.positionChanged.connect(self._on_position_changed)
        self.media_player.durationChanged.connect(self._on_duration_changed)
        self.media_player.playbackStateChanged.connect(self._on_playback_state_changed)
        self.media_player.errorOccurred.connect(self._on_media_error)

        # Connect playback controls
        self.play_button.clicked.connect(self._on_play_pause_clicked)
        self.seek_slider.sliderMoved.connect(self._on_seek_slider_moved)

        # Set default volume
        self.audio_output.setVolume(self.volume_slider.value() / 100.0)
        self.volume_slider.valueChanged.connect(self._on_volume_changed)

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
            self._display_video(pattern.path)
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
        self._stop_video()
        self._show_placeholder("Select a pattern from the library")

    def _display_video(self, video_path):
        """
        Display and play a video file

        Args:
            video_path: Path to the video file
        """
        try:
            # Stop any currently playing video
            self._stop_video()

            # Hide image label and show video widget
            self.display_label.hide()
            if self.video_widget not in [self.display_layout.itemAt(i).widget()
                                         for i in range(self.display_layout.count())]:
                self.display_layout.addWidget(self.video_widget)
            self.video_widget.show()

            # Load the video
            video_url = QUrl.fromLocalFile(str(video_path))
            self.media_player.setSource(video_url)

            # Enable video controls
            self.play_button.setEnabled(True)
            self.seek_slider.setEnabled(True)

            # Mark as playing video
            self.is_playing_video = True

            # Start playing
            self.media_player.play()

            print(f"Playing video: {video_path}")

        except Exception as e:
            self._show_placeholder(f"Error loading video:\n{str(e)}")
            print(f"Error displaying video: {e}")

    def _stop_video(self):
        """Stop video playback and cleanup"""
        if self.is_playing_video:
            self.media_player.stop()
            self.video_widget.hide()
            self.display_label.show()
            self.is_playing_video = False

            # Disable video controls
            self.play_button.setEnabled(False)
            self.seek_slider.setEnabled(False)
            self.seek_slider.setValue(0)
            self.time_label.setText("00:00 / 00:00")

    def _on_play_pause_clicked(self):
        """Handle play/pause button click"""
        if not self.is_playing_video:
            return

        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def _on_playback_state_changed(self, state):
        """Handle playback state changes"""
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.play_button.setText("⏸ Pause")
        else:
            self.play_button.setText("▶ Play")

    def _on_position_changed(self, position):
        """Handle video position change"""
        if not self.is_playing_video:
            return

        # Update seek slider (block signals to avoid feedback loop)
        self.seek_slider.blockSignals(True)
        self.seek_slider.setValue(position)
        self.seek_slider.blockSignals(False)

        # Update time display
        self._update_time_display(position, self.media_player.duration())

    def _on_duration_changed(self, duration):
        """Handle video duration change"""
        if not self.is_playing_video:
            return

        self.seek_slider.setRange(0, duration)
        self._update_time_display(self.media_player.position(), duration)

    def _on_seek_slider_moved(self, position):
        """Handle seek slider movement"""
        if self.is_playing_video:
            self.media_player.setPosition(position)

    def _on_volume_changed(self, value):
        """Handle volume slider change"""
        self.audio_output.setVolume(value / 100.0)

    def _on_media_error(self, error, error_string):
        """Handle media player errors"""
        print(f"Media error: {error_string}")
        self._show_placeholder(f"Video playback error:\n{error_string}")
        self.is_playing_video = False

    def _update_time_display(self, position, duration):
        """
        Update the time display label

        Args:
            position: Current position in milliseconds
            duration: Total duration in milliseconds
        """
        def format_time(ms):
            """Format milliseconds to MM:SS"""
            seconds = int(ms / 1000)
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{minutes:02d}:{seconds:02d}"

        current_time = format_time(position)
        total_time = format_time(duration)
        self.time_label.setText(f"{current_time} / {total_time}")
