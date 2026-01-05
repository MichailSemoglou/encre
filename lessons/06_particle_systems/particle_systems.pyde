"""
Lesson 06: Particle Systems
===========================

Learn to create and manage particle systems for
dynamic, organic visual effects.

Learning Objectives:
- Create particle classes with physics
- Manage particle lifecycles
- Apply forces (gravity, wind)
- Use particles for artistic effects

Run this sketch in Processing with Python Mode enabled.
"""

# Particle system
particles = []
emitter_x = 400
emitter_y = 300
mode = 0
modes = ["Fountain", "Explosion", "Rain", "Fireflies"]

# Palette (art-inspired colors)
palette = []


class Particle:
    """A single particle with position, velocity, and lifecycle."""

    def __init__(self, x, y, mode):
        self.x = x
        self.y = y
        self.mode = mode

        if mode == 0:  # Fountain
            self.vx = random(-2, 2)
            self.vy = random(-8, -4)
            self.gravity = 0.15
            self.col = palette[int(random(len(palette)))]
            self.size = random(8, 15)

        elif mode == 1:  # Explosion
            angle = random(TWO_PI)
            speed = random(2, 8)
            self.vx = cos(angle) * speed
            self.vy = sin(angle) * speed
            self.gravity = 0.05
            self.col = palette[int(random(len(palette)))]
            self.size = random(5, 12)

        elif mode == 2:  # Rain
            self.vx = random(-0.5, 0.5)
            self.vy = random(5, 12)
            self.gravity = 0.1
            self.col = color(100, 150, 200, 150)
            self.size = random(2, 4)

        elif mode == 3:  # Fireflies
            self.vx = random(-1, 1)
            self.vy = random(-1, 1)
            self.gravity = 0
            self.col = color(255, 220, 100)
            self.size = random(4, 8)
            self.phase = random(TWO_PI)

        self.lifespan = 255
        self.decay = random(2, 5)

    def update(self):
        """Update particle physics."""
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.lifespan -= self.decay

        # Mode-specific behavior
        if self.mode == 3:  # Fireflies wander
            self.vx += random(-0.2, 0.2)
            self.vy += random(-0.2, 0.2)
            self.vx = constrain(self.vx, -2, 2)
            self.vy = constrain(self.vy, -2, 2)
            # Pulsing glow
            self.phase += 0.1

    def display(self):
        """Draw the particle."""
        noStroke()

        if self.mode == 3:  # Fireflies glow
            glow = (sin(self.phase) + 1) / 2
            alpha = self.lifespan * glow
            fill(red(self.col), green(self.col), blue(self.col), alpha)
            ellipse(self.x, self.y, self.size * (1 + glow), self.size * (1 + glow))
        else:
            fill(red(self.col), green(self.col), blue(self.col), self.lifespan)
            ellipse(self.x, self.y, self.size, self.size)

    def isDead(self):
        """Check if particle should be removed."""
        if self.lifespan <= 0:
            return True
        if self.y > height + 20:
            return True
        if self.mode == 2 and self.y > height - 5:
            return True
        return False


def setup():
    size(800, 600)
    global palette

    # Art-inspired palette
    palette = [
        color(66, 133, 244),   # Blue
        color(219, 68, 55),    # Red
        color(244, 180, 0),    # Yellow
        color(15, 157, 88),    # Green
        color(156, 39, 176),   # Purple
    ]

    print("Lesson 06: Particle Systems")
    print("\nControls:")
    print("  Click to emit particles")
    print("  Press 1-4 to switch modes")
    print("  Press 'c' to clear")
    print("  Press 's' to save image")


def draw():
    # Different backgrounds per mode
    if mode == 2:  # Rain
        background(40, 50, 60)
    elif mode == 3:  # Fireflies
        background(20, 25, 40)
    else:
        background(30)

    # Continuous emission for some modes
    if mode == 0:  # Fountain
        for _ in range(3):
            particles.append(Particle(emitter_x, height - 50, mode))
    elif mode == 2:  # Rain
        for _ in range(5):
            particles.append(Particle(random(width), -10, mode))
    elif mode == 3:  # Fireflies
        if len(particles) < 50 and random(1) < 0.1:
            particles.append(Particle(random(width), random(height), mode))

    # Update and display particles
    for i in range(len(particles) - 1, -1, -1):
        p = particles[i]
        p.update()
        p.display()
        if p.isDead():
            particles.pop(i)

    # UI
    drawUI()


def drawUI():
    """Draw mode indicator and particle count."""
    fill(255)
    noStroke()
    textSize(14)
    text("Mode: " + modes[mode], 20, 25)
    text("Particles: " + str(len(particles)), 20, 45)

    if mode == 1:
        text("Click anywhere for explosion", 20, height - 20)
    else:
        text("Click to set emitter position", 20, height - 20)


def mousePressed():
    global emitter_x, emitter_y

    if mode == 1:  # Explosion
        for _ in range(100):
            particles.append(Particle(mouseX, mouseY, mode))
    else:
        emitter_x = mouseX
        emitter_y = mouseY


def keyPressed():
    global mode, particles

    if key == '1':
        mode = 0
        particles = []
        print("Mode: Fountain")
    elif key == '2':
        mode = 1
        particles = []
        print("Mode: Explosion (click to trigger)")
    elif key == '3':
        mode = 2
        particles = []
        print("Mode: Rain")
    elif key == '4':
        mode = 3
        particles = []
        print("Mode: Fireflies")
    elif key == 'c':
        particles = []
        print("Particles cleared")
    elif key == 's':
        filename = "particles_" + str(frameCount) + ".png"
        save(filename)
        print("Saved:", filename)


# -------------------------------------------------
# Particle System Concepts:
#
# 1. Emitter: Where particles are born
# 2. Particle: Has position, velocity, lifespan
# 3. Forces: Gravity, wind, attraction/repulsion
# 4. Lifecycle: Birth, update, death
#
# Physics basics:
# - velocity += acceleration (gravity)
# - position += velocity
# - lifespan decreases each frame
#
# Performance tips:
# - Remove dead particles
# - Limit maximum particles
# - Use object pooling for many particles
#
# Connection to Renoir:
# Particles can be colored using artist palettes
# to create impressionistic effects, like:
# - Pointillist dots
# - Brushstroke simulations
# - Light and atmosphere effects
# -------------------------------------------------
