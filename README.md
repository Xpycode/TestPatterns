# TestPatterns

Display of test patterns in video and image form with playlist functionality.

## Features

- **Playlist Management**: Add, remove, and reorder test pattern videos and images
- **Auto-playback**: Videos play through their full duration automatically
- **Configurable Image Duration**: Set how long images display (manually configurable in seconds)
- **Settings Panel**: Configure playback behavior, image duration, and looping
- **Keyboard Shortcuts**: Control playback with keyboard
- **Persistent Storage**: Playlist and settings saved automatically

## Usage

### Opening the Application

Simply open `index.html` in a web browser. The application runs entirely in the browser with no server required.

### Adding Items to Playlist

1. Enter a video or image URL in the input field
2. Select media type (or leave as "Auto-detect")
3. Click "Add" or press Enter
4. The item will appear in the playlist

See `samples/example-urls.md` for example test pattern URLs you can use.

### Playback Controls

**Button Controls:**
- **Play**: Start playback
- **Pause**: Pause playback
- **Next**: Skip to next item
- **Previous**: Go to previous item

**Keyboard Shortcuts:**
- `Space`: Play/Pause
- `Right Arrow`: Next item
- `Left Arrow`: Previous item

### Settings

**Image Duration**: Set how long images display before auto-advancing (1-300 seconds)

**Loop Playlist**: When enabled, playlist will restart from the beginning after the last item

**Auto-play on Load**: When enabled, playlist starts automatically when page loads

**Clear Playlist**: Remove all items from the playlist

### Playlist Management

- **Play**: Click "Play" button on any item to jump to it
- **Reorder**: Use up/down arrows to reorder items
- **Remove**: Click "Remove" to delete an item
- **Active Item**: Currently playing item is highlighted

## How It Works

### Videos
- Videos play through their entire duration automatically
- When a video ends, the playlist advances to the next item
- Native browser video player controls are available

### Images
- Images display for the duration specified in Settings
- After the timer expires, the playlist advances to the next item
- Duration can be changed at any time in the Settings panel

### Auto-advance
- After each item completes (video ends or image timer expires), the playlist automatically moves to the next item
- When the last item finishes:
  - If "Loop Playlist" is enabled: restarts from the beginning
  - If "Loop Playlist" is disabled: playback stops

## Technical Details

- Pure HTML, CSS, and JavaScript (no dependencies)
- Uses localStorage to persist playlist and settings
- Responsive design works on desktop and mobile
- Supports common video formats: MP4, WebM, OGG, MOV
- Supports common image formats: JPG, PNG, GIF, WebP, SVG

## Files

- `index.html` - Main application structure
- `style.css` - Styling and layout
- `app.js` - Playlist logic and playback control
- `samples/example-urls.md` - Example test pattern URLs
