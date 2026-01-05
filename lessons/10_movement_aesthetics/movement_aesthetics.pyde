"""
Lesson 10: Movement Aesthetics
==============================

Explore how different art movements use color differently.
Compare Impressionism, Expressionism, and other styles.

Learning Objectives:
- Understand color characteristics of art movements
- Generate art in different movement styles
- Use renoir data to inform generative choices
- Compare warm/cool ratios and saturation levels

Run this sketch in Processing with Python Mode enabled.
"""

import json

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
brushstrokes = []


def setup():
    size(800, 600)
    initializePalettes()

    print("Lesson 10: Movement Aesthetics")
    print("\nControls:")
    print("  Press 1-4 to switch movements")
    print("  Click and drag to paint")
    print("  Press 'c' to clear")
    print("  Press 's' to save image")


def initializePalettes():
    """Initialize palettes for each movement."""
    # Impressionism: Light, airy colors
    movements["impressionism"]["palette"] = [
        color(142, 178, 197),  # Sky blue
        color(216, 191, 161),  # Warm beige
        color(168, 199, 168),  # Soft green
        color(230, 210, 180),  # Light cream
        color(180, 160, 200),  # Lavender
    ]

    # Expressionism: Bold, emotional colors
    movements["expressionism"]["palette"] = [
        color(200, 50, 50),    # Deep red
        color(50, 50, 150),    # Dark blue
        color(220, 180, 50),   # Intense yellow
        color(30, 100, 30),    # Dark green
        color(150, 50, 150),   # Purple
    ]

    # Tonalism: Muted, atmospheric
    movements["tonalism"]["palette"] = [
        color(120, 115, 100),  # Warm gray
        color(100, 110, 120),  # Cool gray
        color(130, 120, 110),  # Taupe
        color(90, 95, 100),    # Slate
        color(110, 105, 95),   # Stone
    ]

    # Fauvism: Pure, saturated colors
    movements["fauvism"]["palette"] = [
        color(255, 50, 50),    # Pure red
        color(50, 200, 50),    # Pure green
        color(50, 50, 255),    # Pure blue
        color(255, 200, 0),    # Bright yellow
        color(255, 100, 200),  # Hot pink
    ]


def draw():
    # Don't clear - allow painting to accumulate
    drawUI()


def drawUI():
    """Draw movement info panel."""
    m = movements[current_movement]

    # Info panel
    fill(255, 240)
    noStroke()
    rect(10, 10, 250, 90, 5)

    fill(0)
    textSize(16)
    text(m["name"], 20, 35)

    textSize(11)
    fill(80)
    text(m["description"], 20, 55)
    text("Saturation: " + str(int(m["saturation"] * 100)) + "%", 20, 75)
    text("Style: " + m["stroke_style"], 130, 75)

    # Palette swatches
    for i, c in enumerate(m["palette"]):
        fill(c)
        noStroke()
        rect(20 + i * 25, 82, 20, 12, 2)


def mouseDragged():
    """Paint in the current movement's style."""
    m = movements[current_movement]
    palette = m["palette"]
    style = m["stroke_style"]

    # Pick random color from palette
    col = palette[int(random(len(palette)))]

    if style == "short":
        # Impressionist: Short, broken strokes
        drawImpressionistStroke(mouseX, mouseY, col)

    elif style == "bold":
        # Expressionist: Bold, angular strokes
        drawExpressionistStroke(mouseX, mouseY, col)

    elif style == "soft":
        # Tonalist: Soft, blended strokes
        drawTonalistStroke(mouseX, mouseY, col)

    elif style == "wild":
        # Fauvist: Wild, energetic strokes
        drawFauvistStroke(mouseX, mouseY, col)


def drawImpressionistStroke(x, y, col):
    """Short, dabbed strokes with light variation."""
    for _ in range(3):
        px = x + random(-15, 15)
        py = y + random(-15, 15)

        # Slight color variation
        r = red(col) + random(-20, 20)
        g = green(col) + random(-20, 20)
        b = blue(col) + random(-20, 20)

        noStroke()
        fill(r, g, b, 180)

        # Short dabs
        angle = random(TWO_PI)
        pushMatrix()
        translate(px, py)
        rotate(angle)
        ellipse(0, 0, random(8, 15), random(4, 8))
        popMatrix()


def drawExpressionistStroke(x, y, col):
    """Bold, angular, emotional strokes."""
    stroke(col)
    strokeWeight(random(4, 10))
    strokeCap(SQUARE)

    # Angular direction
    angle = noise(x * 0.01, y * 0.01) * TWO_PI
    length = random(20, 40)

    x2 = x + cos(angle) * length
    y2 = y + sin(angle) * length

    line(x, y, x2, y2)


def drawTonalistStroke(x, y, col):
    """Soft, atmospheric, blended strokes."""
    noStroke()

    # Very transparent, layered
    r = red(col)
    g = green(col)
    b = blue(col)
    fill(r, g, b, 30)

    # Soft, large circles
    for i in range(3):
        size = random(30, 60)
        px = x + random(-10, 10)
        py = y + random(-10, 10)
        ellipse(px, py, size, size)


def drawFauvistStroke(x, y, col):
    """Wild, energetic, pure color strokes."""
    stroke(col)
    strokeWeight(random(5, 12))
    strokeCap(ROUND)

    # Energetic, varied direction
    angle = random(TWO_PI)
    length = random(15, 35)

    x2 = x + cos(angle) * length
    y2 = y + sin(angle) * length

    line(x, y, x2, y2)

    # Sometimes add complementary splashes
    if random(1) > 0.7:
        noStroke()
        fill(255 - red(col), 255 - green(col), 255 - blue(col), 200)
        ellipse(x + random(-20, 20), y + random(-20, 20), 8, 8)


def keyPressed():
    global current_movement

    if key == '1':
        current_movement = "impressionism"
        setBackground()
        print("Movement: Impressionism")

    elif key == '2':
        current_movement = "expressionism"
        setBackground()
        print("Movement: Expressionism")

    elif key == '3':
        current_movement = "tonalism"
        setBackground()
        print("Movement: Tonalism")

    elif key == '4':
        current_movement = "fauvism"
        setBackground()
        print("Movement: Fauvism")

    elif key == 'c':
        setBackground()
        print("Canvas cleared")

    elif key == 's':
        filename = current_movement + "_" + str(frameCount) + ".png"
        save(filename)
        print("Saved:", filename)


def setBackground():
    """Set background appropriate to movement."""
    m = movements[current_movement]
    if current_movement == "tonalism":
        background(180, 175, 165)
    elif current_movement == "expressionism":
        background(30)
    else:
        background(245)


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

setBackground()
