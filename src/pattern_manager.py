"""Pattern Manager - Handles pattern catalog and persistence"""

import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any

from .models import Pattern


class PatternManager:
    """Manages the pattern library with JSON persistence"""

    def __init__(self, data_dir: str = "data", library_file: str = "library.json"):
        """
        Initialize the pattern manager

        Args:
            data_dir: Directory for storing library data
            library_file: Name of the JSON library file
        """
        self.data_dir = Path(data_dir)
        self.library_path = self.data_dir / library_file
        self.patterns: List[Pattern] = []
        self.settings: Dict[str, Any] = {
            "default_loop": True,
            "last_selected_id": None,
            "library_sort": "custom"
        }

        # Ensure data directory exists
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Load existing library or create new one
        if self.library_path.exists():
            self.load_library()
        else:
            self._create_default_library()

    def load_library(self) -> bool:
        """
        Load pattern library from JSON file

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.library_path, 'r') as f:
                data = json.load(f)

            # Load patterns
            self.patterns = [
                Pattern.from_dict(p) for p in data.get("patterns", [])
            ]

            # Load settings
            self.settings = data.get("settings", self.settings)

            print(f"Loaded {len(self.patterns)} patterns from library")
            return True

        except Exception as e:
            print(f"Error loading library: {e}")
            return False

    def save_library(self) -> bool:
        """
        Save pattern library to JSON file

        Returns:
            True if successful, False otherwise
        """
        try:
            data = {
                "version": "1.0",
                "patterns": [p.to_dict() for p in self.patterns],
                "settings": self.settings
            }

            with open(self.library_path, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"Saved {len(self.patterns)} patterns to library")
            return True

        except Exception as e:
            print(f"Error saving library: {e}")
            return False

    def _create_default_library(self):
        """Create default library with built-in patterns"""
        print("Creating default library...")
        self.patterns = []
        self.settings = {
            "default_loop": True,
            "last_selected_id": None,
            "library_sort": "custom"
        }
        # Built-in patterns will be added by the test pattern generator
        self.save_library()

    def add_pattern(self, pattern: Pattern) -> bool:
        """
        Add a pattern to the library

        Args:
            pattern: Pattern to add

        Returns:
            True if successful, False otherwise
        """
        try:
            # Set custom order to end of list
            pattern.custom_order = len(self.patterns)
            self.patterns.append(pattern)
            self.save_library()
            return True
        except Exception as e:
            print(f"Error adding pattern: {e}")
            return False

    def remove_pattern(self, pattern_id: str) -> bool:
        """
        Remove a pattern from the library

        Args:
            pattern_id: ID of pattern to remove

        Returns:
            True if successful, False otherwise
        """
        try:
            self.patterns = [p for p in self.patterns if p.id != pattern_id]
            self._reorder_patterns()
            self.save_library()
            return True
        except Exception as e:
            print(f"Error removing pattern: {e}")
            return False

    def get_pattern_by_id(self, pattern_id: str) -> Optional[Pattern]:
        """
        Get a pattern by its ID

        Args:
            pattern_id: ID of the pattern

        Returns:
            Pattern if found, None otherwise
        """
        for pattern in self.patterns:
            if pattern.id == pattern_id:
                return pattern
        return None

    def get_pattern_by_index(self, index: int) -> Optional[Pattern]:
        """
        Get a pattern by its index in the current list

        Args:
            index: Index of the pattern

        Returns:
            Pattern if found, None otherwise
        """
        if 0 <= index < len(self.patterns):
            return self.patterns[index]
        return None

    def get_all_patterns(self) -> List[Pattern]:
        """Get all patterns in the library"""
        return self.patterns.copy()

    def update_pattern(self, pattern_id: str, **kwargs) -> bool:
        """
        Update a pattern's attributes

        Args:
            pattern_id: ID of pattern to update
            **kwargs: Attributes to update

        Returns:
            True if successful, False otherwise
        """
        pattern = self.get_pattern_by_id(pattern_id)
        if pattern:
            for key, value in kwargs.items():
                if hasattr(pattern, key):
                    setattr(pattern, key, value)
            self.save_library()
            return True
        return False

    def move_pattern(self, from_index: int, to_index: int) -> bool:
        """
        Move a pattern from one position to another

        Args:
            from_index: Current index
            to_index: Target index

        Returns:
            True if successful, False otherwise
        """
        try:
            if 0 <= from_index < len(self.patterns) and 0 <= to_index < len(self.patterns):
                pattern = self.patterns.pop(from_index)
                self.patterns.insert(to_index, pattern)
                self._reorder_patterns()
                self.save_library()
                return True
            return False
        except Exception as e:
            print(f"Error moving pattern: {e}")
            return False

    def _reorder_patterns(self):
        """Update custom_order values to match current list order"""
        for i, pattern in enumerate(self.patterns):
            pattern.custom_order = i

    def sort_patterns(self, sort_type: str = "custom"):
        """
        Sort patterns by specified criteria

        Args:
            sort_type: 'custom', 'name', or 'type'
        """
        if sort_type == "name":
            self.patterns.sort(key=lambda p: p.name.lower())
        elif sort_type == "type":
            self.patterns.sort(key=lambda p: (p.type, p.name.lower()))
        elif sort_type == "custom":
            self.patterns.sort(key=lambda p: p.custom_order)

        self._reorder_patterns()
        self.settings["library_sort"] = sort_type
        self.save_library()

    def search_patterns(self, query: str) -> List[Pattern]:
        """
        Search patterns by name

        Args:
            query: Search query

        Returns:
            List of matching patterns
        """
        query_lower = query.lower()
        return [
            p for p in self.patterns
            if query_lower in p.name.lower()
        ]

    def get_setting(self, key: str, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)

    def set_setting(self, key: str, value: Any):
        """Set a setting value"""
        self.settings[key] = value
        self.save_library()

    def get_pattern_count(self) -> int:
        """Get total number of patterns"""
        return len(self.patterns)

    def has_builtin_patterns(self) -> bool:
        """Check if library has built-in patterns"""
        return any(p.is_builtin for p in self.patterns)
