"""Utility Functions - Helper functions for the application"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from .models import Pattern


class TestPatternGenerator:
    """Generate built-in test patterns programmatically"""

    def __init__(self, output_dir: str = "resources/patterns"):
        """
        Initialize the test pattern generator

        Args:
            output_dir: Directory to save generated patterns
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.width = 1920
        self.height = 1080

    def generate_all_patterns(self, pattern_manager) -> int:
        """
        Generate all built-in test patterns if they don't exist

        Args:
            pattern_manager: PatternManager instance to add patterns to

        Returns:
            Number of patterns generated
        """
        # Only generate if library doesn't have built-in patterns
        if pattern_manager.has_builtin_patterns():
            print("Built-in patterns already exist, skipping generation")
            return 0

        patterns_info = [
            ("smpte_bars.png", "SMPTE Color Bars", self.generate_smpte_bars),
            ("ebu_bars.png", "EBU Color Bars", self.generate_ebu_bars),
            ("grayscale.png", "Grayscale Ramp", self.generate_grayscale),
            ("grid.png", "Grid Pattern", self.generate_grid),
            ("black.png", "Black Frame", self.generate_black),
            ("white.png", "White Frame", self.generate_white),
        ]

        generated = 0
        for i, (filename, name, generator_func) in enumerate(patterns_info):
            filepath = self.output_dir / filename

            # Generate the pattern image
            generator_func(filepath)

            # Create Pattern object and add to manager
            pattern = Pattern.create(
                name=name,
                path=str(filepath),
                pattern_type="image",
                custom_order=i,
                is_builtin=True
            )
            pattern_manager.add_pattern(pattern)
            generated += 1
            print(f"Generated: {name}")

        print(f"Generated {generated} built-in test patterns")
        return generated

    def generate_smpte_bars(self, filepath: Path):
        """Generate SMPTE color bars test pattern"""
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)

        # SMPTE color bars (standard 75% bars)
        bar_width = self.width // 7
        top_height = int(self.height * 0.67)
        middle_height = int(self.height * 0.75)

        # Top section - 7 bars (75% intensity)
        colors_top = [
            (192, 192, 192),  # White (75%)
            (192, 192, 0),    # Yellow
            (0, 192, 192),    # Cyan
            (0, 192, 0),      # Green
            (192, 0, 192),    # Magenta
            (192, 0, 0),      # Red
            (0, 0, 192),      # Blue
        ]

        for i, color in enumerate(colors_top):
            x1 = i * bar_width
            x2 = (i + 1) * bar_width if i < 6 else self.width
            draw.rectangle([x1, 0, x2, top_height], fill=color)

        # Middle section - Blue, Black, Magenta, Black, Cyan, Black, White
        colors_middle = [
            (0, 0, 192),      # Blue
            (0, 0, 0),        # Black
            (192, 0, 192),    # Magenta
            (0, 0, 0),        # Black
            (0, 192, 192),    # Cyan
            (0, 0, 0),        # Black
            (192, 192, 192),  # White
        ]

        for i, color in enumerate(colors_middle):
            x1 = i * bar_width
            x2 = (i + 1) * bar_width if i < 6 else self.width
            draw.rectangle([x1, top_height, x2, middle_height], fill=color)

        # Bottom section - PLUGE pattern
        pluge_width = bar_width * 5 // 7
        colors_pluge = [
            (9, 9, 9),        # -I (3.5% black)
            (0, 0, 0),        # Black
            (19, 19, 19),     # +I (7.5% gray)
            (0, 0, 0),        # Black
        ]

        x_offset = 0
        for i, color in enumerate(colors_pluge):
            if i < 3:
                w = pluge_width
            else:
                w = self.width - x_offset
            draw.rectangle([x_offset, middle_height, x_offset + w, self.height], fill=color)
            x_offset += w

        img.save(filepath)

    def generate_ebu_bars(self, filepath: Path):
        """Generate EBU color bars test pattern"""
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)

        # EBU color bars (100% bars)
        bar_width = self.width // 8

        # Main section - 8 bars (100% intensity)
        colors = [
            (255, 255, 255),  # White (100%)
            (255, 255, 0),    # Yellow
            (0, 255, 255),    # Cyan
            (0, 255, 0),      # Green
            (255, 0, 255),    # Magenta
            (255, 0, 0),      # Red
            (0, 0, 255),      # Blue
            (0, 0, 0),        # Black
        ]

        for i, color in enumerate(colors):
            x1 = i * bar_width
            x2 = (i + 1) * bar_width if i < 7 else self.width
            draw.rectangle([x1, 0, x2, self.height], fill=color)

        img.save(filepath)

    def generate_grayscale(self, filepath: Path):
        """Generate grayscale ramp test pattern"""
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)

        # Create 16 steps from black to white
        num_steps = 16
        step_width = self.width // num_steps

        for i in range(num_steps):
            gray_value = int((i / (num_steps - 1)) * 255)
            color = (gray_value, gray_value, gray_value)
            x1 = i * step_width
            x2 = (i + 1) * step_width if i < num_steps - 1 else self.width
            draw.rectangle([x1, 0, x2, self.height], fill=color)

        img.save(filepath)

    def generate_grid(self, filepath: Path):
        """Generate grid/crosshatch test pattern"""
        img = Image.new('RGB', (self.width, self.height), color=(32, 32, 32))
        draw = ImageDraw.Draw(img)

        # Grid spacing
        grid_spacing = 96  # Every 96 pixels

        # Draw vertical lines
        for x in range(0, self.width, grid_spacing):
            line_width = 2 if x % (grid_spacing * 2) == 0 else 1
            draw.line([(x, 0), (x, self.height)], fill=(128, 128, 128), width=line_width)

        # Draw horizontal lines
        for y in range(0, self.height, grid_spacing):
            line_width = 2 if y % (grid_spacing * 2) == 0 else 1
            draw.line([(0, y), (self.width, y)], fill=(128, 128, 128), width=line_width)

        # Draw center crosshairs
        center_x = self.width // 2
        center_y = self.height // 2
        crosshair_size = 100

        # Red crosshairs at center
        draw.line([(center_x - crosshair_size, center_y), (center_x + crosshair_size, center_y)],
                  fill=(255, 0, 0), width=3)
        draw.line([(center_x, center_y - crosshair_size), (center_x, center_y + crosshair_size)],
                  fill=(255, 0, 0), width=3)

        # Draw corner markers
        marker_size = 50
        corners = [
            (0, 0),
            (self.width - marker_size, 0),
            (0, self.height - marker_size),
            (self.width - marker_size, self.height - marker_size)
        ]

        for cx, cy in corners:
            draw.rectangle([cx, cy, cx + marker_size, cy + marker_size],
                          outline=(255, 255, 255), width=2)

        img.save(filepath)

    def generate_black(self, filepath: Path):
        """Generate black frame"""
        img = Image.new('RGB', (self.width, self.height), color=(0, 0, 0))
        img.save(filepath)

    def generate_white(self, filepath: Path):
        """Generate white frame"""
        img = Image.new('RGB', (self.width, self.height), color=(255, 255, 255))
        img.save(filepath)


def init_builtin_patterns(pattern_manager) -> int:
    """
    Initialize built-in patterns if they don't exist

    Args:
        pattern_manager: PatternManager instance

    Returns:
        Number of patterns generated
    """
    generator = TestPatternGenerator()
    return generator.generate_all_patterns(pattern_manager)
