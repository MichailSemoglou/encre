"""
Lesson 07: Flow Fields
======================

Create mesmerizing flow field visualizations using
Perlin noise to guide particle movement.

Learning Objectives:
- Generate vector fields from noise
- Guide particles along flow lines
- Visualize fields and particle trails
- Create organic, generative compositions

Run this sketch in Processing with Python Mode enabled.
"""

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
        self.col = palette[int(random(len(palette)))]

    def reset(self):
        self.x = random(width)
        self.y = random(height)
        self.prev_x = self.x
        self.prev_y = self.y
        self.max_speed = random(2, 4)

    def follow(self, field):
        """Follow the flow field vectors."""
        # Find which cell we're in
        col = int(self.x / scale)
        row = int(self.y / scale)

        # Clamp to field bounds
        col = constrain(col, 0, cols - 1)
        row = constrain(row, 0, rows - 1)

        # Get the angle from the field
        angle = field[col][row]

        # Calculate velocity from angle
        self.vx = cos(angle) * self.max_speed
        self.vy = sin(angle) * self.max_speed

    def update(self):
        # Store previous position for trails
        self.prev_x = self.x
        self.prev_y = self.y

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Wrap around edges
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

    def display(self):
        if show_trails:
            # Draw line from previous to current position
            stroke(red(self.col), green(self.col), blue(self.col), 50)
            strokeWeight(1)
            line(self.prev_x, self.prev_y, self.x, self.y)
        else:
            # Draw as point
            stroke(self.col)
            strokeWeight(2)
            point(self.x, self.y)


def setup():
    global cols, rows, field, particles, palette

    size(800, 600)

    # Art-inspired palette (Monet-like)
    palette = [
        color(142, 178, 197),  # Sky blue
        color(89, 112, 95),    # Sage green
        color(216, 191, 161),  # Warm beige
        color(78, 91, 110),    # Blue-gray
        color(168, 147, 120),  # Earth tone
    ]

    # Calculate field dimensions
    cols = int(width / scale) + 1
    rows = int(height / scale) + 1

    # Initialize field
    field = [[0 for _ in range(rows)] for _ in range(cols)]

    # Create particles
    particles = [FlowParticle() for _ in range(num_particles)]

    # Start with faded background
    background(20)

    print("Lesson 07: Flow Fields")
    print("\nControls:")
    print("  Press 'f' to show/hide field")
    print("  Press 't' to toggle trails")
    print("  Press 'r' to reset")
    print("  Press 's' to save image")


def draw():
    global z_offset

    if not show_trails:
        background(20)
    else:
        # Subtle fade for trail effect
        noStroke()
        fill(20, 5)
        rect(0, 0, width, height)

    # Update flow field
    updateField()

    # Show field vectors if enabled
    if show_field:
        drawField()

    # Update and display particles
    for p in particles:
        p.follow(field)
        p.update()
        p.display()

    # Animate the noise
    z_offset += 0.003

    # UI
    drawUI()


def updateField():
    """Update the flow field based on Perlin noise."""
    noise_scale = 0.1

    for i in range(cols):
        for j in range(rows):
            # Use 3D noise for animation
            angle = noise(i * noise_scale, j * noise_scale, z_offset) * TWO_PI * 2
            field[i][j] = angle


def drawField():
    """Visualize the flow field vectors."""
    for i in range(cols):
        for j in range(rows):
            x = i * scale
            y = j * scale
            angle = field[i][j]

            # Draw vector
            stroke(255, 100)
            strokeWeight(1)
            pushMatrix()
            translate(x + scale/2, y + scale/2)
            rotate(angle)
            line(0, 0, scale * 0.4, 0)
            # Arrow head
            line(scale * 0.4, 0, scale * 0.3, -3)
            line(scale * 0.4, 0, scale * 0.3, 3)
            popMatrix()


def drawUI():
    """Draw mode indicators."""
    fill(255)
    noStroke()
    textSize(12)
    text("Flow Field | Particles: " + str(num_particles), 20, 25)

    modes = []
    if show_field:
        modes.append("Field ON")
    if show_trails:
        modes.append("Trails ON")
    text(" | ".join(modes) if modes else "Points only", 20, 45)


def keyPressed():
    global show_field, show_trails, particles

    if key == 'f':
        show_field = not show_field
        print("Field vectors:", "ON" if show_field else "OFF")

    elif key == 't':
        show_trails = not show_trails
        background(20)
        print("Trails:", "ON" if show_trails else "OFF")

    elif key == 'r':
        particles = [FlowParticle() for _ in range(num_particles)]
        background(20)
        print("Reset particles")

    elif key == 's':
        filename = "flowfield_" + str(frameCount) + ".png"
        save(filename)
        print("Saved:", filename)


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
