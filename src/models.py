"""Data Models - Pattern class and related models"""

import uuid
from dataclasses import dataclass, asdict
from typing import Optional
from pathlib import Path


@dataclass
class Pattern:
    """Model representing a test pattern (image or video)"""

    id: str
    name: str
    type: str  # 'image' or 'video'
    path: str
    custom_order: int
    is_builtin: bool
    duration: Optional[float] = None  # Duration in seconds for videos
    thumbnail_path: Optional[str] = None

    @classmethod
    def create(cls, name: str, path: str, pattern_type: str,
               custom_order: int = 0, is_builtin: bool = False,
               duration: Optional[float] = None, thumbnail_path: Optional[str] = None):
        """Create a new pattern with a generated UUID"""
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            type=pattern_type,
            path=path,
            custom_order=custom_order,
            is_builtin=is_builtin,
            duration=duration,
            thumbnail_path=thumbnail_path
        )

    @classmethod
    def from_dict(cls, data: dict):
        """Create Pattern instance from dictionary"""
        return cls(**data)

    def to_dict(self) -> dict:
        """Convert Pattern to dictionary for JSON serialization"""
        return asdict(self)

    def get_display_name(self) -> str:
        """Get formatted display name with type indicator"""
        icon = "🎬" if self.type == "video" else "📊"
        duration_str = f" ({self._format_duration()})" if self.duration else ""
        return f"{icon} {self.name}{duration_str}"

    def _format_duration(self) -> str:
        """Format duration in MM:SS format"""
        if not self.duration:
            return ""
        minutes = int(self.duration // 60)
        seconds = int(self.duration % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def file_exists(self) -> bool:
        """Check if the pattern file exists"""
        return Path(self.path).exists()

    def get_file_extension(self) -> str:
        """Get the file extension"""
        return Path(self.path).suffix.lower()

    def is_image(self) -> bool:
        """Check if pattern is an image"""
        return self.type == "image"

    def is_video(self) -> bool:
        """Check if pattern is a video"""
        return self.type == "video"
