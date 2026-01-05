"""
Lesson 06: Particle Systems (py5 version)
=========================================

Learn to create and manage particle systems for
dynamic, organic visual effects.

Learning Objectives:
- Create particle classes with physics
- Manage particle lifecycles
- Apply forces (gravity, wind)
- Use particles for artistic effects

Run with: python particle_systems_py5.py
"""

import py5

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
            self.vx = py5.random(-2, 2)
            self.vy = py5.random(-8, -4)
            self.gravity = 0.15
            self.col = palette[int(py5.random(len(palette)))]
            self.size = py5.random(8, 15)

        elif mode == 1:  # Explosion
            angle = py5.random(py5.TWO_PI)
            speed = py5.random(2, 8)
            self.vx = py5.cos(angle) * speed
            self.vy = py5.sin(angle) * speed
            self.gravity = 0.05
            self.col = palette[int(py5.random(len(palette)))]
            self.size = py5.random(5, 12)

        elif mode == 2:  # Rain
            self.vx = py5.random(-0.5, 0.5)
            self.vy = py5.random(5, 12)
            self.gravity = 0.1
            self.col = py5.color(100, 150, 200, 150)
            self.size = py5.random(2, 4)

        elif mode == 3:  # Fireflies
            self.vx = py5.random(-1, 1)
            self.vy = py5.random(-1, 1)
            self.gravity = 0
            self.col = py5.color(255, 220, 100)
            self.size = py5.random(4, 8)
            self.phase = py5.random(py5.TWO_PI)

        self.lifespan = 255
        self.decay = py5.random(2, 5)

    def update(self):
        """Update particle physics."""
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.lifespan -= self.decay

        # Mode-specific behavior
        if self.mode == 3:  # Fireflies wander
            self.vx += py5.random(-0.2, 0.2)
            self.vy += py5.random(-0.2, 0.2)
            self.vx = py5.constrain(self.vx, -2, 2)
            self.vy = py5.constrain(self.vy, -2, 2)
            # Pulsing glow
            self.phase += 0.1

    def display(self):
        """Draw the particle."""
        py5.no_stroke()

        if self.mode == 3:  # Fireflies glow
            glow = (py5.sin(self.phase) + 1) / 2
            alpha = self.lifespan * glow
            py5.fill(py5.red(self.col), py5.green(self.col), py5.blue(self.col), alpha)
            py5.ellipse(self.x, self.y, self.size * (1 + glow), self.size * (1 + glow))
        else:
            py5.fill(py5.red(self.col), py5.green(self.col), py5.blue(self.col), self.lifespan)
            py5.ellipse(self.x, self.y, self.size, self.size)

    def is_dead(self):
        """Check if particle should be removed."""
        if self.lifespan <= 0:
            return True
        if self.y > py5.height + 20:
            return True
        if self.mode == 2 and self.y > py5.height - 5:
            return True
        return False


def setup():
    py5.size(800, 600)
    global palette

    # Art-inspired palette
    palette = [
        py5.color(66, 133, 244),   # Blue
        py5.color(219, 68, 55),    # Red
        py5.color(244, 180, 0),    # Yellow
        py5.color(15, 157, 88),    # Green
        py5.color(156, 39, 176),   # Purple
    ]

    print("Lesson 06: Particle Systems")
    print("\nControls:")
    print("  Click to emit particles")
    print("  Press 1-4 to switch modes")
    print("  Press 'c' to clear")
    print("  Press 's' to save image")


def draw():
    global particles

    # Different backgrounds per mode
    if mode == 2:  # Rain
        py5.background(40, 50, 60)
    elif mode == 3:  # Fireflies
        py5.background(20, 25, 40)
    else:
        py5.background(30)

    # Continuous emission for some modes
    if mode == 0:  # Fountain
        for _ in range(3):
            particles.append(Particle(emitter_x, py5.height - 50, mode))
    elif mode == 2:  # Rain
        for _ in range(5):
            particles.append(Particle(py5.random(py5.width), -10, mode))
    elif mode == 3:  # Fireflies
        if len(particles) < 50 and py5.random(1) < 0.1:
            particles.append(Particle(py5.random(py5.width), py5.random(py5.height), mode))

    # Update and display particles
    for i in range(len(particles) - 1, -1, -1):
        p = particles[i]
        p.update()
        p.display()
        if p.is_dead():
            particles.pop(i)

    # UI
    draw_ui()


def draw_ui():
    """Draw mode indicator and particle count."""
    py5.fill(255)
    py5.no_stroke()
    py5.text_size(14)
    py5.text(f"Mode: {modes[mode]}", 20, 25)
    py5.text(f"Particles: {len(particles)}", 20, 45)

    if mode == 1:
        py5.text("Click anywhere for explosion", 20, py5.height - 20)
    else:
        py5.text("Click to set emitter position", 20, py5.height - 20)


def mouse_pressed():
    global emitter_x, emitter_y

    if mode == 1:  # Explosion
        for _ in range(100):
            particles.append(Particle(py5.mouse_x, py5.mouse_y, mode))
    else:
        emitter_x = py5.mouse_x
        emitter_y = py5.mouse_y


def key_pressed():
    global mode, particles

    if py5.key == '1':
        mode = 0
        particles = []
        print("Mode: Fountain")
    elif py5.key == '2':
        mode = 1
        particles = []
        print("Mode: Explosion (click to trigger)")
    elif py5.key == '3':
        mode = 2
        particles = []
        print("Mode: Rain")
    elif py5.key == '4':
        mode = 3
        particles = []
        print("Mode: Fireflies")
    elif py5.key == 'c':
        particles = []
        print("Particles cleared")
    elif py5.key == 's':
        filename = f"particles_{py5.frame_count}.png"
        py5.save(filename)
        print(f"Saved: {filename}")


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

py5.run_sketch()
