"""
Lesson 11: Artist Style Generation (py5 version)
=================================================

Generate art inspired by specific artists' color palettes
and brushwork characteristics from renoir analysis.

Learning Objectives:
- Load artist palettes from renoir exports
- Simulate artist-specific brushwork
- Combine color and technique parameters
- Create homages to master artists

Run with: python artist_style_py5.py
"""

import py5

# Artist data
artists = {}
current_artist = "monet"


def setup():
    py5.size(800, 600)
    initialize_artists()
    set_background()

    print("Lesson 11: Artist Style Generation")
    print("\nControls:")
    print("  Press 1-4 to switch artists")
    print("  Click and drag to paint")
    print("  Press 'g' to auto-generate")
    print("  Press 'c' to clear")
    print("  Press 's' to save image")


def initialize_artists():
    """Initialize artist profiles with palettes and styles."""

    # Claude Monet - Water Lilies period
    artists["monet"] = {
        "name": "Claude Monet",
        "period": "Impressionism",
        "palette": [
            py5.color(142, 178, 197),  # Sky reflection
            py5.color(89, 112, 95),    # Lily pad green
            py5.color(176, 166, 198),  # Water lavender
            py5.color(185, 157, 137),  # Warm undertone
            py5.color(112, 145, 128),  # Deep water green
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
            py5.color(25, 55, 95),     # Night blue
            py5.color(60, 90, 140),    # Sky blue
            py5.color(230, 200, 80),   # Star yellow
            py5.color(40, 70, 50),     # Cypress green
            py5.color(120, 100, 80),   # Earth brown
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
            py5.color(180, 200, 220),  # Sky blue
            py5.color(140, 170, 120),  # Green
            py5.color(200, 180, 140),  # Sand
            py5.color(190, 140, 120),  # Skin tone
            py5.color(80, 100, 140),   # Shadow blue
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
            py5.color(255, 0, 0),      # Primary red
            py5.color(0, 0, 255),      # Primary blue
            py5.color(255, 255, 0),    # Primary yellow
            py5.color(255, 255, 255),  # White
            py5.color(0, 0, 0),        # Black
        ],
        "stroke_length": (50, 150),
        "stroke_width": (20, 60),
        "direction": "grid",
        "opacity": 255,
        "overlap": False
    }


def draw():
    draw_ui()


def draw_ui():
    """Draw artist info panel."""
    a = artists[current_artist]

    # Info panel
    py5.fill(255, 240)
    py5.no_stroke()
    py5.rect(10, 10, 220, 95, 5)

    py5.fill(0)
    py5.text_size(14)
    py5.text(a["name"], 20, 32)

    py5.text_size(11)
    py5.fill(80)
    py5.text(a["period"], 20, 50)
    py5.text(f"Style: {a['direction']}", 20, 68)

    # Palette swatches
    for i, c in enumerate(a["palette"]):
        py5.fill(c)
        py5.no_stroke()
        py5.rect(20 + i * 22, 78, 18, 12, 2)


def mouse_dragged():
    """Paint in the current artist's style."""
    a = artists[current_artist]
    draw_artist_stroke(py5.mouse_x, py5.mouse_y, a)


def draw_artist_stroke(x, y, artist):
    """Draw a stroke in the artist's characteristic style."""
    palette = artist["palette"]
    col = palette[int(py5.random(len(palette)))]
    min_len, max_len = artist["stroke_length"]
    min_w, max_w = artist["stroke_width"]
    direction = artist["direction"]
    alpha = artist["opacity"]

    if direction == "horizontal":
        draw_horizontal_stroke(x, y, col, min_len, max_len, min_w, max_w, alpha)
    elif direction == "swirl":
        draw_swirl_stroke(x, y, col, min_len, max_len, min_w, max_w, alpha)
    elif direction == "point":
        draw_point_stroke(x, y, col, min_len, max_len, alpha)
    elif direction == "grid":
        draw_grid_stroke(x, y, col, min_len, max_len, min_w, max_w)


def draw_horizontal_stroke(x, y, col, min_len, max_len, min_w, max_w, alpha):
    """Impressionist horizontal brushstroke."""
    for _ in range(2):
        px = x + py5.random(-10, 10)
        py_val = y + py5.random(-10, 10)

        py5.stroke(py5.red(col), py5.green(col), py5.blue(col), alpha)
        py5.stroke_weight(py5.random(min_w, max_w))
        py5.stroke_cap(py5.ROUND)

        length = py5.random(min_len, max_len)
        # Slight wave
        y_offset = py5.sin(px * 0.1) * 3
        py5.line(px - length/2, py_val + y_offset, px + length/2, py_val - y_offset)


