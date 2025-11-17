# Test Pattern Player

A professional cross-platform desktop application for displaying video test patterns (both still images and videos) for broadcast and video production use.

## Features

- **Professional Test Patterns**: Includes SMPTE color bars, EBU color bars, grayscale ramps, grid patterns, and more
- **Custom Pattern Support**: Add your own images and videos
- **Video Playback**: Full-featured video player with play/pause, seek, loop, and volume controls
- **Fullscreen Display**: Present patterns on any connected monitor
- **Library Management**: Organize, search, rename, and reorder your pattern collection
- **Cross-Platform**: Runs on macOS and Windows
- **Portable**: Windows version requires no installation or admin rights

## Requirements

- **Python**: 3.8 or higher
- **Operating Systems**: macOS 10.14+, Windows 11
- **Dependencies**: See `requirements.txt`

## Installation

### macOS Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd TestPatterns
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Windows Setup

1. **Clone the repository:**
   ```cmd
   git clone <repository-url>
   cd TestPatterns
   ```

2. **Create a virtual environment:**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

## Running the Application

### Development Mode

**macOS/Linux:**
```bash
source venv/bin/activate
python main.py
```

**Windows:**
```cmd
venv\Scripts\activate
python main.py
```

## Building Executables

### macOS Build

```bash
cd build
chmod +x build_macos.sh
./build_macos.sh
```

The macOS app bundle will be created in `dist/TestPatternPlayer.app`

### Windows Build

```cmd
cd build
build_windows.bat
```

The portable Windows app will be created in `dist\TestPatternPlayer\`

## Usage

### Adding Custom Patterns

1. Click "Add Pattern" button in the Library Panel
2. Select one or more image or video files
3. Supported formats:
   - **Images**: PNG, JPEG, JPG, TIFF, BMP
   - **Videos**: MP4, MOV, MKV, AVI, WEBM

### Playing Patterns

- **Single click** a pattern in the library to display it
- **Double click** to display in fullscreen
- Use playback controls for videos (play/pause, seek, loop, volume)

### Keyboard Shortcuts

- `Space` - Play/Pause (videos)
- `F` or `F11` - Toggle fullscreen
- `L` - Toggle loop
- `ESC` - Exit fullscreen
- `Up/Down` - Navigate library
- `Delete` - Remove selected pattern
- `Ctrl/Cmd + O` - Add pattern
- `Ctrl/Cmd + Q` - Quit application

### Managing Your Library

- **Rename**: Right-click pattern → Rename
- **Delete**: Right-click pattern → Delete (or press Delete key)
- **Reorder**: Drag and drop patterns to custom positions
- **Search**: Use the search bar to filter patterns by name
- **Sort**: Library menu → Sort by Name/Type/Custom

## Project Structure

```
test-pattern-app/
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                 # Git ignore rules
├── src/                       # Source code
│   ├── main_window.py         # Main application window
│   ├── library_panel.py       # Library list widget
│   ├── player_panel.py        # Video/image player widget
│   ├── pattern_manager.py     # Pattern catalog manager
│   ├── models.py              # Data models
│   └── utils.py               # Helper functions
├── resources/                 # Application resources
│   ├── patterns/              # Preloaded test patterns
│   ├── icons/                 # UI icons
│   └── styles/                # Qt stylesheets
├── data/                      # Application data (created at runtime)
│   └── library.json           # Pattern library database
└── build/                     # Build scripts and specs
    ├── build_macos.sh         # macOS build script
    └── build_windows.bat      # Windows build script
```

## Development

### Current Status

**Phase 1: Project Foundation** ✓ Complete
- Basic project structure established
- Application launches with empty window
- Menu bar structure in place

**Phase 2: UI Layout** ✓ Complete
- Two-panel layout with QSplitter (30% / 70% split)
- Library panel with search bar, pattern list, and "Add Pattern" button
- Player panel with display area and control buttons
- Professional dark theme styling
- Resizable splitter between panels

**Phase 3: Pattern Management** ✓ Complete
- Pattern data model with UUID, metadata, and type indicators
- PatternManager with JSON persistence (data/library.json)
- Test pattern generator creating professional broadcast patterns
- 6 built-in patterns: SMPTE bars, EBU bars, grayscale, grid, black, white
- Pattern search and filtering functionality
- Library panel integration with real pattern data
- Pattern selection with signal/slot communication

**Phase 4: Image Display** ✓ Complete
- QPixmap-based image loading and display
- Automatic scaling to fit display area while maintaining aspect ratio
- Smooth transformation for high-quality scaling
- Dynamic resize handling - images rescale on window resize
- Error handling for missing/invalid files
- Placeholder messages for errors and non-image patterns
- Centered display with proper alignment

**Phase 5: User Pattern Import** ✓ Complete
- Add Pattern button with QFileDialog for selecting files
- Multiple file selection support
- File type filtering (images: PNG, JPG, TIFF, BMP; videos: MP4, MOV, MKV, AVI, WEBM)
- Automatic pattern type detection based on file extension
- Right-click context menu on patterns
- Rename pattern with input dialog
- Delete pattern with confirmation dialog (builtin patterns protected)
- Move Up/Move Down in context menu for custom ordering
- Success notification after adding patterns
- All changes persist to library.json

**Phase 6: Video Playback** ✓ Complete
- QtMultimedia integration (QMediaPlayer, QAudioOutput, QVideoWidget)
- Video widget displays in place of image label for videos
- Play/Pause button functionality with state updates
- Seek slider connected to video position with live updates
- Time display shows current position and total duration (MM:SS format)
- Volume control with slider
- Automatic playback start when video selected
- Error handling for unsupported codecs and file issues
- Clean widget swapping between images and videos

**Phase 7: Playback Controls** ✓ Complete
- Loop button functionality with toggle state
- End-of-playback detection via mediaStatusChanged signal
- Automatic video restart when loop is enabled
- Loop preference persistence (saves to settings)
- Keyboard shortcut: Space for play/pause
- Keyboard shortcut: L for loop toggle
- Loop preference loaded on application startup
- Loop state saved when application closes

**Phase 8: Fullscreen Mode** ✓ Complete
- Fullscreen toggle button in control panel
- Fullscreen mode hides library panel, control panel, and menu bar
- Window expands to full screen when entering fullscreen mode
- Keyboard shortcut: F or F11 to toggle fullscreen
- Keyboard shortcut: ESC to exit fullscreen
- Fullscreen button text updates based on state
- Signal-based communication between player panel and main window
- Fullscreen works for both images and videos

### Upcoming Phases
- **Phase 9**: Library enhancements
- **Phase 10**: Polish and build scripts

## Troubleshooting

### Application won't start
- Ensure Python 3.8+ is installed: `python --version`
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check that you're using the virtual environment

### Video won't play
- Ensure the video codec is supported by Qt Multimedia
- Try converting the video to MP4 with H.264 codec
- Check that audio output device is available

### Patterns not persisting
- Ensure the `data/` directory exists and is writable
- Check file permissions on `data/library.json`

## License

MIT License - See LICENSE file for details

## Contributing

This is a structured development project following a phased approach. Please refer to the project documentation for the development roadmap.

## Support

For issues and feature requests, please use the GitHub issue tracker.
