"""
Lesson 10: Movement Aesthetics (py5 version)
============================================

Explore how different art movements use color differently.
Compare Impressionism, Expressionism, and other styles.

Learning Objectives:
- Understand color characteristics of art movements
- Generate art in different movement styles
- Use renoir data to inform generative choices
- Compare warm/cool ratios and saturation levels

Run with: python movement_aesthetics_py5.py
"""

import py5

# Movement palettes and characteristics
movements = {
    "impressionism": {
        "name": "Impressionism",
        "palette": [],
        "saturation": 0.6,
        "stroke_style": "short",
        "description": "Light, atmospheric, broken color"
    },
    "expressionism": {
        "name": "Expressionism",
        "palette": [],
        "saturation": 0.9,
        "stroke_style": "bold",
        "description": "Emotional, vivid, distorted"
    },
    "tonalism": {
        "name": "Tonalism",
        "palette": [],
        "saturation": 0.3,
        "stroke_style": "soft",
        "description": "Muted, atmospheric, unified tone"
    },
    "fauvism": {
        "name": "Fauvism",
        "palette": [],
        "saturation": 1.0,
        "stroke_style": "wild",
        "description": "Wild beasts, pure color, liberation"
    }
}

current_movement = "impressionism"


def setup():
    py5.size(800, 600)
    initialize_palettes()
    set_background()

    print("Lesson 10: Movement Aesthetics")
    print("\nControls:")
    print("  Press 1-4 to switch movements")
    print("  Click and drag to paint")
    print("  Press 'c' to clear")
    print("  Press 's' to save image")


def initialize_palettes():
    """Initialize palettes for each movement."""
    # Impressionism: Light, airy colors
    movements["impressionism"]["palette"] = [
        py5.color(142, 178, 197),  # Sky blue
        py5.color(216, 191, 161),  # Warm beige
        py5.color(168, 199, 168),  # Soft green
        py5.color(230, 210, 180),  # Light cream
        py5.color(180, 160, 200),  # Lavender
    ]

    # Expressionism: Bold, emotional colors
    movements["expressionism"]["palette"] = [
        py5.color(200, 50, 50),    # Deep red
        py5.color(50, 50, 150),    # Dark blue
        py5.color(220, 180, 50),   # Intense yellow
        py5.color(30, 100, 30),    # Dark green
        py5.color(150, 50, 150),   # Purple
    ]

    # Tonalism: Muted, atmospheric
    movements["tonalism"]["palette"] = [
        py5.color(120, 115, 100),  # Warm gray
        py5.color(100, 110, 120),  # Cool gray
        py5.color(130, 120, 110),  # Taupe
        py5.color(90, 95, 100),    # Slate
        py5.color(110, 105, 95),   # Stone
    ]

    # Fauvism: Pure, saturated colors
    movements["fauvism"]["palette"] = [
        py5.color(255, 50, 50),    # Pure red
        py5.color(50, 200, 50),    # Pure green
        py5.color(50, 50, 255),    # Pure blue
        py5.color(255, 200, 0),    # Bright yellow
        py5.color(255, 100, 200),  # Hot pink
    ]


def draw():
    # Don't clear - allow painting to accumulate
    draw_ui()


def draw_ui():
    """Draw movement info panel."""
    m = movements[current_movement]

    # Info panel
    py5.fill(255, 240)
    py5.no_stroke()
    py5.rect(10, 10, 250, 90, 5)

    py5.fill(0)
    py5.text_size(16)
    py5.text(m["name"], 20, 35)

    py5.text_size(11)
    py5.fill(80)
    py5.text(m["description"], 20, 55)
    py5.text(f"Saturation: {int(m['saturation'] * 100)}%", 20, 75)
    py5.text(f"Style: {m['stroke_style']}", 130, 75)

    # Palette swatches
    for i, c in enumerate(m["palette"]):
        py5.fill(c)
        py5.no_stroke()
        py5.rect(20 + i * 25, 82, 20, 12, 2)


def mouse_dragged():
    """Paint in the current movement's style."""
    m = movements[current_movement]
    palette = m["palette"]
    style = m["stroke_style"]

    # Pick random color from palette
    col = palette[int(py5.random(len(palette)))]

    if style == "short":
        draw_impressionist_stroke(py5.mouse_x, py5.mouse_y, col)
    elif style == "bold":
        draw_expressionist_stroke(py5.mouse_x, py5.mouse_y, col)
    elif style == "soft":
        draw_tonalist_stroke(py5.mouse_x, py5.mouse_y, col)
    elif style == "wild":
        draw_fauvist_stroke(py5.mouse_x, py5.mouse_y, col)


