"""
Lesson 11: Artist Style Generation
===================================

Generate art inspired by specific artists' color palettes
and brushwork characteristics from renoir analysis.

Learning Objectives:
- Load artist palettes from renoir exports
- Simulate artist-specific brushwork
- Combine color and technique parameters
- Create homages to master artists

Run this sketch in Processing with Python Mode enabled.
"""

import json

# Artist data
artists = {}
current_artist = "monet"

# Canvas state
strokes = []


def setup():
    size(800, 600)
    initializeArtists()
    setBackground()

    print("Lesson 11: Artist Style Generation")
    print("\nControls:")
    print("  Press 1-4 to switch artists")
    print("  Click and drag to paint")
    print("  Press 'g' to auto-generate")
    print("  Press 'c' to clear")
    print("  Press 's' to save image")


def initializeArtists():
    """Initialize artist profiles with palettes and styles."""

    # Claude Monet - Water Lilies period
    artists["monet"] = {
        "name": "Claude Monet",
        "period": "Impressionism",
        "palette": [
            color(142, 178, 197),  # Sky reflection
            color(89, 112, 95),    # Lily pad green
            color(176, 166, 198),  # Water lavender
            color(185, 157, 137),  # Warm undertone
            color(112, 145, 128),  # Deep water green
        ],
        "stroke_length": (10, 25),
        "stroke_width": (3, 8),
        "direction": "horizontal",
        "opacity": 180,
        "overlap": True
    }

    # Vincent van Gogh - Starry Night period
    artists["vangogh"] = {
        "name": "Vincent van Gogh",
        "period": "Post-Impressionism",
        "palette": [
            color(25, 55, 95),     # Night blue
            color(60, 90, 140),    # Sky blue
            color(230, 200, 80),   # Star yellow
            color(40, 70, 50),     # Cypress green
            color(120, 100, 80),   # Earth brown
        ],
        "stroke_length": (15, 35),
        "stroke_width": (4, 10),
        "direction": "swirl",
        "opacity": 220,
        "overlap": True
    }

    # Georges Seurat - Pointillism
    artists["seurat"] = {
        "name": "Georges Seurat",
        "period": "Neo-Impressionism",
        "palette": [
            color(180, 200, 220),  # Sky blue
            color(140, 170, 120),  # Green
            color(200, 180, 140),  # Sand
            color(190, 140, 120),  # Skin tone
            color(80, 100, 140),   # Shadow blue
        ],
        "stroke_length": (3, 6),
        "stroke_width": (3, 6),
        "direction": "point",
        "opacity": 200,
        "overlap": False
    }

    # Piet Mondrian - De Stijl
    artists["mondrian"] = {
        "name": "Piet Mondrian",
        "period": "De Stijl",
        "palette": [
            color(255, 0, 0),      # Primary red
            color(0, 0, 255),      # Primary blue
            color(255, 255, 0),    # Primary yellow
            color(255, 255, 255),  # White
            color(0, 0, 0),        # Black
        ],
        "stroke_length": (50, 150),
        "stroke_width": (20, 60),
        "direction": "grid",
        "opacity": 255,
        "overlap": False
    }


def draw():
    drawUI()


def drawUI():
    """Draw artist info panel."""
    a = artists[current_artist]

    # Info panel
    fill(255, 240)
    noStroke()
    rect(10, 10, 220, 95, 5)

    fill(0)
    textSize(14)
    text(a["name"], 20, 32)

    textSize(11)
    fill(80)
    text(a["period"], 20, 50)
    text("Style: " + a["direction"], 20, 68)

    # Palette swatches
    for i, c in enumerate(a["palette"]):
        fill(c)
        noStroke()
        rect(20 + i * 22, 78, 18, 12, 2)


def mouseDragged():
    """Paint in the current artist's style."""
    a = artists[current_artist]
    drawArtistStroke(mouseX, mouseY, a)


def drawArtistStroke(x, y, artist):
    """Draw a stroke in the artist's characteristic style."""
    palette = artist["palette"]
    col = palette[int(random(len(palette)))]
    min_len, max_len = artist["stroke_length"]
    min_w, max_w = artist["stroke_width"]
    direction = artist["direction"]
    alpha = artist["opacity"]

    if direction == "horizontal":
        # Monet-style horizontal water strokes
        drawHorizontalStroke(x, y, col, min_len, max_len, min_w, max_w, alpha)

    elif direction == "swirl":
        # Van Gogh-style swirling strokes
        drawSwirlStroke(x, y, col, min_len, max_len, min_w, max_w, alpha)

    elif direction == "point":
        # Seurat-style pointillist dots
        drawPointStroke(x, y, col, min_len, max_len, alpha)

    elif direction == "grid":
        # Mondrian-style geometric blocks
        drawGridStroke(x, y, col, min_len, max_len, min_w, max_w)


