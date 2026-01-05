"""
Lesson 07: Flow Fields (py5 version)
====================================

Create mesmerizing flow field visualizations using
Perlin noise to guide particle movement.

Learning Objectives:
- Generate vector fields from noise
- Guide particles along flow lines
- Visualize fields and particle trails
- Create organic, generative compositions

Run with: python flow_fields_py5.py
"""

import py5

# Flow field settings
cols = 0
rows = 0
scale = 20
field = []
particles = []
num_particles = 500

# Animation
z_offset = 0

# Visualization mode
show_field = False
show_trails = True

# Palette
palette = []


class FlowParticle:
    """A particle that follows the flow field."""

    def __init__(self):
        self.reset()
        self.col = palette[int(py5.random(len(palette)))]

    def reset(self):
        self.x = py5.random(py5.width)
        self.y = py5.random(py5.height)
        self.prev_x = self.x
        self.prev_y = self.y
        self.vx = 0
        self.vy = 0
        self.max_speed = py5.random(2, 4)

    def follow(self, field):
        """Follow the flow field vectors."""
        # Find which cell we're in
        col = int(self.x / scale)
        row = int(self.y / scale)

        # Clamp to field bounds
        col = py5.constrain(col, 0, cols - 1)
        row = py5.constrain(row, 0, rows - 1)

        # Get the angle from the field
        angle = field[col][row]

        # Calculate velocity from angle
        self.vx = py5.cos(angle) * self.max_speed
        self.vy = py5.sin(angle) * self.max_speed

    def update(self):
        # Store previous position for trails
        self.prev_x = self.x
        self.prev_y = self.y

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Wrap around edges
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

    def display(self):
        if show_trails:
            # Draw line from previous to current position
            py5.stroke(py5.red(self.col), py5.green(self.col), py5.blue(self.col), 50)
            py5.stroke_weight(1)
            py5.line(self.prev_x, self.prev_y, self.x, self.y)
        else:
            # Draw as point
            py5.stroke(self.col)
            py5.stroke_weight(2)
            py5.point(self.x, self.y)


def setup():
    global cols, rows, field, particles, palette

    py5.size(800, 600)

    # Art-inspired palette (Monet-like)
    palette = [
        py5.color(142, 178, 197),  # Sky blue
        py5.color(89, 112, 95),    # Sage green
        py5.color(216, 191, 161),  # Warm beige
        py5.color(78, 91, 110),    # Blue-gray
        py5.color(168, 147, 120),  # Earth tone
    ]

    # Calculate field dimensions
    cols = int(py5.width / scale) + 1
    rows = int(py5.height / scale) + 1

    # Initialize field
    field = [[0 for _ in range(rows)] for _ in range(cols)]

    # Create particles
    particles = [FlowParticle() for _ in range(num_particles)]

    # Start with faded background
    py5.background(20)

    print("Lesson 07: Flow Fields")
    print("\nControls:")
    print("  Press 'f' to show/hide field")
    print("  Press 't' to toggle trails")
    print("  Press 'r' to reset")
    print("  Press 's' to save image")


def draw():
    global z_offset

    if not show_trails:
        py5.background(20)
    else:
        # Subtle fade for trail effect
        py5.no_stroke()
        py5.fill(20, 5)
        py5.rect(0, 0, py5.width, py5.height)

    # Update flow field
    update_field()

    # Show field vectors if enabled
    if show_field:
        draw_field()

    # Update and display particles
    for p in particles:
        p.follow(field)
        p.update()
        p.display()

    # Animate the noise
    z_offset += 0.003

    # UI
    draw_ui()


def update_field():
    """Update the flow field based on Perlin noise."""
    noise_scale = 0.1

    for i in range(cols):
        for j in range(rows):
            # Use 3D noise for animation
            angle = py5.noise(i * noise_scale, j * noise_scale, z_offset) * py5.TWO_PI * 2
            field[i][j] = angle


def draw_field():
    """Visualize the flow field vectors."""
    for i in range(cols):
        for j in range(rows):
            x = i * scale
            y = j * scale
            angle = field[i][j]

            # Draw vector
            py5.stroke(255, 100)
            py5.stroke_weight(1)
            py5.push_matrix()
            py5.translate(x + scale/2, y + scale/2)
            py5.rotate(angle)
            py5.line(0, 0, scale * 0.4, 0)
            # Arrow head
            py5.line(scale * 0.4, 0, scale * 0.3, -3)
            py5.line(scale * 0.4, 0, scale * 0.3, 3)
            py5.pop_matrix()


def draw_ui():
    """Draw mode indicators."""
    py5.fill(255)
    py5.no_stroke()
    py5.text_size(12)
    py5.text(f"Flow Field | Particles: {num_particles}", 20, 25)

    modes = []
    if show_field:
        modes.append("Field ON")
    if show_trails:
        modes.append("Trails ON")
    py5.text(" | ".join(modes) if modes else "Points only", 20, 45)


def key_pressed():
    global show_field, show_trails, particles

    if py5.key == 'f':
        show_field = not show_field
        print(f"Field vectors: {'ON' if show_field else 'OFF'}")

    elif py5.key == 't':
        show_trails = not show_trails
        py5.background(20)
        print(f"Trails: {'ON' if show_trails else 'OFF'}")

    elif py5.key == 'r':
        particles = [FlowParticle() for _ in range(num_particles)]
        py5.background(20)
        print("Reset particles")

    elif py5.key == 's':
        filename = f"flowfield_{py5.frame_count}.png"
        py5.save(filename)
        print(f"Saved: {filename}")


# -------------------------------------------------
# Flow Field Concepts:
#
# 1. The field is a grid of angles (vectors)
# 2. Perlin noise generates smooth, continuous angles
# 3. Particles look up their cell's angle
# 4. Particles move in that direction
#
# Variations to try:
# - Change noise scale (0.01 = smooth, 0.5 = chaotic)
# - Multiply angle by 2 or 4 for more swirls
# - Add curl noise for more interesting patterns
# - Use multiple noise layers
#
# Connection to Renoir:
# Flow fields can simulate:
# - Brushstroke directions in paintings
# - Wind patterns in landscapes
# - Water movement in Impressionist seascapes
# - Atmospheric effects and light flow
# -------------------------------------------------

py5.run_sketch()
