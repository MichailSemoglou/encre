"""
Lesson 02: Color Systems
========================

Explore RGB and HSB color modes, color theory concepts,
and how they relate to the renoir color analysis.

Learning Objectives:
- Understand RGB vs HSB color modes
- Work with color components
- Create color harmonies
- Connect to renoir's color analysis concepts

Run this sketch in Processing with Python Mode enabled.
"""

# Color mode state
use_hsb = False

def setup():
    size(800, 600)
    print("Lesson 02: Color Systems")
    print("\nControls:")
    print("  Press 'r' for RGB mode")
    print("  Press 'h' for HSB mode")
    print("  Press 's' to save image")
    print("  Move mouse to explore colors")


def draw():
    global use_hsb

    if use_hsb:
        colorMode(HSB, 360, 100, 100)
        drawHSBMode()
    else:
        colorMode(RGB, 255)
        drawRGBMode()

    # Draw mode indicator
    colorMode(RGB, 255)
    fill(0)
    noStroke()
    rect(0, 0, width, 40)
    fill(255)
    textSize(16)
    mode_text = "HSB Mode (Hue, Saturation, Brightness)" if use_hsb else "RGB Mode (Red, Green, Blue)"
    text(mode_text, 20, 26)


def drawRGBMode():
    """Demonstrate RGB color space."""
    background(240)

    # RGB gradient bars
    for x in range(width):
        r = map(x, 0, width, 0, 255)

        # Red channel
        stroke(r, 0, 0)
        line(x, 60, x, 120)

        # Green channel
        stroke(0, r, 0)
        line(x, 140, x, 200)

        # Blue channel
        stroke(0, 0, r)
        line(x, 220, x, 280)

    # Labels
    fill(0)
    textSize(14)
    text("Red", 10, 95)
    text("Green", 10, 175)
    text("Blue", 10, 255)

    # Interactive color mixer
    r = map(mouseX, 0, width, 0, 255)
    g = map(mouseY, 0, height, 0, 255)
    b = 128  # Fixed blue component

    # Color preview
    fill(r, g, b)
    stroke(0)
    strokeWeight(2)
    rect(300, 350, 200, 150, 10)

    # Color values
    fill(0)
    noStroke()
    textSize(14)
    text("R: " + str(int(r)), 320, 380)
    text("G: " + str(int(g)), 320, 400)
    text("B: " + str(int(b)), 320, 420)
    text("Move mouse to mix colors", 300, 530)

    # Complementary color
    fill(255 - r, 255 - g, 255 - b)
    stroke(0)
    strokeWeight(2)
    rect(520, 350, 80, 80, 10)

    fill(0)
    noStroke()
    text("Complement", 520, 460)


def drawHSBMode():
    """Demonstrate HSB color space - more intuitive for artists."""
    background(30)

    # Hue wheel
    noStroke()
    centerX = 200
    centerY = 300
    radius = 120

    for angle in range(360):
        h = angle
        fill(h, 100, 100)
        arc(centerX, centerY, radius * 2, radius * 2,
            radians(angle), radians(angle + 2))

    # White center
    fill(0, 0, 100)
    ellipse(centerX, centerY, 80, 80)

    # Labels
    fill(255)
    textSize(14)
    text("Hue Wheel", 160, 450)

    # Saturation gradient
    for x in range(200):
        s = map(x, 0, 200, 0, 100)
        fill(200, s, 100)  # Fixed hue (cyan), varying saturation
        noStroke()
        rect(450 + x, 100, 1, 60)

    fill(255)
    text("Saturation (0-100)", 500, 180)

    # Brightness gradient
    for x in range(200):
        b = map(x, 0, 200, 0, 100)
        fill(200, 100, b)  # Fixed hue and saturation, varying brightness
        noStroke()
        rect(450 + x, 220, 1, 60)

    fill(255)
    text("Brightness (0-100)", 500, 300)

    # Interactive HSB picker
    h = map(mouseX, 0, width, 0, 360)
    s = map(mouseY, 0, height, 100, 0)  # Inverted for intuitive control

    fill(h, s, 90)
    stroke(255)
    strokeWeight(2)
    rect(450, 350, 200, 120, 10)

    fill(255)
    noStroke()
    textSize(14)
    text("H: " + str(int(h)) + " deg", 470, 390)
    text("S: " + str(int(s)) + "%", 470, 410)
    text("B: 90%", 470, 430)
    text("Move mouse to explore", 450, 500)

    # Analogous colors (adjacent on wheel)
    fill(255)
    text("Analogous Colors:", 450, 540)

    for i in range(-2, 3):
        analog_h = (h + i * 30) % 360
        fill(analog_h, s, 90)
        noStroke()
        rect(450 + (i + 2) * 40, 550, 35, 35, 5)


def keyPressed():
    global use_hsb

    if key == 'r':
        use_hsb = False
        print("Switched to RGB mode")

    elif key == 'h':
        use_hsb = True
        print("Switched to HSB mode")

    elif key == 's':
        filename = "color_systems_" + str(frameCount) + ".png"
        save(filename)
        print("Saved:", filename)


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
