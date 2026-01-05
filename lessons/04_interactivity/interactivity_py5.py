"""
Lesson 04: Interactivity (py5 version)
======================================

Learn to respond to mouse and keyboard input
to create interactive generative art.

Learning Objectives:
- Handle mouse events and position
- Respond to keyboard input
- Create interactive drawing tools
- Build responsive visual feedback

Run with: python interactivity_py5.py
"""

import py5

# Drawing state
strokes = []
current_color = None
brush_size = 20
colors = []


def setup():
    py5.size(800, 600)
    py5.background(250)

    global colors, current_color
    # Art-inspired palette
    colors = [
        py5.color(41, 65, 114),    # Deep blue
        py5.color(193, 84, 55),    # Burnt orange
        py5.color(85, 130, 89),    # Sage green
        py5.color(156, 136, 103),  # Warm gray
        py5.color(180, 60, 60),    # Muted red
    ]
    current_color = colors[0]

    print("Lesson 04: Interactivity")
    print("\nControls:")
    print("  Mouse drag: Draw")
    print("  1-5: Change color")
    print("  Up/Down: Brush size")
    print("  'c': Clear canvas")
    print("  's': Save image")
    print("  'p': Show palette")


def draw():
    # Draw UI elements
    draw_brush_preview()
    draw_palette_bar()


def draw_brush_preview():
    """Show current brush at mouse position."""
    # Brush preview (follows mouse)
    py5.no_fill()
    py5.stroke(0, 100)
    py5.stroke_weight(1)
    py5.ellipse(py5.mouse_x, py5.mouse_y, brush_size, brush_size)


def draw_palette_bar():
    """Draw color palette at bottom."""
    bar_height = 40
    swatch_size = 30

    # Background bar
    py5.no_stroke()
    py5.fill(240)
    py5.rect(0, py5.height - bar_height, py5.width, bar_height)

    # Color swatches
    for i, c in enumerate(colors):
        x = 20 + i * (swatch_size + 10)
        y = py5.height - bar_height + 5

        # Highlight current color
        if c == current_color:
            py5.stroke(0)
            py5.stroke_weight(3)
        else:
            py5.stroke(150)
            py5.stroke_weight(1)

        py5.fill(c)
        py5.rect(x, y, swatch_size, swatch_size, 5)

    # Brush size indicator
    py5.fill(0)
    py5.no_stroke()
    py5.text_size(12)
    py5.text(f"Size: {brush_size}", py5.width - 100, py5.height - 15)

    # Key hints
    py5.fill(100)
    py5.text("Keys: 1-5 color | Up/Down size | c clear | s save", 220, py5.height - 15)


def mouse_dragged():
    """Draw while mouse is dragged."""
    # Calculate brush opacity based on speed
    speed = py5.dist(py5.mouse_x, py5.mouse_y, py5.pmouse_x, py5.pmouse_y)
    alpha = py5.remap(speed, 0, 50, 200, 50)
    alpha = py5.constrain(alpha, 50, 200)

    # Draw brush stroke
    py5.no_stroke()
    r = py5.red(current_color)
    g = py5.green(current_color)
    b = py5.blue(current_color)
    py5.fill(r, g, b, alpha)

    # Draw multiple circles for smooth stroke
    steps = int(speed) + 1
    for i in range(steps):
        t = float(i) / steps
        x = py5.lerp(py5.pmouse_x, py5.mouse_x, t)
        y = py5.lerp(py5.pmouse_y, py5.mouse_y, t)
        py5.ellipse(x, y, brush_size, brush_size)


def mouse_pressed():
    """Single click draws a dot."""
    if py5.mouse_y < py5.height - 45:  # Not on palette bar
        py5.no_stroke()
        r = py5.red(current_color)
        g = py5.green(current_color)
        b = py5.blue(current_color)
        py5.fill(r, g, b, 200)
        py5.ellipse(py5.mouse_x, py5.mouse_y, brush_size, brush_size)


def key_pressed():
    global current_color, brush_size

    # Number keys for color selection
    if py5.key == '1' and len(colors) >= 1:
        current_color = colors[0]
        print("Color: Deep Blue")
    elif py5.key == '2' and len(colors) >= 2:
        current_color = colors[1]
        print("Color: Burnt Orange")
    elif py5.key == '3' and len(colors) >= 3:
        current_color = colors[2]
        print("Color: Sage Green")
    elif py5.key == '4' and len(colors) >= 4:
        current_color = colors[3]
        print("Color: Warm Gray")
    elif py5.key == '5' and len(colors) >= 5:
        current_color = colors[4]
        print("Color: Muted Red")

    # Arrow keys for brush size
    elif py5.key_code == py5.UP:
        brush_size = min(brush_size + 5, 100)
        print(f"Brush size: {brush_size}")
    elif py5.key_code == py5.DOWN:
        brush_size = max(brush_size - 5, 5)
        print(f"Brush size: {brush_size}")

    # Clear canvas
    elif py5.key == 'c':
        py5.background(250)
        print("Canvas cleared")

    # Save image
    elif py5.key == 's':
        filename = f"interactive_{py5.frame_count}.png"
        py5.save(filename)
        print(f"Saved: {filename}")

    # Show palette info
    elif py5.key == 'p':
        show_palette_info()


def show_palette_info():
    """Display palette information overlay."""
    # Semi-transparent overlay
    py5.fill(255, 230)
    py5.no_stroke()
    py5.rect(50, 50, 300, 200, 10)

    py5.fill(0)
    py5.text_size(16)
    py5.text("Current Palette", 70, 80)

    py5.text_size(12)
    names = ["Deep Blue", "Burnt Orange", "Sage Green", "Warm Gray", "Muted Red"]
    for i, (c, name) in enumerate(zip(colors, names)):
        y = 110 + i * 30

        py5.fill(c)
        py5.no_stroke()
        py5.rect(70, y - 15, 20, 20, 3)

        py5.fill(0)
        py5.text(name, 100, y)

        # RGB values
        py5.fill(100)
        py5.text(f"RGB({int(py5.red(c))}, {int(py5.green(c))}, {int(py5.blue(c))})", 200, y)


# -------------------------------------------------
# Interactivity Tips:
#
# Mouse variables:
# - py5.mouse_x, py5.mouse_y: Current position
# - py5.pmouse_x, py5.pmouse_y: Previous frame position
# - py5.is_mouse_pressed: Boolean, is mouse down?
#
# Keyboard:
# - py5.key: The character pressed
# - py5.key_code: Special keys (UP, DOWN, LEFT, RIGHT)
#
# Events:
# - mouse_pressed(): Called once on click
# - mouse_dragged(): Called while dragging
# - mouse_released(): Called when released
# - key_pressed(): Called once per key press
# -------------------------------------------------

py5.run_sketch()
