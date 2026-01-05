"""
Lesson 09: Palette-Driven Generation
====================================

This sketch demonstrates how to load color palettes
exported from renoir and use them in generative art.

Prerequisites:
- Export a palette using utils/palette_exporter.py
- Place the JSON file in the data/ folder

Learning Objectives:
- Load JSON data in Processing.py
- Convert renoir palettes to Processing colors
- Create generative compositions using art-historical colors
"""

import json

# Global variables
palette = []
color_names = []
brushstrokes = []

class Brushstroke:
    """A simple brushstroke inspired by Impressionism."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.col = palette[int(random(len(palette)))]
        self.angle = noise(x * 0.01, y * 0.01) * TWO_PI
        self.length = random(15, 40)
        self.weight = random(3, 8)
        self.alpha = random(150, 220)

    def display(self):
        pushMatrix()
        translate(self.x, self.y)
        rotate(self.angle)

        # Get RGB components from the color
        r = red(self.col)
        g = green(self.col)
        b = blue(self.col)

        stroke(r, g, b, self.alpha)
        strokeWeight(self.weight)
        strokeCap(ROUND)
        line(-self.length/2, 0, self.length/2, 0)
        popMatrix()


def setup():
    size(800, 600)
    global palette, color_names

    # Try to load palette from JSON
    try:
        # Path relative to sketch folder
        with open('data/monet.json') as f:
            data = json.load(f)

        # Convert to Processing colors
        if 'named_colors' in data:
            for c in data['named_colors']:
                palette.append(color(c['rgb'][0], c['rgb'][1], c['rgb'][2]))
                color_names.append(c.get('name', 'Unknown'))
        else:
            for c in data['colors']:
                palette.append(color(c[0], c[1], c[2]))
                color_names.append('Color ' + str(len(palette)))

        print("Loaded palette with", len(palette), "colors:")
        for name in color_names:
            print(" -", name)

    except Exception as e:
        print("Could not load palette:", e)
        print("Using default colors...")
        # Fallback: Monet-inspired colors
        palette = [
            color(142, 178, 197),  # Sky blue
            color(89, 112, 95),    # Sage green
            color(216, 191, 161),  # Warm beige
            color(78, 91, 110),    # Blue-gray
            color(168, 147, 120)   # Earth tone
        ]
        color_names = ['Sky', 'Sage', 'Beige', 'Blue-gray', 'Earth']

    # Set background to darkest palette color or first color
    background(palette[0])

    print("\nControls:")
    print("  Click and drag to paint")
    print("  Press 'c' to clear")
    print("  Press 's' to save image")
    print("  Press 'p' to show palette")
    print("  Press 'h' to hide palette")


def draw():
    # Add brushstrokes while mouse is pressed
    if mousePressed:
        for _ in range(3):  # Multiple strokes per frame
            x = mouseX + random(-20, 20)
            y = mouseY + random(-20, 20)
            stroke = Brushstroke(x, y)
            stroke.display()


def keyPressed():
    global brushstrokes

    if key == 'c':
        # Clear canvas
        background(palette[0])
        print("Canvas cleared")

    elif key == 's':
        # Save image
        filename = "palette_driven_" + str(frameCount) + ".png"
        save(filename)
        print("Saved:", filename)

    elif key == 'p':
        # Show palette
        showPalette()

    elif key == 'h':
        # Hide palette (redraw background)
        background(palette[0])
        print("Palette hidden")


def showPalette():
    """Display the current palette as swatches."""
    swatch_size = 60
    margin = 20

    # Draw palette background
    fill(255, 230)
    noStroke()
    rect(margin - 10, margin - 10,
         len(palette) * (swatch_size + 10) + 10,
         swatch_size + 50)

    # Draw color swatches
    for i, (c, name) in enumerate(zip(palette, color_names)):
        x = margin + i * (swatch_size + 10)
        y = margin

        # Swatch
        fill(c)
        stroke(0)
        strokeWeight(1)
        rect(x, y, swatch_size, swatch_size)

        # Label
        fill(0)
        textSize(10)
        text(name[:10], x, y + swatch_size + 15)


def mousePressed():
    """Start painting."""
    pass  # Drawing happens in draw() when mousePressed is True


# -------------------------------------------------
# To use this sketch:
#
# 1. First, export a palette from renoir:
#
#    cd utils/
#    python palette_exporter.py --artist claude-monet \
#        --output ../lessons/09_palette_driven/data/monet.json
#
# 2. Or create a simple palette JSON manually:
#
#    {
#      "colors": [
#        [142, 178, 197],
#        [89, 112, 95],
#        [216, 191, 161]
#      ]
#    }
#
# 3. Run this sketch in Processing (Python Mode)
# -------------------------------------------------