def drawHorizontalStroke(x, y, col, min_len, max_len, min_w, max_w, alpha):
    """Impressionist horizontal brushstroke."""
    for _ in range(2):
        px = x + random(-10, 10)
        py = y + random(-10, 10)

        stroke(red(col), green(col), blue(col), alpha)
        strokeWeight(random(min_w, max_w))
        strokeCap(ROUND)

        length = random(min_len, max_len)
        # Slight wave
        y_offset = sin(px * 0.1) * 3
        line(px - length/2, py + y_offset, px + length/2, py - y_offset)


def drawSwirlStroke(x, y, col, min_len, max_len, min_w, max_w, alpha):
    """Expressive swirling brushstroke."""
    angle = noise(x * 0.01, y * 0.01) * TWO_PI * 2

    stroke(red(col), green(col), blue(col), alpha)
    strokeWeight(random(min_w, max_w))
    strokeCap(ROUND)

    length = random(min_len, max_len)
    x2 = x + cos(angle) * length
    y2 = y + sin(angle) * length

    # Curved stroke using bezier
    cx1 = x + cos(angle + PI/4) * length/2
    cy1 = y + sin(angle + PI/4) * length/2

    noFill()
    beginShape()
    vertex(x, y)
    quadraticVertex(cx1, cy1, x2, y2)
    endShape()


def drawPointStroke(x, y, col, min_size, max_size, alpha):
    """Pointillist dot application."""
    for _ in range(5):
        px = x + random(-15, 15)
        py = y + random(-15, 15)

        # Slight color variation for optical mixing
        r = constrain(red(col) + random(-30, 30), 0, 255)
        g = constrain(green(col) + random(-30, 30), 0, 255)
        b = constrain(blue(col) + random(-30, 30), 0, 255)

        noStroke()
        fill(r, g, b, alpha)
        size = random(min_size, max_size)
        ellipse(px, py, size, size)


def drawGridStroke(x, y, col, min_len, max_len, min_w, max_w):
    """Geometric grid-aligned block."""
    # Snap to grid
    grid_size = 40
    gx = int(x / grid_size) * grid_size
    gy = int(y / grid_size) * grid_size

    noStroke()
    fill(col)

    w = random(min_w, max_w)
    h = random(min_w, max_w)
    rect(gx, gy, w, h)


def autoGenerate():
    """Auto-generate a complete composition."""
    a = artists[current_artist]
    setBackground()

    if current_artist == "mondrian":
        # Special handling for Mondrian's grid style
        generateMondrian(a)
    else:
        # Organic generation for others
        for _ in range(500):
            x = random(width)
            y = random(height)
            drawArtistStroke(x, y, a)


def generateMondrian(artist):
    """Generate a Mondrian-style composition."""
    # Black grid lines
    stroke(0)
    strokeWeight(8)

    # Vertical lines
    for _ in range(3):
        x = random(100, width - 100)
        line(x, 0, x, height)

    # Horizontal lines
    for _ in range(3):
        y = random(100, height - 100)
        line(0, y, width, y)

    # Fill some rectangles with color
    noStroke()
    for _ in range(5):
        x = random(width)
        y = random(height)
        w = random(50, 200)
        h = random(50, 200)
        fill(artist["palette"][int(random(4))])
        rect(x, y, w, h)


def setBackground():
    """Set background based on artist."""
    if current_artist == "vangogh":
        background(25, 35, 55)
    elif current_artist == "mondrian":
        background(250)
    else:
        background(240)


def keyPressed():
    global current_artist

    if key == '1':
        current_artist = "monet"
        setBackground()
        print("Artist: Claude Monet")

    elif key == '2':
        current_artist = "vangogh"
        setBackground()
        print("Artist: Vincent van Gogh")

    elif key == '3':
        current_artist = "seurat"
        setBackground()
        print("Artist: Georges Seurat")

    elif key == '4':
        current_artist = "mondrian"
        setBackground()
        print("Artist: Piet Mondrian")

    elif key == 'g':
        autoGenerate()
        print("Auto-generated composition")

    elif key == 'c':
        setBackground()
        print("Canvas cleared")

    elif key == 's':
        filename = current_artist + "_" + str(frameCount) + ".png"
        save(filename)
        print("Saved:", filename)


# -------------------------------------------------
# Artist Style Parameters (derived from renoir):
#
# Monet:
# - Horizontal strokes suggest water reflections
# - Muted blues, greens, lavenders
# - Overlapping for depth
#
# Van Gogh:
# - Swirling, energetic brushwork
# - Thick impasto effect
# - Strong yellows and blues
#
# Seurat:
# - Small dots of pure color
# - Optical color mixing
# - Scientific approach to color
#
# Mondrian:
# - Grid-based composition
# - Primary colors only
# - Balance through asymmetry
#
# To use renoir palettes:
# 1. Export with palette_exporter.py
# 2. Place JSON in data/ folder
# 3. Load in setup() using json.load()
# -------------------------------------------------
