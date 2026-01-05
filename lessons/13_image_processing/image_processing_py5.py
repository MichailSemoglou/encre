"""
Lesson 13: Image Processing (py5 version)
=========================================

Learn to load, manipulate, and transform images
using pixel-level operations.

Learning Objectives:
- Load and display images
- Access and modify pixels
- Apply filters and effects
- Create artistic image transformations

Run with: python image_processing_py5.py
Note: Place an image named 'source.jpg' in the same folder.
"""

import py5
from pathlib import Path

# Image and mode
img = None
mode = 0
modes = ["Original", "Grayscale", "Threshold", "Pixelate", "Pointillism", "Color Shift"]

# Effect parameters
threshold_val = 128
pixel_size = 10
point_density = 5000

# Palette for pointillism
palette = []


def setup():
    py5.size(900, 600)
    global img, palette

    # Try to load image
    img_path = Path(__file__).parent / "data" / "source.jpg"
    if img_path.exists():
        img = py5.load_image(str(img_path))
        if img:
            img.resize(900, 600)
    else:
        img = None

    # Fallback: create a gradient image
    if img is None:
        img = py5.create_image(800, 600, py5.RGB)
        img.load_pixels()
        for y in range(img.height):
            for x in range(img.width):
                r = py5.remap(x, 0, img.width, 50, 200)
                g = py5.remap(y, 0, img.height, 100, 180)
                b = 150
                img.pixels[y * img.width + x] = py5.color(r, g, b)
        img.update_pixels()
        print("No image found - using generated gradient")
        print("Place 'source.jpg' in data/ folder for real images")

    # Art palette for pointillism
    palette = [
        py5.color(142, 178, 197),
        py5.color(219, 68, 55),
        py5.color(244, 180, 0),
        py5.color(15, 157, 88),
        py5.color(156, 39, 176),
    ]

    print("Lesson 13: Image Processing")
    print("\nControls:")
    print("  Press 1-6 to switch effects")
    print("  Up/Down to adjust parameters")
    print("  Press 's' to save image")


def draw():
    py5.background(30)

    if mode == 0:
        draw_original()
    elif mode == 1:
        draw_grayscale()
    elif mode == 2:
        draw_threshold()
    elif mode == 3:
        draw_pixelate()
    elif mode == 4:
        draw_pointillism()
    elif mode == 5:
        draw_color_shift()

    draw_ui()


def draw_original():
    """Display original image."""
    py5.image(img, 0, 0)


def draw_grayscale():
    """Convert to grayscale."""
    result = py5.create_image(img.width, img.height, py5.RGB)
    img.load_pixels()
    result.load_pixels()

    for i in range(len(img.pixels)):
        c = img.pixels[i]
        r = py5.red(c)
        g = py5.green(c)
        b = py5.blue(c)
        gray = 0.299 * r + 0.587 * g + 0.114 * b
        result.pixels[i] = py5.color(gray)

    result.update_pixels()
    py5.image(result, 0, 0)


def draw_threshold():
    """Binary threshold effect."""
    result = py5.create_image(img.width, img.height, py5.RGB)
    img.load_pixels()
    result.load_pixels()

    for i in range(len(img.pixels)):
        c = img.pixels[i]
        gray = (py5.red(c) + py5.green(c) + py5.blue(c)) / 3

        if gray > threshold_val:
            result.pixels[i] = py5.color(255)
        else:
            result.pixels[i] = py5.color(0)

    result.update_pixels()
    py5.image(result, 0, 0)


