"""
Lesson 04: Interactivity
========================

Learn to respond to mouse and keyboard input
to create interactive generative art.

Learning Objectives:
- Handle mouse events and position
- Respond to keyboard input
- Create interactive drawing tools
- Build responsive visual feedback

Run this sketch in Processing with Python Mode enabled.
"""

# Drawing state
strokes = []
current_color = None
brush_size = 20
colors = []

def setup():
    size(800, 600)
    background(250)

    global colors, current_color
    # Art-inspired palette
    colors = [
        color(41, 65, 114),    # Deep blue
        color(193, 84, 55),    # Burnt orange
        color(85, 130, 89),    # Sage green
        color(156, 136, 103),  # Warm gray
        color(180, 60, 60),    # Muted red
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
    drawBrushPreview()
    drawPaletteBar()


def drawBrushPreview():
    """Show current brush at mouse position."""
    # Brush preview (follows mouse)
    noFill()
    stroke(0, 100)
    strokeWeight(1)
    ellipse(mouseX, mouseY, brush_size, brush_size)


def drawPaletteBar():
    """Draw color palette at bottom."""
    bar_height = 40
    swatch_size = 30

    # Background bar
    noStroke()
    fill(240)
    rect(0, height - bar_height, width, bar_height)

    # Color swatches
    for i, c in enumerate(colors):
        x = 20 + i * (swatch_size + 10)
        y = height - bar_height + 5

        # Highlight current color
        if c == current_color:
            stroke(0)
            strokeWeight(3)
        else:
            stroke(150)
            strokeWeight(1)

        fill(c)
        rect(x, y, swatch_size, swatch_size, 5)

    # Brush size indicator
    fill(0)
    noStroke()
    textSize(12)
    text("Size: " + str(brush_size), width - 100, height - 15)

    # Key hints
    fill(100)
    text("Keys: 1-5 color | Up/Down size | c clear | s save", 220, height - 15)


def mouseDragged():
    """Draw while mouse is dragged."""
    # Calculate brush opacity based on speed
    speed = dist(mouseX, mouseY, pmouseX, pmouseY)
    alpha = map(speed, 0, 50, 200, 50)
    alpha = constrain(alpha, 50, 200)

    # Draw brush stroke
    noStroke()
    r = red(current_color)
    g = green(current_color)
    b = blue(current_color)
    fill(r, g, b, alpha)

    # Draw multiple circles for smooth stroke
    steps = int(speed) + 1
    for i in range(steps):
        t = float(i) / steps
        x = lerp(pmouseX, mouseX, t)
        y = lerp(pmouseY, mouseY, t)
        ellipse(x, y, brush_size, brush_size)


def mousePressed():
    """Single click draws a dot."""
    if mouseY < height - 45:  # Not on palette bar
        noStroke()
        r = red(current_color)
        g = green(current_color)
        b = blue(current_color)
        fill(r, g, b, 200)
        ellipse(mouseX, mouseY, brush_size, brush_size)


def keyPressed():
    global current_color, brush_size

    # Number keys for color selection
    if key == '1' and len(colors) >= 1:
        current_color = colors[0]
        print("Color: Deep Blue")
    elif key == '2' and len(colors) >= 2:
        current_color = colors[1]
        print("Color: Burnt Orange")
    elif key == '3' and len(colors) >= 3:
        current_color = colors[2]
        print("Color: Sage Green")
    elif key == '4' and len(colors) >= 4:
        current_color = colors[3]
        print("Color: Warm Gray")
    elif key == '5' and len(colors) >= 5:
        current_color = colors[4]
        print("Color: Muted Red")

    # Arrow keys for brush size
    elif keyCode == UP:
        brush_size = min(brush_size + 5, 100)
        print("Brush size:", brush_size)
    elif keyCode == DOWN:
        brush_size = max(brush_size - 5, 5)
        print("Brush size:", brush_size)

    # Clear canvas
    elif key == 'c':
        background(250)
        print("Canvas cleared")

    # Save image
    elif key == 's':
        filename = "interactive_" + str(frameCount) + ".png"
        save(filename)
        print("Saved:", filename)

    # Show palette info
    elif key == 'p':
        showPaletteInfo()


def showPaletteInfo():
    """Display palette information overlay."""
    # Semi-transparent overlay
    fill(255, 230)
    noStroke()
    rect(50, 50, 300, 200, 10)

    fill(0)
    textSize(16)
    text("Current Palette", 70, 80)

    textSize(12)
    names = ["Deep Blue", "Burnt Orange", "Sage Green", "Warm Gray", "Muted Red"]
    for i, (c, name) in enumerate(zip(colors, names)):
        y = 110 + i * 30

        fill(c)
        noStroke()
        rect(70, y - 15, 20, 20, 3)

        fill(0)
        text(name, 100, y)

        # RGB values
        fill(100)
        text("RGB(" + str(int(red(c))) + ", " + str(int(green(c))) + ", " + str(int(blue(c))) + ")", 200, y)


# -------------------------------------------------
# Interactivity Tips:
#
# Mouse variables:
# - mouseX, mouseY: Current position
# - pmouseX, pmouseY: Previous frame position
# - mousePressed: Boolean, is mouse down?
#
# Keyboard:
# - key: The character pressed
# - keyCode: Special keys (UP, DOWN, LEFT, RIGHT)
#
# Events:
# - mousePressed(): Called once on click
# - mouseDragged(): Called while dragging
# - mouseReleased(): Called when released
# - keyPressed(): Called once per key press
# -------------------------------------------------
