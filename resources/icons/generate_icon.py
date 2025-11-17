"""
Generate application icon for Test Pattern Player
Creates a simple SMPTE-inspired icon
"""

from PIL import Image, ImageDraw

def generate_icon():
    """Generate application icon with SMPTE color bars"""
    # Icon sizes
    sizes = [16, 32, 48, 64, 128, 256, 512, 1024]

    # SMPTE color bars (simplified - 7 bars)
    colors = [
        (192, 192, 192),  # White (75%)
        (192, 192, 0),    # Yellow
        (0, 192, 192),    # Cyan
        (0, 192, 0),      # Green
        (192, 0, 192),    # Magenta
        (192, 0, 0),      # Red
        (0, 0, 192),      # Blue
    ]

    for size in sizes:
        # Create new image
        img = Image.new('RGB', (size, size), (0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Draw color bars
        bar_width = size // 7
        for i, color in enumerate(colors):
            x1 = i * bar_width
            x2 = (i + 1) * bar_width if i < 6 else size
            draw.rectangle([(x1, 0), (x2, size)], fill=color)

        # Save PNG
        img.save(f'icon_{size}x{size}.png', 'PNG')
        print(f"Generated icon_{size}x{size}.png")

    # Create main icon.png (512x512 for app)
    img = Image.new('RGB', (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    bar_width = 512 // 7
    for i, color in enumerate(colors):
        x1 = i * bar_width
        x2 = (i + 1) * bar_width if i < 6 else 512
        draw.rectangle([(x1, 0), (x2, 512)], fill=color)

    img.save('icon.png', 'PNG')
    print("Generated icon.png")

    # Create ICO file for Windows (multiple sizes)
    icon_images = []
    for size in [16, 32, 48, 64, 128, 256]:
        img = Image.new('RGB', (size, size), (0, 0, 0))
        draw = ImageDraw.Draw(img)

        bar_width = size // 7
        for i, color in enumerate(colors):
            x1 = i * bar_width
            x2 = (i + 1) * bar_width if i < 6 else size
            draw.rectangle([(x1, 0), (x2, size)], fill=color)

        icon_images.append(img)

    # Save as ICO (Windows icon)
    icon_images[0].save('icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
    print("Generated icon.ico")

    # Create ICNS for macOS (requires additional setup, so we'll note this)
    print("\nNote: For macOS .icns file, use iconutil on macOS:")
    print("  mkdir icon.iconset")
    print("  cp icon_16x16.png icon.iconset/icon_16x16.png")
    print("  cp icon_32x32.png icon.iconset/icon_16x16@2x.png")
    print("  cp icon_32x32.png icon.iconset/icon_32x32.png")
    print("  cp icon_64x64.png icon.iconset/icon_32x32@2x.png")
    print("  cp icon_128x128.png icon.iconset/icon_128x128.png")
    print("  cp icon_256x256.png icon.iconset/icon_128x128@2x.png")
    print("  cp icon_256x256.png icon.iconset/icon_256x256.png")
    print("  cp icon_512x512.png icon.iconset/icon_256x256@2x.png")
    print("  cp icon_512x512.png icon.iconset/icon_512x512.png")
    print("  cp icon_1024x1024.png icon.iconset/icon_512x512@2x.png")
    print("  iconutil -c icns icon.iconset")

if __name__ == '__main__':
    generate_icon()
