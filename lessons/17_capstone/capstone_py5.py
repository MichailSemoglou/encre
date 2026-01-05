"""
Lesson 17: Capstone Project (py5 version)
=========================================

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

Run with: python capstone_py5.py
"""

import py5
from pathlib import Path

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
        self.x = py5.random(py5.width)
        self.y = py5.random(py5.height)
        self.prev_x = self.x
        self.prev_y = self.y
        self.vx = 0
        self.vy = 0

        palette = artist_profile["palette"]
        self.col = palette[int(py5.random(len(palette)))]
        self.max_speed = py5.random(artist_profile["speed_range"][0],
                                    artist_profile["speed_range"][1])
        self.stroke_weight = py5.random(artist_profile["stroke_weight"][0],
                                        artist_profile["stroke_weight"][1])
        self.lifespan = py5.random(100, 300)
        self.age = 0

    def follow(self, field):
        col_idx = int(self.x / scale)
        row_idx = int(self.y / scale)

        col_idx = py5.constrain(col_idx, 0, cols - 1)
        row_idx = py5.constrain(row_idx, 0, rows - 1)

        angle = field[col_idx][row_idx]

        self.vx = py5.cos(angle) * self.max_speed
        self.vy = py5.sin(angle) * self.max_speed

    def update(self):
        self.prev_x = self.x
        self.prev_y = self.y

        self.x += self.vx
        self.y += self.vy
        self.age += 1

        if self.x < 0:
            self.x = py5.width
            self.prev_x = self.x
        if self.x > py5.width:
            self.x = 0
            self.prev_x = self.x
        if self.y < 0:
            self.y = py5.height
            self.prev_y = self.y
        if self.y > py5.height:
            self.y = 0
            self.prev_y = self.y

    def display(self, artist_profile):
        life_ratio = 1 - (self.age / self.lifespan)
        alpha = life_ratio * artist_profile["opacity"]

        if show_trails:
            py5.stroke(py5.red(self.col), py5.green(self.col), py5.blue(self.col), alpha)
            py5.stroke_weight(self.stroke_weight)
            py5.line(self.prev_x, self.prev_y, self.x, self.y)
        else:
            py5.no_stroke()
            py5.fill(py5.red(self.col), py5.green(self.col), py5.blue(self.col), alpha)
            py5.ellipse(self.x, self.y, self.stroke_weight * 2, self.stroke_weight * 2)

    def is_dead(self):
        return self.age >= self.lifespan


def setup():
    global cols, rows, field, particles

    py5.size(1200, 800)

    init_artists()

    cols = int(py5.width / scale) + 1
    rows = int(py5.height / scale) + 1
    field = [[0 for _ in range(rows)] for _ in range(cols)]

    particles = [ArtParticle(artists[current_artist]) for _ in range(max_particles)]

    Path("export").mkdir(exist_ok=True)

    print("=" * 50)
    print("ENCRE CAPSTONE: Generative Art Journey")
    print("=" * 50)
    print("\nArtists: 1-Monet, 2-Van Gogh, 3-Seurat, 4-Kandinsky")
    print("\nControls:")
    print("  f: Toggle flow field")
    print("  t: Toggle trails")
    print("  i: Toggle info panel")
    print("  r: Reset particles")
    print("  s: Save image")
    print("  SPACE: Clear canvas")


