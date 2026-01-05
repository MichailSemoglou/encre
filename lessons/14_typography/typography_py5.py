"""
Lesson 14: Typography in Generative Art (py5 version)
=====================================================

Explore creative typography using text as
a generative medium.

Learning Objectives:
- Draw and style text
- Use text as visual elements
- Create kinetic typography
- Build text-based compositions

Run with: python typography_py5.py
"""

import py5

# Mode control
mode = 0
modes = ["Basic", "Circular", "Wave", "Particles", "ASCII Art"]

# Animation
t = 0

# Text content
quote = "Art is not what you see, but what you make others see."
author = "- Edgar Degas"

# Particles for mode 3
text_particles = []

# Palette
palette = []


def setup():
    global palette

    py5.size(800, 600)

    palette = [
        py5.color(41, 65, 114),
        py5.color(193, 84, 55),
        py5.color(85, 130, 89),
        py5.color(156, 136, 103),
        py5.color(180, 60, 60),
    ]

    init_text_particles()

    print("Lesson 14: Typography")
    print("\nControls:")
    print("  Press 1-5 to switch modes")
    print("  Press 's' to save image")


def init_text_particles():
    """Create particles from text characters."""
    global text_particles
    text_particles = []

    phrase = "GENERATIVE"
    char_size = 60
    start_x = 100
    start_y = 300

    for i, char in enumerate(phrase):
        text_particles.append({
            'char': char,
            'home_x': start_x + i * char_size,
            'home_y': start_y,
            'x': start_x + i * char_size,
            'y': start_y,
            'vx': 0,
            'vy': 0,
            'col': palette[i % len(palette)]
        })


def draw():
    global t
    t += 0.02

    if mode == 0:
        draw_basic_typography()
    elif mode == 1:
        draw_circular_text()
    elif mode == 2:
        draw_wave_text()
    elif mode == 3:
        draw_text_particles()
    elif mode == 4:
        draw_ascii_art()

    # Mode indicator
    py5.fill(0)
    py5.text_size(12)
    py5.text_align(py5.LEFT)
    py5.text(f"Mode: {modes[mode]} (Press 1-5)", 20, 25)


def draw_basic_typography():
    """Basic styled text display."""
    py5.background(250)

    # Title
    py5.fill(palette[0])
    py5.text_size(48)
    py5.text_align(py5.CENTER)
    py5.text("Typography", py5.width/2, 150)

    # Quote
    py5.fill(60)
    py5.text_size(24)
    py5.text_leading(36)
    py5.text(quote, py5.width/2 - 250, 250, 500, 200)

    # Author
    py5.fill(palette[1])
    py5.text_size(18)
    py5.text(author, py5.width/2, 420)

    # Decorative elements
    py5.no_fill()
    py5.stroke(palette[2], 150)
    py5.stroke_weight(2)
    py5.line(200, 180, 600, 180)
    py5.line(200, 450, 600, 450)

    # Letter showcase
    py5.no_stroke()
    sizes = [72, 60, 48, 36, 24]
    for i, s in enumerate(sizes):
        py5.fill(palette[i % len(palette)])
        py5.text_size(s)
        py5.text("Aa", 100 + i * 130, 550)


def draw_circular_text():
    """Text arranged in a circle."""
    py5.background(30)

    phrase = "PROCESSING * PYTHON * GENERATIVE * ART * "
    radius = 200
    cx = py5.width / 2
    cy = py5.height / 2

    py5.text_size(16)
    py5.text_align(py5.CENTER)

    for i, char in enumerate(phrase):
        angle = py5.remap(i, 0, len(phrase), 0, py5.TWO_PI) + t
        x = cx + py5.cos(angle) * radius
        y = cy + py5.sin(angle) * radius

        py5.push_matrix()
        py5.translate(x, y)
        py5.rotate(angle + py5.HALF_PI)

        py5.fill(py5.lerp_color(palette[0], palette[1], (py5.sin(angle + t) + 1) / 2))
        py5.text(char, 0, 0)
        py5.pop_matrix()

    # Inner circle with different text
    inner_phrase = "ART * CODE * "
    inner_radius = 100

    py5.text_size(14)
    for i, char in enumerate(inner_phrase):
        angle = py5.remap(i, 0, len(inner_phrase), 0, py5.TWO_PI) - t * 0.5
        x = cx + py5.cos(angle) * inner_radius
        y = cy + py5.sin(angle) * inner_radius

        py5.push_matrix()
        py5.translate(x, y)
        py5.rotate(angle + py5.HALF_PI)

        py5.fill(palette[2])
        py5.text(char, 0, 0)
        py5.pop_matrix()