def draw_swirl_stroke(x, y, col, min_len, max_len, min_w, max_w, alpha):
    """Expressive swirling brushstroke."""
    angle = py5.noise(x * 0.01, y * 0.01) * py5.TWO_PI * 2

    py5.stroke(py5.red(col), py5.green(col), py5.blue(col), alpha)
    py5.stroke_weight(py5.random(min_w, max_w))
    py5.stroke_cap(py5.ROUND)

    length = py5.random(min_len, max_len)
    x2 = x + py5.cos(angle) * length
    y2 = y + py5.sin(angle) * length

    # Curved stroke using bezier
    cx1 = x + py5.cos(angle + py5.PI/4) * length/2
    cy1 = y + py5.sin(angle + py5.PI/4) * length/2

    py5.no_fill()
    py5.begin_shape()
    py5.vertex(x, y)
    py5.quadratic_vertex(cx1, cy1, x2, y2)
    py5.end_shape()


def draw_point_stroke(x, y, col, min_size, max_size, alpha):
    """Pointillist dot application."""
    for _ in range(5):
        px = x + py5.random(-15, 15)
        py_val = y + py5.random(-15, 15)

        # Slight color variation for optical mixing
        r = py5.constrain(py5.red(col) + py5.random(-30, 30), 0, 255)
        g = py5.constrain(py5.green(col) + py5.random(-30, 30), 0, 255)
        b = py5.constrain(py5.blue(col) + py5.random(-30, 30), 0, 255)

        py5.no_stroke()
        py5.fill(r, g, b, alpha)
        size = py5.random(min_size, max_size)
        py5.ellipse(px, py_val, size, size)


def draw_grid_stroke(x, y, col, min_len, max_len, min_w, max_w):
    """Geometric grid-aligned block."""
    # Snap to grid
    grid_size = 40
    gx = int(x / grid_size) * grid_size
    gy = int(y / grid_size) * grid_size

    py5.no_stroke()
    py5.fill(col)

    w = py5.random(min_w, max_w)
    h = py5.random(min_w, max_w)
    py5.rect(gx, gy, w, h)


def auto_generate():
    """Auto-generate a complete composition."""
    a = artists[current_artist]
    set_background()

    if current_artist == "mondrian":
        generate_mondrian(a)
    else:
        for _ in range(500):
            x = py5.random(py5.width)
            y = py5.random(py5.height)
            draw_artist_stroke(x, y, a)


def generate_mondrian(artist):
    """Generate a Mondrian-style composition."""
    # Black grid lines
    py5.stroke(0)
    py5.stroke_weight(8)

    # Vertical lines
    for _ in range(3):
        x = py5.random(100, py5.width - 100)
        py5.line(x, 0, x, py5.height)

    # Horizontal lines
    for _ in range(3):
        y = py5.random(100, py5.height - 100)
        py5.line(0, y, py5.width, y)

    # Fill some rectangles with color
    py5.no_stroke()
    for _ in range(5):
        x = py5.random(py5.width)
        y = py5.random(py5.height)
        w = py5.random(50, 200)
        h = py5.random(50, 200)
        py5.fill(artist["palette"][int(py5.random(4))])
        py5.rect(x, y, w, h)


def set_background():
    """Set background based on artist."""
    if current_artist == "vangogh":
        py5.background(25, 35, 55)
    elif current_artist == "mondrian":
        py5.background(250)
    else:
        py5.background(240)


def key_pressed():
    global current_artist

    if py5.key == '1':
        current_artist = "monet"
        set_background()
        print("Artist: Claude Monet")

    elif py5.key == '2':
        current_artist = "vangogh"
        set_background()
        print("Artist: Vincent van Gogh")

    elif py5.key == '3':
        current_artist = "seurat"
        set_background()
        print("Artist: Georges Seurat")

    elif py5.key == '4':
        current_artist = "mondrian"
        set_background()
        print("Artist: Piet Mondrian")

    elif py5.key == 'g':
        auto_generate()
        print("Auto-generated composition")

    elif py5.key == 'c':
        set_background()
        print("Canvas cleared")

    elif py5.key == 's':
        filename = f"{current_artist}_{py5.frame_count}.png"
        py5.save(filename)
        print(f"Saved: {filename}")


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

py5.run_sketch()
