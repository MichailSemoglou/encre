"""
Lesson 05: Randomness and Noise
===============================

Explore the difference between random() and noise(),
and learn to create organic, natural-looking patterns.

Learning Objectives:
- Understand random() vs noise()
- Create Perlin noise patterns
- Apply noise to motion and visuals
- Build natural-looking generative systems

Run this sketch in Processing with Python Mode enabled.
"""

# Mode control
mode = 0
modes = ["Random", "Noise 1D", "Noise 2D", "Comparison"]

# Animation
t = 0
particles = []


def setup():
    size(800, 600)
    noiseSeed(42)  # Consistent results
    initParticles()

    print("Lesson 05: Randomness and Noise")
    print("\nControls:")
    print("  Press 1-4 to switch modes")
    print("  Press 'r' to reset")
    print("  Press 's' to save image")


def initParticles():
    """Initialize particles for comparison mode."""
    global particles
    particles = []
    for i in range(50):
        particles.append({
            'x': width / 2,
            'y': height / 2,
            'x2': width / 2,
            'y2': height / 2
        })


def draw():
    global t
    t += 0.01

    if mode == 0:
        drawRandomDemo()
    elif mode == 1:
        drawNoise1D()
    elif mode == 2:
        drawNoise2D()
    elif mode == 3:
        drawComparison()

    # Mode indicator
    fill(0)
    noStroke()
    rect(0, 0, width, 35)
    fill(255)
    textSize(14)
    text("Mode: " + modes[mode] + " (Press 1-4 to switch)", 20, 24)


def drawRandomDemo():
    """Demonstrate random() - chaotic, unpredictable."""
    background(240)

    # Random dots
    noStroke()
    for i in range(100):
        x = random(width)
        y = random(60, height - 60)
        r = random(5, 20)

        # Random color
        fill(random(255), random(255), random(255), 150)
        ellipse(x, y, r, r)

    # Random line graph
    stroke(0)
    strokeWeight(2)
    noFill()
    beginShape()
    for x in range(0, width, 10):
        y = random(height/2 - 100, height/2 + 100)
        vertex(x, y)
    endShape()

    # Explanation
    fill(0)
    noStroke()
    textSize(12)
    text("random(): Each value is completely independent", 20, height - 40)
    text("Results are chaotic and unpredictable", 20, height - 20)


def drawNoise1D():
    """Demonstrate 1D Perlin noise - smooth, organic."""
    background(240)

    # Noise line graph
    stroke(0)
    strokeWeight(2)
    noFill()
    beginShape()
    for x in range(width):
        # noise() returns 0-1, so we scale it
        n = noise(x * 0.01 + t)
        y = map(n, 0, 1, 100, height - 100)
        vertex(x, y)
    endShape()

    # Show noise values as dots
    noStroke()
    for x in range(0, width, 20):
        n = noise(x * 0.01 + t)
        y = map(n, 0, 1, 100, height - 100)

        # Color based on noise value
        fill(map(n, 0, 1, 50, 200), 100, 150)
        ellipse(x, y, 15, 15)

    # Explanation
    fill(0)
    noStroke()
    textSize(12)
    text("noise(x): Smooth, continuous values", 20, height - 40)
    text("Adjacent inputs produce similar outputs", 20, height - 20)


def drawNoise2D():
    """Demonstrate 2D Perlin noise - creates natural textures."""
    # Draw noise field
    loadPixels()
    scale_factor = 0.01

    for x in range(width):
        for y in range(height - 50):
            n = noise(x * scale_factor, y * scale_factor + t)
            brightness = int(n * 255)
            idx = x + y * width
            pixels[idx] = color(brightness)

    updatePixels()

    # Explanation overlay
    fill(0, 200)
    noStroke()
    rect(10, height - 50, 400, 45, 5)

    fill(255)
    textSize(12)
    text("noise(x, y): 2D noise creates natural textures", 20, height - 30)
    text("Like clouds, terrain, organic patterns", 20, height - 12)


def drawComparison():
    """Side by side comparison of random vs noise motion."""
    background(30)

    # Dividing line
    stroke(100)
    strokeWeight(1)
    line(width/2, 50, width/2, height - 50)

    # Labels
    fill(255)
    noStroke()
    textSize(14)
    text("random() motion", 100, 70)
    text("noise() motion", width/2 + 100, 70)

    # Update and draw particles
    noStroke()
    for i, p in enumerate(particles):
        # Random motion (left side)
        p['x'] += random(-5, 5)
        p['y'] += random(-5, 5)
        p['x'] = constrain(p['x'], 20, width/2 - 20)
        p['y'] = constrain(p['y'], 100, height - 60)

        fill(219, 68, 55, 150)
        ellipse(p['x'], p['y'], 10, 10)

        # Noise motion (right side)
        nx = noise(i * 0.1, t) * 2 - 1
        ny = noise(i * 0.1 + 100, t) * 2 - 1
        p['x2'] += nx * 3
        p['y2'] += ny * 3
        p['x2'] = constrain(p['x2'], width/2 + 20, width - 20)
        p['y2'] = constrain(p['y2'], 100, height - 60)

        fill(66, 133, 244, 150)
        ellipse(p['x2'], p['y2'], 10, 10)

    # Explanation
    fill(255)
    textSize(12)
    text("random(): Jittery, chaotic movement", 50, height - 25)
    text("noise(): Smooth, organic flow", width/2 + 50, height - 25)


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
        initParticles()
    elif key == 'r':
        initParticles()
        noiseSeed(int(random(10000)))
        print("Reset with new seed")
    elif key == 's':
        filename = "noise_" + str(frameCount) + ".png"
        save(filename)
        print("Saved:", filename)


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
# - noiseSeed(): Reproducible results
#
# Connection to Renoir:
# When generating art inspired by Impressionists,
# noise creates the organic brush stroke variation
# that makes generative art feel more natural.
# -------------------------------------------------