def draw_wave_text():
    """Text with wave animation."""
    py5.background(245)

    phrase = "The purpose of art is washing the dust of daily life off our souls."
    words = phrase.split()

    py5.text_align(py5.CENTER)
    py5.text_size(28)

    x_offset = 50
    y_base = py5.height / 2

    for i, word in enumerate(words):
        wave = py5.sin(t * 2 + i * 0.5) * 30
        col = py5.lerp_color(palette[0], palette[3], i / float(len(words)))
        py5.fill(col)

        word_width = py5.text_width(word + " ")
        py5.text(word, x_offset + word_width/2, y_base + wave)
        x_offset += word_width

        if x_offset > py5.width - 100:
            x_offset = 50
            y_base += 50

    py5.fill(100)
    py5.text_size(14)
    py5.text("- Pablo Picasso", py5.width/2, py5.height - 50)


def draw_text_particles():
    """Interactive text particles."""
    py5.background(250)

    py5.text_size(60)
    py5.text_align(py5.CENTER, py5.CENTER)

    for p in text_particles:
        dx = py5.mouse_x - p['x']
        dy = py5.mouse_y - p['y']
        dist_val = py5.sqrt(dx * dx + dy * dy)

        if dist_val < 150:
            force = (150 - dist_val) / 150
            p['vx'] -= dx * force * 0.1
            p['vy'] -= dy * force * 0.1

        p['vx'] += (p['home_x'] - p['x']) * 0.05
        p['vy'] += (p['home_y'] - p['y']) * 0.05

        p['vx'] *= 0.9
        p['vy'] *= 0.9

        p['x'] += p['vx']
        p['y'] += p['vy']

        py5.fill(p['col'])
        py5.text(p['char'], p['x'], p['y'])

    py5.fill(100)
    py5.text_size(14)
    py5.text_align(py5.LEFT)
    py5.text("Move mouse near letters to interact", 20, py5.height - 30)


def draw_ascii_art():
    """ASCII art style rendering."""
    py5.background(20)

    chars = " .:-=+*#%@"
    cell_size = 12

    py5.text_size(cell_size)
    py5.text_align(py5.CENTER, py5.CENTER)
    py5.fill(0, 255, 0)

    for y in range(0, py5.height, cell_size):
        for x in range(0, py5.width, cell_size):
            n = py5.noise(x * 0.02, y * 0.02, t)
            char_index = int(n * len(chars))
            char_index = py5.constrain(char_index, 0, len(chars) - 1)

            py5.text(chars[char_index], x + cell_size/2, y + cell_size/2)

    py5.fill(0, 200)
    py5.no_stroke()
    py5.rect(py5.width/2 - 150, py5.height/2 - 40, 300, 80, 10)

    py5.fill(0, 255, 0)
    py5.text_size(32)
    py5.text("ASCII ART", py5.width/2, py5.height/2)


def key_pressed():
    global mode

    if py5.key == '1':
        mode = 0
    elif py5.key == '2':
        mode = 1
    elif py5.key == '3':
        mode = 2
    elif py5.key == '4':
        mode = 3
        init_text_particles()
    elif py5.key == '5':
        mode = 4
    elif py5.key == 's':
        filename = f"typography_{py5.frame_count}.png"
        py5.save(filename)
        print(f"Saved: {filename}")


# -------------------------------------------------
# Typography Concepts:
#
# Text Functions:
# - py5.text(str, x, y) - Draw text
# - py5.text_size(size) - Set font size
# - py5.text_align(h, v) - Alignment
# - py5.text_width(str) - Get width
# - py5.text_leading(size) - Line spacing
#
# Creative Approaches:
# 1. Circular text: Position along arc
# 2. Wave text: Animate y with sine
# 3. Particle text: Each char is a particle
# 4. ASCII art: Map values to characters
# -------------------------------------------------

py5.run_sketch()
