"""
Lesson 17: Capstone Project
===========================

A comprehensive generative artwork combining all
techniques learned throughout the course, using
palettes inspired by renoir analysis.

This capstone demonstrates:
- Flow fields (Lesson 07)
- Particle systems (Lesson 06)
- Artist-style palettes (Lesson 11)
- Color harmonies (Lesson 02)
- Interactive controls (Lesson 04)
- Animation (Lesson 03)
- Export capabilities (Lesson 16)

Run this sketch in Processing with Python Mode enabled.
"""

import json

# Artist profiles (from renoir analysis)
artists = {}
current_artist = "monet"

# Flow field
cols = 0
rows = 0
scale = 15
field = []

# Particles
particles = []
max_particles = 800

# Animation
t = 0
z_offset = 0

# Display options
show_field = False
show_trails = True
show_info = True


class ArtParticle:
    """A particle that follows the flow field with artist-specific properties."""

    def __init__(self, artist_profile):
        self.reset(artist_profile)

    def reset(self, artist_profile):
        self.x = random(width)
        self.y = random(height)
        self.prev_x = self.x
        self.prev_y = self.y

        # Artist-specific properties
        palette = artist_profile["palette"]
        self.col = palette[int(random(len(palette)))]
        self.max_speed = random(artist_profile["speed_range"][0],
                                artist_profile["speed_range"][1])
        self.stroke_weight = random(artist_profile["stroke_weight"][0],
                                    artist_profile["stroke_weight"][1])
        self.lifespan = random(100, 300)
        self.age = 0

    def follow(self, field):
        col_idx = int(self.x / scale)
        row_idx = int(self.y / scale)

        col_idx = constrain(col_idx, 0, cols - 1)
        row_idx = constrain(row_idx, 0, rows - 1)

        angle = field[col_idx][row_idx]

        self.vx = cos(angle) * self.max_speed
        self.vy = sin(angle) * self.max_speed

    def update(self):
        self.prev_x = self.x
        self.prev_y = self.y

        self.x += self.vx
        self.y += self.vy
        self.age += 1

        # Edge wrapping
        if self.x < 0:
            self.x = width
            self.prev_x = self.x
        if self.x > width:
            self.x = 0
            self.prev_x = self.x
        if self.y < 0:
            self.y = height
            self.prev_y = self.y
        if self.y > height:
            self.y = 0
            self.prev_y = self.y

    def display(self, artist_profile):
        # Fade based on age
        life_ratio = 1 - (self.age / self.lifespan)
        alpha = life_ratio * artist_profile["opacity"]

        if show_trails:
            stroke(red(self.col), green(self.col), blue(self.col), alpha)
            strokeWeight(self.stroke_weight)
            line(self.prev_x, self.prev_y, self.x, self.y)
        else:
            noStroke()
            fill(red(self.col), green(self.col), blue(self.col), alpha)
            ellipse(self.x, self.y, self.stroke_weight * 2, self.stroke_weight * 2)

    def isDead(self):
        return self.age >= self.lifespan


def setup():
    global cols, rows, field, particles

    size(1200, 800)

    # Initialize artist profiles
    initArtists()

    # Calculate flow field dimensions
    cols = int(width / scale) + 1
    rows = int(height / scale) + 1
    field = [[0 for _ in range(rows)] for _ in range(cols)]

    # Initialize particles
    particles = [ArtParticle(artists[current_artist]) for _ in range(max_particles)]

    print("=" * 50)
    print("ENCRE CAPSTONE: Generative Art Journey")
    print("=" * 50)
    print("\nArtists: 1-Monet, 2-Van Gogh, 3-Seurat, 4-Kandinsky")
    print("\nControls:")
    print("  f: Toggle flow field")
    print("  t: Toggle trails")
    print("  i: Toggle info panel")
    print("  r: Reset particles")
    print("  s: Save high-res image")
    print("  SPACE: Clear canvas")


def initArtists():
    """Initialize artist-inspired generation profiles."""

    # Claude Monet - Impressionist water reflections
    artists["monet"] = {
        "name": "Claude Monet",
        "movement": "Impressionism",
        "palette": [
            color(142, 178, 197),  # Water blue
            color(176, 166, 198),  # Lavender
            color(168, 199, 168),  # Soft green
            color(216, 191, 161),  # Warm beige
            color(112, 145, 128),  # Deep green
        ],
        "background": color(210, 220, 230),
        "speed_range": (1.5, 3),
        "stroke_weight": (1, 3),
        "opacity": 80,
        "flow_scale": 0.003,
        "flow_multiplier": 1
    }

    # Vincent van Gogh - Expressive swirls
    artists["vangogh"] = {
        "name": "Vincent van Gogh",
        "movement": "Post-Impressionism",
        "palette": [
            color(25, 55, 95),     # Night blue
            color(60, 90, 140),    # Sky blue
            color(230, 200, 80),   # Star yellow
            color(40, 70, 50),     # Cypress green
            color(180, 150, 100),  # Earth
        ],
        "background": color(25, 35, 55),
        "speed_range": (2, 4),
        "stroke_weight": (2, 5),
        "opacity": 150,
        "flow_scale": 0.005,
        "flow_multiplier": 3
    }

    # Georges Seurat - Pointillist dots
    artists["seurat"] = {
        "name": "Georges Seurat",
        "movement": "Neo-Impressionism",
        "palette": [
            color(180, 200, 220),  # Sky
            color(140, 170, 120),  # Grass
            color(200, 180, 140),  # Sand
            color(220, 190, 170),  # Skin
            color(80, 100, 140),   # Shadow
        ],
        "background": color(240, 235, 220),
        "speed_range": (0.5, 1.5),
        "stroke_weight": (2, 4),
        "opacity": 200,
        "flow_scale": 0.002,
        "flow_multiplier": 1
    }

    # Wassily Kandinsky - Abstract geometric
    artists["kandinsky"] = {
        "name": "Wassily Kandinsky",
        "movement": "Abstract Expressionism",
        "palette": [
            color(200, 50, 50),    # Red
            color(50, 100, 180),   # Blue
            color(240, 200, 50),   # Yellow
            color(30, 30, 30),     # Black
            color(220, 220, 220),  # White
        ],
        "background": color(245, 240, 230),
        "speed_range": (2, 5),
        "stroke_weight": (1, 6),
        "opacity": 180,
        "flow_scale": 0.008,
        "flow_multiplier": 2
    }


