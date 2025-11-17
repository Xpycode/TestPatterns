class TestPatternsPlayer {
    constructor() {
        // DOM elements
        this.videoPlayer = document.getElementById('videoPlayer');
        this.imagePlayer = document.getElementById('imagePlayer');
        this.placeholder = document.getElementById('placeholder');
        this.playlistItems = document.getElementById('playlistItems');
        this.currentItemDisplay = document.getElementById('currentItemDisplay');

        // Controls
        this.playBtn = document.getElementById('playBtn');
        this.pauseBtn = document.getElementById('pauseBtn');
        this.nextBtn = document.getElementById('nextBtn');
        this.prevBtn = document.getElementById('prevBtn');
        this.addToPlaylistBtn = document.getElementById('addToPlaylist');
        this.clearPlaylistBtn = document.getElementById('clearPlaylist');

        // Inputs
        this.mediaUrlInput = document.getElementById('mediaUrl');
        this.mediaTypeSelect = document.getElementById('mediaType');
        this.imageDurationInput = document.getElementById('imageDuration');
        this.autoLoopCheckbox = document.getElementById('autoLoop');
        this.autoPlayCheckbox = document.getElementById('autoPlay');

        // State
        this.playlist = [];
        this.currentIndex = -1;
        this.isPlaying = false;
        this.imageTimer = null;

        this.init();
    }

    init() {
        // Load saved settings and playlist
        this.loadFromStorage();

        // Bind events
        this.playBtn.addEventListener('click', () => this.play());
        this.pauseBtn.addEventListener('click', () => this.pause());
        this.nextBtn.addEventListener('click', () => this.next());
        this.prevBtn.addEventListener('click', () => this.previous());
        this.addToPlaylistBtn.addEventListener('click', () => this.addToPlaylist());
        this.clearPlaylistBtn.addEventListener('click', () => this.clearPlaylist());

        // Settings events
        this.imageDurationInput.addEventListener('change', () => this.saveToStorage());
        this.autoLoopCheckbox.addEventListener('change', () => this.saveToStorage());
        this.autoPlayCheckbox.addEventListener('change', () => this.saveToStorage());

        // Video events
        this.videoPlayer.addEventListener('ended', () => this.onMediaEnded());
        this.videoPlayer.addEventListener('error', (e) => this.onMediaError(e));

        // Image events
        this.imagePlayer.addEventListener('error', (e) => this.onMediaError(e));

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));

        // Enter key on URL input
        this.mediaUrlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.addToPlaylist();
            }
        });

        this.renderPlaylist();

        // Auto-play if enabled and playlist has items
        if (this.autoPlayCheckbox.checked && this.playlist.length > 0) {
            setTimeout(() => this.play(), 500);
        }
    }

    addToPlaylist() {
        const url = this.mediaUrlInput.value.trim();
        if (!url) {
            alert('Please enter a URL');
            return;
        }

        let type = this.mediaTypeSelect.value;
        if (type === 'auto') {
            type = this.detectMediaType(url);
        }

        const item = {
            id: Date.now(),
            url: url,
            type: type
        };

        this.playlist.push(item);
        this.mediaUrlInput.value = '';
        this.renderPlaylist();
        this.saveToStorage();

        // Auto-play if this is the first item and autoplay is enabled
        if (this.playlist.length === 1 && this.autoPlayCheckbox.checked && !this.isPlaying) {
            setTimeout(() => this.play(), 300);
        }
    }

    detectMediaType(url) {
        const videoExtensions = ['.mp4', '.webm', '.ogg', '.mov', '.avi', '.mkv'];
        const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'];

        const urlLower = url.toLowerCase();

        for (const ext of videoExtensions) {
            if (urlLower.includes(ext)) return 'video';
        }

        for (const ext of imageExtensions) {
            if (urlLower.includes(ext)) return 'image';
        }

        // Default to video for streaming URLs (YouTube, etc.)
        if (urlLower.includes('youtube') || urlLower.includes('vimeo')) {
            return 'video';
        }

        // Default to image
        return 'image';
    }

    removeFromPlaylist(id) {
        const index = this.playlist.findIndex(item => item.id === id);
        if (index === -1) return;

        // If removing current item, stop playback
        if (index === this.currentIndex) {
            this.pause();
            this.currentIndex = -1;
        } else if (index < this.currentIndex) {
            // Adjust current index if removing item before it
            this.currentIndex--;
        }

        this.playlist.splice(index, 1);
        this.renderPlaylist();
        this.saveToStorage();
    }

    moveItem(id, direction) {
        const index = this.playlist.findIndex(item => item.id === id);
        if (index === -1) return;

        const newIndex = direction === 'up' ? index - 1 : index + 1;
        if (newIndex < 0 || newIndex >= this.playlist.length) return;

        // Swap items
        [this.playlist[index], this.playlist[newIndex]] = [this.playlist[newIndex], this.playlist[index]];

        // Update current index if needed
        if (this.currentIndex === index) {
            this.currentIndex = newIndex;
        } else if (this.currentIndex === newIndex) {
            this.currentIndex = index;
        }

        this.renderPlaylist();
        this.saveToStorage();
    }

    clearPlaylist() {
        if (this.playlist.length === 0) return;

        if (confirm('Are you sure you want to clear the entire playlist?')) {
            this.pause();
            this.playlist = [];
            this.currentIndex = -1;
            this.renderPlaylist();
            this.saveToStorage();
            this.showPlaceholder();
        }
    }

    renderPlaylist() {
        if (this.playlist.length === 0) {
            this.playlistItems.innerHTML = '<p class="empty-playlist">Playlist is empty. Add items above.</p>';
            return;
        }

        this.playlistItems.innerHTML = this.playlist.map((item, index) => `
            <div class="playlist-item ${index === this.currentIndex ? 'active' : ''}" data-id="${item.id}">
                <div class="item-info">
                    <span class="item-type ${item.type}">${item.type}</span>
                    <div class="item-url" title="${item.url}">${item.url}</div>
                </div>
                <div class="item-controls">
                    ${index > 0 ? '<button onclick="player.moveItem(' + item.id + ', \'up\')">↑</button>' : ''}
                    ${index < this.playlist.length - 1 ? '<button onclick="player.moveItem(' + item.id + ', \'down\')">↓</button>' : ''}
                    <button onclick="player.playItem(' + item.id + ')">Play</button>
                    <button onclick="player.removeFromPlaylist(' + item.id + ')">Remove</button>
                </div>
            </div>
        `).join('');
    }

    playItem(id) {
        const index = this.playlist.findIndex(item => item.id === id);
        if (index === -1) return;

        this.currentIndex = index;
        this.loadCurrentItem();
        this.play();
    }

    play() {
        if (this.playlist.length === 0) {
            alert('Playlist is empty. Add items first.');
            return;
        }

        // If no item is loaded, load the first one
        if (this.currentIndex === -1) {
            this.currentIndex = 0;
            this.loadCurrentItem();
        }

        this.isPlaying = true;

        const currentItem = this.playlist[this.currentIndex];

        if (currentItem.type === 'video') {
            this.videoPlayer.play();
        } else if (currentItem.type === 'image') {
            this.startImageTimer();
        }
    }

    pause() {
        this.isPlaying = false;

        if (this.videoPlayer.style.display !== 'none') {
            this.videoPlayer.pause();
        }

        if (this.imageTimer) {
            clearTimeout(this.imageTimer);
            this.imageTimer = null;
        }
    }

    next() {
        if (this.playlist.length === 0) return;

        this.currentIndex++;

        if (this.currentIndex >= this.playlist.length) {
            if (this.autoLoopCheckbox.checked) {
                this.currentIndex = 0;
            } else {
                this.currentIndex = this.playlist.length - 1;
                this.pause();
                return;
            }
        }

        this.loadCurrentItem();

        if (this.isPlaying) {
            this.play();
        }
    }

    previous() {
        if (this.playlist.length === 0) return;

        this.currentIndex--;

        if (this.currentIndex < 0) {
            if (this.autoLoopCheckbox.checked) {
                this.currentIndex = this.playlist.length - 1;
            } else {
                this.currentIndex = 0;
            }
        }

        this.loadCurrentItem();

        if (this.isPlaying) {
            this.play();
        }
    }

    loadCurrentItem() {
        if (this.currentIndex < 0 || this.currentIndex >= this.playlist.length) {
            this.showPlaceholder();
            return;
        }

        const item = this.playlist[this.currentIndex];

        // Clear any existing timers
        if (this.imageTimer) {
            clearTimeout(this.imageTimer);
            this.imageTimer = null;
        }

        // Hide all players
        this.videoPlayer.style.display = 'none';
        this.imagePlayer.style.display = 'none';
        this.placeholder.style.display = 'none';

        if (item.type === 'video') {
            this.videoPlayer.src = item.url;
            this.videoPlayer.style.display = 'block';
            this.currentItemDisplay.textContent = `Video ${this.currentIndex + 1}/${this.playlist.length}`;
        } else if (item.type === 'image') {
            this.imagePlayer.src = item.url;
            this.imagePlayer.style.display = 'block';
            this.currentItemDisplay.textContent = `Image ${this.currentIndex + 1}/${this.playlist.length}`;
        }

        this.renderPlaylist();
    }

    showPlaceholder() {
        this.videoPlayer.style.display = 'none';
        this.imagePlayer.style.display = 'none';
        this.placeholder.style.display = 'flex';
        this.currentItemDisplay.textContent = 'No item loaded';
    }

    startImageTimer() {
        const duration = parseInt(this.imageDurationInput.value) * 1000;

        if (this.imageTimer) {
            clearTimeout(this.imageTimer);
        }

        this.imageTimer = setTimeout(() => {
            this.onMediaEnded();
        }, duration);
    }

    onMediaEnded() {
        // Auto-advance to next item
        if (this.currentIndex < this.playlist.length - 1) {
            this.next();
        } else if (this.autoLoopCheckbox.checked) {
            this.currentIndex = -1;
            this.next();
        } else {
            this.pause();
        }
    }

    onMediaError(e) {
        console.error('Media error:', e);
        alert('Error loading media. Please check the URL and try again.');
        this.pause();
    }

    handleKeyboard(e) {
        // Space bar - play/pause
        if (e.code === 'Space' && e.target.tagName !== 'INPUT') {
            e.preventDefault();
            if (this.isPlaying) {
                this.pause();
            } else {
                this.play();
            }
        }

        // Arrow right - next
        if (e.code === 'ArrowRight') {
            this.next();
        }

        // Arrow left - previous
        if (e.code === 'ArrowLeft') {
            this.previous();
        }
    }

    saveToStorage() {
        const data = {
            playlist: this.playlist,
            settings: {
                imageDuration: this.imageDurationInput.value,
                autoLoop: this.autoLoopCheckbox.checked,
                autoPlay: this.autoPlayCheckbox.checked
            }
        };

        localStorage.setItem('testPatternsData', JSON.stringify(data));
    }

    loadFromStorage() {
        const data = localStorage.getItem('testPatternsData');

        if (data) {
            try {
                const parsed = JSON.parse(data);

                if (parsed.playlist) {
                    this.playlist = parsed.playlist;
                }

                if (parsed.settings) {
                    this.imageDurationInput.value = parsed.settings.imageDuration || 5;
                    this.autoLoopCheckbox.checked = parsed.settings.autoLoop !== false;
                    this.autoPlayCheckbox.checked = parsed.settings.autoPlay !== false;
                }
            } catch (e) {
                console.error('Error loading saved data:', e);
            }
        }
    }
}

// Initialize the player
const player = new TestPatternsPlayer();