def draw_impressionist_stroke(x, y, col):
    """Short, dabbed strokes with light variation."""
    for _ in range(3):
        px = x + py5.random(-15, 15)
        py_val = y + py5.random(-15, 15)

        # Slight color variation
        r = py5.red(col) + py5.random(-20, 20)
        g = py5.green(col) + py5.random(-20, 20)
        b = py5.blue(col) + py5.random(-20, 20)

        py5.no_stroke()
        py5.fill(r, g, b, 180)

        # Short dabs
        angle = py5.random(py5.TWO_PI)
        py5.push_matrix()
        py5.translate(px, py_val)
        py5.rotate(angle)
        py5.ellipse(0, 0, py5.random(8, 15), py5.random(4, 8))
        py5.pop_matrix()


def draw_expressionist_stroke(x, y, col):
    """Bold, angular, emotional strokes."""
    py5.stroke(col)
    py5.stroke_weight(py5.random(4, 10))
    py5.stroke_cap(py5.SQUARE)

    # Angular direction
    angle = py5.noise(x * 0.01, y * 0.01) * py5.TWO_PI
    length = py5.random(20, 40)

    x2 = x + py5.cos(angle) * length
    y2 = y + py5.sin(angle) * length

    py5.line(x, y, x2, y2)


def draw_tonalist_stroke(x, y, col):
    """Soft, atmospheric, blended strokes."""
    py5.no_stroke()

    # Very transparent, layered
    r = py5.red(col)
    g = py5.green(col)
    b = py5.blue(col)
    py5.fill(r, g, b, 30)

    # Soft, large circles
    for i in range(3):
        size = py5.random(30, 60)
        px = x + py5.random(-10, 10)
        py_val = y + py5.random(-10, 10)
        py5.ellipse(px, py_val, size, size)


def draw_fauvist_stroke(x, y, col):
    """Wild, energetic, pure color strokes."""
    py5.stroke(col)
    py5.stroke_weight(py5.random(5, 12))
    py5.stroke_cap(py5.ROUND)

    # Energetic, varied direction
    angle = py5.random(py5.TWO_PI)
    length = py5.random(15, 35)

    x2 = x + py5.cos(angle) * length
    y2 = y + py5.sin(angle) * length

    py5.line(x, y, x2, y2)

    # Sometimes add complementary splashes
    if py5.random(1) > 0.7:
        py5.no_stroke()
        py5.fill(255 - py5.red(col), 255 - py5.green(col), 255 - py5.blue(col), 200)
        py5.ellipse(x + py5.random(-20, 20), y + py5.random(-20, 20), 8, 8)


def key_pressed():
    global current_movement

    if py5.key == '1':
        current_movement = "impressionism"
        set_background()
        print("Movement: Impressionism")

    elif py5.key == '2':
        current_movement = "expressionism"
        set_background()
        print("Movement: Expressionism")

    elif py5.key == '3':
        current_movement = "tonalism"
        set_background()
        print("Movement: Tonalism")

    elif py5.key == '4':
        current_movement = "fauvism"
        set_background()
        print("Movement: Fauvism")

    elif py5.key == 'c':
        set_background()
        print("Canvas cleared")

    elif py5.key == 's':
        filename = f"{current_movement}_{py5.frame_count}.png"
        py5.save(filename)
        print(f"Saved: {filename}")


def set_background():
    """Set background appropriate to movement."""
    if current_movement == "tonalism":
        py5.background(180, 175, 165)
    elif current_movement == "expressionism":
        py5.background(30)
    else:
        py5.background(245)


# -------------------------------------------------
# Movement Aesthetics (from Renoir analysis):
#
# Impressionism:
# - Light, outdoor scenes
# - Broken color (optical mixing)
# - High brightness, moderate saturation
# - Short, visible brushstrokes
#
# Expressionism:
# - Emotional intensity
# - Bold, sometimes harsh colors
# - High saturation, strong contrasts
# - Distorted forms
#
# Tonalism:
# - Atmospheric, dreamlike
# - Limited color range
# - Low saturation, unified tone
# - Soft edges
#
# Fauvism:
# - "Wild beasts" of color
# - Pure, saturated hues
# - Liberation from realistic color
# - Energetic application
# -------------------------------------------------

py5.run_sketch()
