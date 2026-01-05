"""
Lesson 09: Palette-Driven Generation (py5 version)
===================================================

This sketch demonstrates how to load color palettes
exported from renoir and use them in generative art.

Run with: python palette_driven_py5.py
"""

import py5
import json
from pathlib import Path

# Global variables
palette = []
color_names = []


class Brushstroke:
    """A simple brushstroke inspired by Impressionism."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.col = palette[int(py5.random(len(palette)))]
        self.angle = py5.noise(x * 0.01, y * 0.01) * py5.TWO_PI
        self.length = py5.random(15, 40)
        self.weight = py5.random(3, 8)
        self.alpha = py5.random(150, 220)

    def display(self):
        py5.push_matrix()
        py5.translate(self.x, self.y)
        py5.rotate(self.angle)

        # Get RGB components from the color
        r = py5.red(self.col)
        g = py5.green(self.col)
        b = py5.blue(self.col)

        py5.stroke(r, g, b, self.alpha)
        py5.stroke_weight(self.weight)
        py5.stroke_cap(py5.ROUND)
        py5.line(-self.length/2, 0, self.length/2, 0)
        py5.pop_matrix()


def setup():
    py5.size(800, 600)
    global palette, color_names

    # Try to load palette from JSON
    data_path = Path(__file__).parent / 'data' / 'monet.json'

    try:
        with open(data_path) as f:
            data = json.load(f)

        # Convert to py5 colors
        if 'named_colors' in data:
            for c in data['named_colors']:
                palette.append(py5.color(c['rgb'][0], c['rgb'][1], c['rgb'][2]))
                color_names.append(c.get('name', 'Unknown'))
        else:
            for c in data['colors']:
                palette.append(py5.color(c[0], c[1], c[2]))
                color_names.append('Color ' + str(len(palette)))

        print(f"Loaded palette with {len(palette)} colors:")
        for name in color_names:
            print(f" - {name}")

    except Exception as e:
        print(f"Could not load palette: {e}")
        print("Using default colors...")
        # Fallback: Monet-inspired colors
        palette = [
            py5.color(142, 178, 197),  # Sky blue
            py5.color(89, 112, 95),    # Sage green
            py5.color(216, 191, 161),  # Warm beige
            py5.color(78, 91, 110),    # Blue-gray
            py5.color(168, 147, 120)   # Earth tone
        ]
        color_names = ['Sky', 'Sage', 'Beige', 'Blue-gray', 'Earth']

    # Set background to first palette color
    py5.background(palette[0])

    print("\nControls:")
    print("  Click and drag to paint")
    print("  Press 'c' to clear")
    print("  Press 's' to save image")
    print("  Press 'p' to show palette")
    print("  Press 'h' to hide palette")


def draw():
    # Add brushstrokes while mouse is pressed
    if py5.is_mouse_pressed:
        for _ in range(3):  # Multiple strokes per frame
            x = py5.mouse_x + py5.random(-20, 20)
            y = py5.mouse_y + py5.random(-20, 20)
            stroke = Brushstroke(x, y)
            stroke.display()


def key_pressed():
    if py5.key == 'c':
        # Clear canvas
        py5.background(palette[0])
        print("Canvas cleared")

    elif py5.key == 's':
        # Save image
        filename = f"palette_driven_{py5.frame_count}.png"
        py5.save(filename)
        print(f"Saved: {filename}")

    elif py5.key == 'p':
        # Show palette
        show_palette()

    elif py5.key == 'h':
        # Hide palette (redraw background)
        py5.background(palette[0])
        print("Palette hidden")


def show_palette():
    """Display the current palette as swatches."""
    swatch_size = 60
    margin = 20

    # Draw palette background
    py5.fill(255, 230)
    py5.no_stroke()
    py5.rect(margin - 10, margin - 10,
             len(palette) * (swatch_size + 10) + 10,
             swatch_size + 50)

    # Draw color swatches
    for i, (c, name) in enumerate(zip(palette, color_names)):
        x = margin + i * (swatch_size + 10)
        y = margin

        # Swatch
        py5.fill(c)
        py5.stroke(0)
        py5.stroke_weight(1)
        py5.rect(x, y, swatch_size, swatch_size)

        # Label
        py5.fill(0)
        py5.text_size(10)
        py5.text(name[:10], x, y + swatch_size + 15)


def mouse_pressed():
    """Start painting."""
    pass  # Drawing happens in draw() when is_mouse_pressed is True


# Run the sketch
py5.run_sketch()