def draw():
    global z_offset, t

    artist = artists[current_artist]

    if show_trails:
        # Fade effect
        noStroke()
        fill(red(artist["background"]),
             green(artist["background"]),
             blue(artist["background"]), 10)
        rect(0, 0, width, height)
    else:
        background(artist["background"])

    # Update flow field
    updateField(artist)

    # Show field if enabled
    if show_field:
        drawField()

    # Update and draw particles
    for i in range(len(particles) - 1, -1, -1):
        p = particles[i]
        p.follow(field)
        p.update()
        p.display(artist)

        if p.isDead():
            particles[i] = ArtParticle(artist)

    z_offset += 0.002
    t += 0.01

    # Info panel
    if show_info:
        drawInfoPanel()


def updateField(artist):
    """Update flow field based on artist style."""
    flow_scale = artist["flow_scale"]
    multiplier = artist["flow_multiplier"]

    for i in range(cols):
        for j in range(rows):
            angle = noise(i * flow_scale * 10, j * flow_scale * 10, z_offset)
            angle = angle * TWO_PI * multiplier
            field[i][j] = angle


def drawField():
    """Visualize the flow field."""
    for i in range(0, cols, 2):
        for j in range(0, rows, 2):
            x = i * scale
            y = j * scale
            angle = field[i][j]

            stroke(0, 30)
            strokeWeight(1)
            pushMatrix()
            translate(x + scale/2, y + scale/2)
            rotate(angle)
            line(0, 0, scale * 0.6, 0)
            popMatrix()


def drawInfoPanel():
    """Draw artist info panel."""
    artist = artists[current_artist]

    # Panel background
    fill(255, 220)
    noStroke()
    rect(15, 15, 280, 130, 8)

    # Title
    fill(0)
    textSize(18)
    text(artist["name"], 25, 42)

    # Movement
    fill(100)
    textSize(12)
    text(artist["movement"], 25, 60)

    # Stats
    textSize(11)
    text("Particles: " + str(len(particles)), 25, 85)
    text("Trails: " + ("ON" if show_trails else "OFF"), 130, 85)
    text("Flow: " + ("VISIBLE" if show_field else "HIDDEN"), 200, 85)

    # Palette swatches
    text("Palette:", 25, 110)
    for i, c in enumerate(artist["palette"]):
        fill(c)
        noStroke()
        rect(75 + i * 25, 98, 20, 15, 3)

    # Instructions
    fill(120)
    textSize(10)
    text("Keys: 1-4 artists | f field | t trails | s save", 25, 135)


def keyPressed():
    global current_artist, show_field, show_trails, show_info, particles

    if key == '1':
        switchArtist("monet")
    elif key == '2':
        switchArtist("vangogh")
    elif key == '3':
        switchArtist("seurat")
    elif key == '4':
        switchArtist("kandinsky")
    elif key == 'f':
        show_field = not show_field
    elif key == 't':
        show_trails = not show_trails
        background(artists[current_artist]["background"])
    elif key == 'i':
        show_info = not show_info
    elif key == 'r':
        particles = [ArtParticle(artists[current_artist]) for _ in range(max_particles)]
    elif key == ' ':
        background(artists[current_artist]["background"])
    elif key == 's':
        saveHighRes()


def switchArtist(artist_id):
    global current_artist, particles
    current_artist = artist_id
    artist = artists[current_artist]
    background(artist["background"])
    particles = [ArtParticle(artist) for _ in range(max_particles)]
    print("Artist:", artist["name"])


def saveHighRes():
    """Save high-resolution version."""
    artist = artists[current_artist]
    filename = artist["name"].replace(" ", "_") + "_" + str(millis()) + ".png"
    save("export/" + filename)
    print("Saved:", filename)


# -------------------------------------------------
# Capstone Summary:
#
# This project combines:
# - Flow fields for organic movement
# - Particle systems with lifecycle
# - Artist-inspired color palettes
# - Style-specific parameters
# - Interactive controls
# - Export functionality
#
# Each artist profile includes:
# - Authentic color palette (from renoir)
# - Brushwork characteristics
# - Flow field behavior
# - Opacity and layering
#
# Extensions to try:
# - Load palettes from JSON files
# - Add audio reactivity
# - Implement more artists
# - Create hybrid styles
# - Add image export sequence
# -------------------------------------------------
