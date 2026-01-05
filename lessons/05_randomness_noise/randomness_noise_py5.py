"""
Lesson 05: Randomness and Noise (py5 version)
=============================================

Explore the difference between random() and noise(),
and learn to create organic, natural-looking patterns.

Learning Objectives:
- Understand random() vs noise()
- Create Perlin noise patterns
- Apply noise to motion and visuals
- Build natural-looking generative systems

Run with: python randomness_noise_py5.py
"""

import py5

# Mode control
mode = 0
modes = ["Random", "Noise 1D", "Noise 2D", "Comparison"]

# Animation
t = 0
particles = []


def setup():
    py5.size(800, 600)
    py5.noise_seed(42)  # Consistent results
    init_particles()

    print("Lesson 05: Randomness and Noise")
    print("\nControls:")
    print("  Press 1-4 to switch modes")
    print("  Press 'r' to reset")
    print("  Press 's' to save image")


def init_particles():
    """Initialize particles for comparison mode."""
    global particles
    particles = []
    for i in range(50):
        particles.append({
            'x': py5.width / 2,
            'y': py5.height / 2,
            'x2': py5.width / 2,
            'y2': py5.height / 2
        })


def draw():
    global t
    t += 0.01

    if mode == 0:
        draw_random_demo()
    elif mode == 1:
        draw_noise_1d()
    elif mode == 2:
        draw_noise_2d()
    elif mode == 3:
        draw_comparison()

    # Mode indicator
    py5.fill(0)
    py5.no_stroke()
    py5.rect(0, 0, py5.width, 35)
    py5.fill(255)
    py5.text_size(14)
    py5.text(f"Mode: {modes[mode]} (Press 1-4 to switch)", 20, 24)


def draw_random_demo():
    """Demonstrate random() - chaotic, unpredictable."""
    py5.background(240)

    # Random dots
    py5.no_stroke()
    for i in range(100):
        x = py5.random(py5.width)
        y = py5.random(60, py5.height - 60)
        r = py5.random(5, 20)

        # Random color
        py5.fill(py5.random(255), py5.random(255), py5.random(255), 150)
        py5.ellipse(x, y, r, r)

    # Random line graph
    py5.stroke(0)
    py5.stroke_weight(2)
    py5.no_fill()
    py5.begin_shape()
    for x in range(0, py5.width, 10):
        y = py5.random(py5.height/2 - 100, py5.height/2 + 100)
        py5.vertex(x, y)
    py5.end_shape()

    # Explanation
    py5.fill(0)
    py5.no_stroke()
    py5.text_size(12)
    py5.text("random(): Each value is completely independent", 20, py5.height - 40)
    py5.text("Results are chaotic and unpredictable", 20, py5.height - 20)


def draw_noise_1d():
    """Demonstrate 1D Perlin noise - smooth, organic."""
    py5.background(240)

    # Noise line graph
    py5.stroke(0)
    py5.stroke_weight(2)
    py5.no_fill()
    py5.begin_shape()
    for x in range(py5.width):
        # noise() returns 0-1, so we scale it
        n = py5.noise(x * 0.01 + t)
        y = py5.remap(n, 0, 1, 100, py5.height - 100)
        py5.vertex(x, y)
    py5.end_shape()

    # Show noise values as dots
    py5.no_stroke()
    for x in range(0, py5.width, 20):
        n = py5.noise(x * 0.01 + t)
        y = py5.remap(n, 0, 1, 100, py5.height - 100)

        # Color based on noise value
        py5.fill(py5.remap(n, 0, 1, 50, 200), 100, 150)
        py5.ellipse(x, y, 15, 15)

    # Explanation
    py5.fill(0)
    py5.no_stroke()
    py5.text_size(12)
    py5.text("noise(x): Smooth, continuous values", 20, py5.height - 40)
    py5.text("Adjacent inputs produce similar outputs", 20, py5.height - 20)


def draw_noise_2d():
    """Demonstrate 2D Perlin noise - creates natural textures."""
    # Draw noise field
    py5.load_pixels()
    scale_factor = 0.01

    for x in range(py5.width):
        for y in range(py5.height - 50):
            n = py5.noise(x * scale_factor, y * scale_factor + t)
            brightness = int(n * 255)
            idx = x + y * py5.width
            py5.pixels[idx] = py5.color(brightness)

    py5.update_pixels()

    # Explanation overlay
    py5.fill(0, 200)
    py5.no_stroke()
    py5.rect(10, py5.height - 50, 400, 45, 5)

    py5.fill(255)
    py5.text_size(12)
    py5.text("noise(x, y): 2D noise creates natural textures", 20, py5.height - 30)
    py5.text("Like clouds, terrain, organic patterns", 20, py5.height - 12)


def draw_comparison():
    """Side by side comparison of random vs noise motion."""
    py5.background(30)

    # Dividing line
    py5.stroke(100)
    py5.stroke_weight(1)
    py5.line(py5.width/2, 50, py5.width/2, py5.height - 50)

    # Labels
    py5.fill(255)
    py5.no_stroke()
    py5.text_size(14)
    py5.text("random() motion", 100, 70)
    py5.text("noise() motion", py5.width/2 + 100, 70)

    # Update and draw particles
    py5.no_stroke()
    for i, p in enumerate(particles):
        # Random motion (left side)
        p['x'] += py5.random(-5, 5)
        p['y'] += py5.random(-5, 5)
        p['x'] = py5.constrain(p['x'], 20, py5.width/2 - 20)
        p['y'] = py5.constrain(p['y'], 100, py5.height - 60)

        py5.fill(219, 68, 55, 150)
        py5.ellipse(p['x'], p['y'], 10, 10)

        # Noise motion (right side)
        nx = py5.noise(i * 0.1, t) * 2 - 1
        ny = py5.noise(i * 0.1 + 100, t) * 2 - 1
        p['x2'] += nx * 3
        p['y2'] += ny * 3
        p['x2'] = py5.constrain(p['x2'], py5.width/2 + 20, py5.width - 20)
        p['y2'] = py5.constrain(p['y2'], 100, py5.height - 60)

        py5.fill(66, 133, 244, 150)
        py5.ellipse(p['x2'], p['y2'], 10, 10)

    # Explanation
    py5.fill(255)
    py5.text_size(12)
    py5.text("random(): Jittery, chaotic movement", 50, py5.height - 25)
    py5.text("noise(): Smooth, organic flow", py5.width/2 + 50, py5.height - 25)


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
        init_particles()
    elif py5.key == 'r':
        init_particles()
        py5.noise_seed(int(py5.random(10000)))
        print("Reset with new seed")
    elif py5.key == 's':
        filename = f"noise_{py5.frame_count}.png"
        py5.save(filename)
        print(f"Saved: {filename}")


# -------------------------------------------------
# Key Concepts:
#
# random(min, max):
# - Completely independent values
# - Good for: scatter, variety, chaos
#
# noise(x), noise(x, y), noise(x, y, z):
# - Smooth, continuous values (0 to 1)
# - Adjacent inputs = similar outputs
# - Good for: terrain, clouds, organic motion
#
# Noise parameters:
# - Scale: noise(x * 0.01) - lower = smoother
# - Offset: noise(x + t) - animates over time
# - noise_seed(): Reproducible results
#
# Connection to Renoir:
# When generating art inspired by Impressionists,
# noise creates the organic brush stroke variation
# that makes generative art feel more natural.
# -------------------------------------------------

py5.run_sketch()