def init_artists():
    """Initialize artist-inspired generation profiles."""

    artists["monet"] = {
        "name": "Claude Monet",
        "movement": "Impressionism",
        "palette": [
            py5.color(142, 178, 197),
            py5.color(176, 166, 198),
            py5.color(168, 199, 168),
            py5.color(216, 191, 161),
            py5.color(112, 145, 128),
        ],
        "background": py5.color(210, 220, 230),
        "speed_range": (1.5, 3),
        "stroke_weight": (1, 3),
        "opacity": 80,
        "flow_scale": 0.003,
        "flow_multiplier": 1
    }

    artists["vangogh"] = {
        "name": "Vincent van Gogh",
        "movement": "Post-Impressionism",
        "palette": [
            py5.color(25, 55, 95),
            py5.color(60, 90, 140),
            py5.color(230, 200, 80),
            py5.color(40, 70, 50),
            py5.color(180, 150, 100),
        ],
        "background": py5.color(25, 35, 55),
        "speed_range": (2, 4),
        "stroke_weight": (2, 5),
        "opacity": 150,
        "flow_scale": 0.005,
        "flow_multiplier": 3
    }

    artists["seurat"] = {
        "name": "Georges Seurat",
        "movement": "Neo-Impressionism",
        "palette": [
            py5.color(180, 200, 220),
            py5.color(140, 170, 120),
            py5.color(200, 180, 140),
            py5.color(220, 190, 170),
            py5.color(80, 100, 140),
        ],
        "background": py5.color(240, 235, 220),
        "speed_range": (0.5, 1.5),
        "stroke_weight": (2, 4),
        "opacity": 200,
        "flow_scale": 0.002,
        "flow_multiplier": 1
    }

    artists["kandinsky"] = {
        "name": "Wassily Kandinsky",
        "movement": "Abstract Expressionism",
        "palette": [
            py5.color(200, 50, 50),
            py5.color(50, 100, 180),
            py5.color(240, 200, 50),
            py5.color(30, 30, 30),
            py5.color(220, 220, 220),
        ],
        "background": py5.color(245, 240, 230),
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
        py5.no_stroke()
        py5.fill(py5.red(artist["background"]),
                 py5.green(artist["background"]),
                 py5.blue(artist["background"]), 10)
        py5.rect(0, 0, py5.width, py5.height)
    else:
        py5.background(artist["background"])

    update_field(artist)

    if show_field:
        draw_field()

    for i in range(len(particles) - 1, -1, -1):
        p = particles[i]
        p.follow(field)
        p.update()
        p.display(artist)

        if p.is_dead():
            particles[i] = ArtParticle(artist)

    z_offset += 0.002
    t += 0.01

    if show_info:
        draw_info_panel()


def update_field(artist):
    """Update flow field based on artist style."""
    flow_scale = artist["flow_scale"]
    multiplier = artist["flow_multiplier"]

    for i in range(cols):
        for j in range(rows):
            angle = py5.noise(i * flow_scale * 10, j * flow_scale * 10, z_offset)
            angle = angle * py5.TWO_PI * multiplier
            field[i][j] = angle


def draw_field():
    """Visualize the flow field."""
    for i in range(0, cols, 2):
        for j in range(0, rows, 2):
            x = i * scale
            y = j * scale
            angle = field[i][j]

            py5.stroke(0, 30)
            py5.stroke_weight(1)
            py5.push_matrix()
            py5.translate(x + scale/2, y + scale/2)
            py5.rotate(angle)
            py5.line(0, 0, scale * 0.6, 0)
            py5.pop_matrix()


def draw_info_panel():
    """Draw artist info panel."""
    artist = artists[current_artist]

    py5.fill(255, 220)
    py5.no_stroke()
    py5.rect(15, 15, 280, 130, 8)

    py5.fill(0)
    py5.text_size(18)
    py5.text(artist["name"], 25, 42)

    py5.fill(100)
    py5.text_size(12)
    py5.text(artist["movement"], 25, 60)

    py5.text_size(11)
    py5.text(f"Particles: {len(particles)}", 25, 85)
    py5.text(f"Trails: {'ON' if show_trails else 'OFF'}", 130, 85)
    py5.text(f"Flow: {'VISIBLE' if show_field else 'HIDDEN'}", 200, 85)

    py5.text("Palette:", 25, 110)
    for i, c in enumerate(artist["palette"]):
        py5.fill(c)
        py5.no_stroke()
        py5.rect(75 + i * 25, 98, 20, 15, 3)

    py5.fill(120)
    py5.text_size(10)
    py5.text("Keys: 1-4 artists | f field | t trails | s save", 25, 135)


def key_pressed():
    global current_artist, show_field, show_trails, show_info, particles

    if py5.key == '1':
        switch_artist("monet")
    elif py5.key == '2':
        switch_artist("vangogh")
    elif py5.key == '3':
        switch_artist("seurat")
    elif py5.key == '4':
        switch_artist("kandinsky")
    elif py5.key == 'f':
        show_field = not show_field
    elif py5.key == 't':
        show_trails = not show_trails
        py5.background(artists[current_artist]["background"])
    elif py5.key == 'i':
        show_info = not show_info
    elif py5.key == 'r':
        particles = [ArtParticle(artists[current_artist]) for _ in range(max_particles)]
    elif py5.key == ' ':
        py5.background(artists[current_artist]["background"])
    elif py5.key == 's':
        save_image()


def switch_artist(artist_id):
    global current_artist, particles
    current_artist = artist_id
    artist = artists[current_artist]
    py5.background(artist["background"])
    particles = [ArtParticle(artist) for _ in range(max_particles)]
    print(f"Artist: {artist['name']}")


def save_image():
    """Save current artwork."""
    artist = artists[current_artist]
    filename = f"export/{artist['name'].replace(' ', '_')}_{py5.millis()}.png"
    py5.save(filename)
    print(f"Saved: {filename}")


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
# -------------------------------------------------

py5.run_sketch()
