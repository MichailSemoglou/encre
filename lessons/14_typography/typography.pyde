"""
Lesson 14: Typography in Generative Art
=======================================

Explore creative typography using text as
a generative medium.

Learning Objectives:
- Draw and style text
- Use text as visual elements
- Create kinetic typography
- Build text-based compositions

Run this sketch in Processing with Python Mode enabled.
"""

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

    size(800, 600)

    palette = [
        color(41, 65, 114),
        color(193, 84, 55),
        color(85, 130, 89),
        color(156, 136, 103),
        color(180, 60, 60),
    ]

    initTextParticles()

    print("Lesson 14: Typography")
    print("\nControls:")
    print("  Press 1-5 to switch modes")
    print("  Press 's' to save image")


def initTextParticles():
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
        drawBasicTypography()
    elif mode == 1:
        drawCircularText()
    elif mode == 2:
        drawWaveText()
    elif mode == 3:
        drawTextParticles()
    elif mode == 4:
        drawASCIIArt()

    # Mode indicator
    fill(0)
    textSize(12)
    textAlign(LEFT)
    text("Mode: " + modes[mode] + " (Press 1-5)", 20, 25)


def drawBasicTypography():
    """Basic styled text display."""
    background(250)

    # Title
    fill(palette[0])
    textSize(48)
    textAlign(CENTER)
    text("Typography", width/2, 150)

    # Quote
    fill(60)
    textSize(24)
    textLeading(36)
    text(quote, width/2 - 250, 250, 500, 200)

    # Author
    fill(palette[1])
    textSize(18)
    text(author, width/2, 420)

    # Decorative elements
    noFill()
    stroke(palette[2], 150)
    strokeWeight(2)
    line(200, 180, 600, 180)
    line(200, 450, 600, 450)

    # Letter showcase
    noStroke()
    sizes = [72, 60, 48, 36, 24]
    for i, s in enumerate(sizes):
        fill(palette[i % len(palette)])
        textSize(s)
        text("Aa", 100 + i * 130, 550)


def drawCircularText():
    """Text arranged in a circle."""
    background(30)

    phrase = "PROCESSING * PYTHON * GENERATIVE * ART * "
    radius = 200
    cx = width / 2
    cy = height / 2

    textSize(16)
    textAlign(CENTER)

    for i, char in enumerate(phrase):
        angle = map(i, 0, len(phrase), 0, TWO_PI) + t
        x = cx + cos(angle) * radius
        y = cy + sin(angle) * radius

        pushMatrix()
        translate(x, y)
        rotate(angle + HALF_PI)

        fill(lerpColor(palette[0], palette[1], (sin(angle + t) + 1) / 2))
        text(char, 0, 0)
        popMatrix()

    # Inner circle with different text
    inner_phrase = "ART * CODE * "
    inner_radius = 100

    textSize(14)
    for i, char in enumerate(inner_phrase):
        angle = map(i, 0, len(inner_phrase), 0, TWO_PI) - t * 0.5
        x = cx + cos(angle) * inner_radius
        y = cy + sin(angle) * inner_radius

        pushMatrix()
        translate(x, y)
        rotate(angle + HALF_PI)

        fill(palette[2])
        text(char, 0, 0)
        popMatrix()


def drawWaveText():
    """Text with wave animation."""
    background(245)

    phrase = "The purpose of art is washing the dust of daily life off our souls."
    words = phrase.split()

    textAlign(CENTER)
    textSize(28)

    x_offset = 50
    y_base = height / 2

    for i, word in enumerate(words):
        # Calculate wave offset
        wave = sin(t * 2 + i * 0.5) * 30

        # Color based on position
        col = lerpColor(palette[0], palette[3], i / float(len(words)))
        fill(col)

        # Draw word
        word_width = textWidth(word + " ")
        text(word, x_offset + word_width/2, y_base + wave)
        x_offset += word_width

        # Wrap to next line
        if x_offset > width - 100:
            x_offset = 50
            y_base += 50

    # Attribution
    fill(100)
    textSize(14)
    text("- Pablo Picasso", width/2, height - 50)


def drawTextParticles():
    """Interactive text particles."""
    background(250)

    textSize(60)
    textAlign(CENTER, CENTER)

    for p in text_particles:
        # Calculate distance to mouse
        dx = mouseX - p['x']
        dy = mouseY - p['y']
        dist_val = sqrt(dx * dx + dy * dy)

        # Repel from mouse
        if dist_val < 150:
            force = (150 - dist_val) / 150
            p['vx'] -= dx * force * 0.1
            p['vy'] -= dy * force * 0.1

        # Spring back to home
        p['vx'] += (p['home_x'] - p['x']) * 0.05
        p['vy'] += (p['home_y'] - p['y']) * 0.05

        # Damping
        p['vx'] *= 0.9
        p['vy'] *= 0.9

        # Update position
        p['x'] += p['vx']
        p['y'] += p['vy']

        # Draw character
        fill(p['col'])
        text(p['char'], p['x'], p['y'])

    # Instructions
    fill(100)
    textSize(14)
    textAlign(LEFT)
    text("Move mouse near letters to interact", 20, height - 30)


def drawASCIIArt():
    """ASCII art style rendering."""
    background(20)

    chars = " .:-=+*#%@"
    cell_size = 12

    textSize(cell_size)
    textAlign(CENTER, CENTER)
    fill(0, 255, 0)  # Terminal green

    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            # Create a pattern using noise
            n = noise(x * 0.02, y * 0.02, t)
            char_index = int(n * len(chars))
            char_index = constrain(char_index, 0, len(chars) - 1)

            text(chars[char_index], x + cell_size/2, y + cell_size/2)

    # Overlay title
    fill(0, 200)
    noStroke()
    rect(width/2 - 150, height/2 - 40, 300, 80, 10)

    fill(0, 255, 0)
    textSize(32)
    text("ASCII ART", width/2, height/2)


def keyPressed():
    global mode

    if key == '1':
        mode = 0
    elif key == '2':
        mode = 1
    elif key == '3':
        mode = 2
    elif key == '4':
        mode = 3
        initTextParticles()
    elif key == '5':
        mode = 4
    elif key == 's':
        filename = "typography_" + str(frameCount) + ".png"
        save(filename)
        print("Saved:", filename)


# -------------------------------------------------
# Typography Concepts:
#
# Text Functions:
# - text(str, x, y) - Draw text
# - textSize(size) - Set font size
# - textAlign(h, v) - Alignment
# - textWidth(str) - Get width
# - textLeading(size) - Line spacing
#
# Creative Approaches:
# 1. Circular text: Position along arc
# 2. Wave text: Animate y with sine
# 3. Particle text: Each char is a particle
# 4. ASCII art: Map values to characters
#
# Connection to Renoir:
# Typography can incorporate artist palettes
# to create text art in specific color schemes.
# -------------------------------------------------