def draw_pixelate():
    """Pixelation effect."""
    py5.no_stroke()
    img.load_pixels()

    for y in range(0, img.height, pixel_size):
        for x in range(0, img.width, pixel_size):
            # Get pixel from center of block
            px = min(x + pixel_size//2, img.width - 1)
            py = min(y + pixel_size//2, img.height - 1)
            c = img.pixels[py * img.width + px]
            py5.fill(c)
            py5.rect(x, y, pixel_size, pixel_size)


def draw_pointillism():
    """Pointillist rendering using palette colors."""
    py5.background(240)
    py5.no_stroke()
    img.load_pixels()

    for _ in range(point_density):
        x = int(py5.random(img.width))
        y = int(py5.random(img.height))

        c = img.pixels[y * img.width + x]
        closest = find_closest_color(c)

        py5.fill(closest, 200)
        size_val = py5.random(3, 8)
        py5.ellipse(x, y, size_val, size_val)


def find_closest_color(target):
    """Find closest color in palette."""
    min_dist = float('inf')
    closest = palette[0]

    tr = py5.red(target)
    tg = py5.green(target)
    tb = py5.blue(target)

    for c in palette:
        pr = py5.red(c)
        pg = py5.green(c)
        pb = py5.blue(c)

        d = py5.sqrt((tr - pr)**2 + (tg - pg)**2 + (tb - pb)**2)
        if d < min_dist:
            min_dist = d
            closest = c

    return closest


def draw_color_shift():
    """Shift colors in HSB space."""
    result = py5.create_image(img.width, img.height, py5.RGB)
    img.load_pixels()
    result.load_pixels()

    shift = py5.remap(py5.mouse_x, 0, py5.width, 0, 360)

    py5.color_mode(py5.HSB, 360, 100, 100)

    for i in range(len(img.pixels)):
        c = img.pixels[i]
        h = py5.hue(c)
        s = py5.saturation(c)
        b = py5.brightness(c)

        new_h = (h + shift) % 360
        result.pixels[i] = py5.color(new_h, s, b)

    py5.color_mode(py5.RGB, 255)
    result.update_pixels()
    py5.image(result, 0, 0)


def draw_ui():
    """Draw effect info."""
    py5.fill(0, 180)
    py5.no_stroke()
    py5.rect(10, 10, 200, 70, 5)

    py5.fill(255)
    py5.text_size(14)
    py5.text(f"Effect: {modes[mode]}", 20, 32)

    py5.text_size(11)
    if mode == 2:
        py5.text(f"Threshold: {threshold_val}", 20, 52)
        py5.text("Up/Down to adjust", 20, 68)
    elif mode == 3:
        py5.text(f"Pixel size: {pixel_size}", 20, 52)
        py5.text("Up/Down to adjust", 20, 68)
    elif mode == 4:
        py5.text(f"Density: {point_density}", 20, 52)
        py5.text("Up/Down to adjust", 20, 68)
    elif mode == 5:
        py5.text("Move mouse to shift hue", 20, 52)


def key_pressed():
    global mode, threshold_val, pixel_size, point_density

    if py5.key == '1':
        mode = 0
    elif py5.key == '2':
        mode = 1
    elif py5.key == '3':
        mode = 2
    elif py5.key == '4':
        mode = 3
    elif py5.key == '5':
        mode = 4
    elif py5.key == '6':
        mode = 5
    elif py5.key_code == py5.UP:
        if mode == 2:
            threshold_val = min(threshold_val + 10, 255)
        elif mode == 3:
            pixel_size = min(pixel_size + 2, 50)
        elif mode == 4:
            point_density = min(point_density + 500, 20000)
    elif py5.key_code == py5.DOWN:
        if mode == 2:
            threshold_val = max(threshold_val - 10, 0)
        elif mode == 3:
            pixel_size = max(pixel_size - 2, 2)
        elif mode == 4:
            point_density = max(point_density - 500, 500)
    elif py5.key == 's':
        filename = f"processed_{py5.frame_count}.png"
        py5.save(filename)
        print(f"Saved: {filename}")


# -------------------------------------------------
# Image Processing Concepts:
#
# 1. Pixel Access:
#    img.load_pixels()   - Load into pixels[]
#    img.pixels[i]       - Access pixel i
#    img.update_pixels() - Apply changes
#    img.pixels[y * img.width + x] - Get color at x,y
#
# 2. Color Components:
#    py5.red(c), py5.green(c), py5.blue(c)
#    py5.hue(c), py5.saturation(c), py5.brightness(c)
#
# 3. Common Operations:
#    - Grayscale: Average RGB or use luminance
#    - Threshold: Binary black/white
#    - Pixelate: Sample blocks
#    - Color shift: Modify HSB values
#
# Connection to Renoir:
# Image processing can extract color palettes
# from artwork images, which is exactly what
# renoir's ColorExtractor does using k-means
# clustering.
# -------------------------------------------------

py5.run_sketch()
