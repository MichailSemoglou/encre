"""
Lesson 02: Color Systems (py5 version)
======================================

Explore RGB and HSB color modes, color theory concepts,
and how they relate to the renoir color analysis.

Learning Objectives:
- Understand RGB vs HSB color modes
- Work with color components
- Create color harmonies
- Connect to renoir's color analysis concepts

Run with: python color_systems_py5.py
"""

import py5

# Color mode state
use_hsb = False


def setup():
    py5.size(800, 600)
    print("Lesson 02: Color Systems")
    print("\nControls:")
    print("  Press 'r' for RGB mode")
    print("  Press 'h' for HSB mode")
    print("  Press 's' to save image")
    print("  Move mouse to explore colors")


def draw():
    global use_hsb

    if use_hsb:
        py5.color_mode(py5.HSB, 360, 100, 100)
        draw_hsb_mode()
    else:
        py5.color_mode(py5.RGB, 255)
        draw_rgb_mode()

    # Draw mode indicator
    py5.color_mode(py5.RGB, 255)
    py5.fill(0)
    py5.no_stroke()
    py5.rect(0, 0, py5.width, 40)
    py5.fill(255)
    py5.text_size(16)
    mode_text = "HSB Mode (Hue, Saturation, Brightness)" if use_hsb else "RGB Mode (Red, Green, Blue)"
    py5.text(mode_text, 20, 26)


def draw_rgb_mode():
    """Demonstrate RGB color space."""
    py5.background(240)

    # RGB gradient bars
    for x in range(py5.width):
        r = py5.remap(x, 0, py5.width, 0, 255)

        # Red channel
        py5.stroke(r, 0, 0)
        py5.line(x, 60, x, 120)

        # Green channel
        py5.stroke(0, r, 0)
        py5.line(x, 140, x, 200)

        # Blue channel
        py5.stroke(0, 0, r)
        py5.line(x, 220, x, 280)

    # Labels
    py5.fill(0)
    py5.text_size(14)
    py5.text("Red", 10, 95)
    py5.text("Green", 10, 175)
    py5.text("Blue", 10, 255)

    # Interactive color mixer
    r = py5.remap(py5.mouse_x, 0, py5.width, 0, 255)
    g = py5.remap(py5.mouse_y, 0, py5.height, 0, 255)
    b = 128  # Fixed blue component

    # Color preview
    py5.fill(r, g, b)
    py5.stroke(0)
    py5.stroke_weight(2)
    py5.rect(300, 350, 200, 150, 10)

    # Color values
    py5.fill(0)
    py5.no_stroke()
    py5.text_size(14)
    py5.text(f"R: {int(r)}", 320, 380)
    py5.text(f"G: {int(g)}", 320, 400)
    py5.text(f"B: {int(b)}", 320, 420)
    py5.text("Move mouse to mix colors", 300, 530)

    # Complementary color
    py5.fill(255 - r, 255 - g, 255 - b)
    py5.stroke(0)
    py5.stroke_weight(2)
    py5.rect(520, 350, 80, 80, 10)

    py5.fill(0)
    py5.no_stroke()
    py5.text("Complement", 520, 460)


def draw_hsb_mode():
    """Demonstrate HSB color space - more intuitive for artists."""
    py5.background(30)

    # Hue wheel
    py5.no_stroke()
    center_x = 200
    center_y = 300
    radius = 120

    for angle in range(360):
        h = angle
        py5.fill(h, 100, 100)
        py5.arc(center_x, center_y, radius * 2, radius * 2,
                py5.radians(angle), py5.radians(angle + 2))

    # White center
    py5.fill(0, 0, 100)
    py5.ellipse(center_x, center_y, 80, 80)

    # Labels
    py5.fill(255)
    py5.text_size(14)
    py5.text("Hue Wheel", 160, 450)

    # Saturation gradient
    for x in range(200):
        s = py5.remap(x, 0, 200, 0, 100)
        py5.fill(200, s, 100)  # Fixed hue (cyan), varying saturation
        py5.no_stroke()
        py5.rect(450 + x, 100, 1, 60)

    py5.fill(255)
    py5.text("Saturation (0-100)", 500, 180)

    # Brightness gradient
    for x in range(200):
        b = py5.remap(x, 0, 200, 0, 100)
        py5.fill(200, 100, b)  # Fixed hue and saturation, varying brightness
        py5.no_stroke()
        py5.rect(450 + x, 220, 1, 60)

    py5.fill(255)
    py5.text("Brightness (0-100)", 500, 300)

    # Interactive HSB picker
    h = py5.remap(py5.mouse_x, 0, py5.width, 0, 360)
    s = py5.remap(py5.mouse_y, 0, py5.height, 100, 0)  # Inverted for intuitive control

    py5.fill(h, s, 90)
    py5.stroke(255)
    py5.stroke_weight(2)
    py5.rect(450, 350, 200, 120, 10)

    py5.fill(255)
    py5.no_stroke()
    py5.text_size(14)
    py5.text(f"H: {int(h)} deg", 470, 390)
    py5.text(f"S: {int(s)}%", 470, 410)
    py5.text("B: 90%", 470, 430)
    py5.text("Move mouse to explore", 450, 500)

    # Analogous colors (adjacent on wheel)
    py5.fill(255)
    py5.text("Analogous Colors:", 450, 540)

    for i in range(-2, 3):
        analog_h = (h + i * 30) % 360
        py5.fill(analog_h, s, 90)
        py5.no_stroke()
        py5.rect(450 + (i + 2) * 40, 550, 35, 35, 5)


def key_pressed():
    global use_hsb

    if py5.key == 'r':
        use_hsb = False
        print("Switched to RGB mode")

    elif py5.key == 'h':
        use_hsb = True
        print("Switched to HSB mode")

    elif py5.key == 's':
        filename = f"color_systems_{py5.frame_count}.png"
        py5.save(filename)
        print(f"Saved: {filename}")


# -------------------------------------------------
# Connection to Renoir:
#
# The renoir package uses HSV (same as HSB) for
# color analysis because it's more intuitive for
# understanding artistic color choices:
#
# - Hue: What color is it? (color wheel position)
# - Saturation: How vivid? (renoir's vibrancy analysis)
# - Brightness: How light/dark? (renoir's luminance)
#
# When analyzing an artist's palette with renoir,
# HSB helps reveal their color preferences:
# - Impressionists: High saturation, varied hues
# - Tonalists: Low saturation, limited hues
# -------------------------------------------------

py5.run_sketch()
