"""
Lesson 15: Sound and Music Visualization
========================================

Create visual responses to audio input using
simulated audio data.

Learning Objectives:
- Understand audio visualization concepts
- Map audio data to visual properties
- Create frequency-based animations
- Build responsive visual systems

Note: This lesson uses simulated audio data.
For real audio, use the Minim library in Processing
or py5's sound capabilities.

Run this sketch in Processing with Python Mode enabled.
"""

# Simulated audio data
num_bands = 64
spectrum = []
waveform = []
beat_detected = False
beat_timer = 0

# Visualization mode
mode = 0
modes = ["Spectrum", "Waveform", "Circular", "Particles"]

# Animation
t = 0

# Palette
palette = []

# Particles for mode 3
particles = []


def setup():
    global spectrum, waveform, palette

    size(800, 600)

    # Initialize simulated spectrum
    spectrum = [0] * num_bands
    waveform = [0] * 256

    palette = [
        color(66, 133, 244),
        color(219, 68, 55),
        color(244, 180, 0),
        color(15, 157, 88),
        color(156, 39, 176),
    ]

    print("Lesson 15: Sound Visualization")
    print("\nControls:")
    print("  Press 1-4 to switch modes")
    print("  Press SPACE to simulate beat")
    print("  Press 's' to save image")


def draw():
    global t, beat_timer
    t += 0.02

    # Update simulated audio
    updateSimulatedAudio()

    # Decay beat timer
    if beat_timer > 0:
        beat_timer -= 1

    if mode == 0:
        drawSpectrum()
    elif mode == 1:
        drawWaveform()
    elif mode == 2:
        drawCircular()
    elif mode == 3:
        drawParticleReactive()

    # Mode indicator
    fill(255)
    textSize(12)
    text("Mode: " + modes[mode] + " | Press SPACE for beat", 20, 25)


def updateSimulatedAudio():
    """Generate simulated audio data using noise."""
    global spectrum, waveform, beat_detected

    # Simulate spectrum (bass heavy with decay)
    for i in range(num_bands):
        target = noise(i * 0.1, t) * (1 - i / float(num_bands))
        # Add beat boost to low frequencies
        if beat_timer > 0 and i < 8:
            target += 0.5 * (beat_timer / 30.0)
        spectrum[i] = lerp(spectrum[i], target, 0.3)

    # Simulate waveform
    for i in range(len(waveform)):
        waveform[i] = noise(i * 0.02, t * 3) * 2 - 1
        # Add beat influence
        if beat_timer > 0:
            waveform[i] *= 1 + (beat_timer / 60.0)


def drawSpectrum():
    """Classic bar spectrum visualization."""
    background(20)

    bar_width = width / float(num_bands)

    for i in range(num_bands):
        # Map frequency to height
        bar_height = spectrum[i] * height * 0.8

        # Color based on frequency
        col_index = int(map(i, 0, num_bands, 0, len(palette)))
        col_index = constrain(col_index, 0, len(palette) - 1)
        col = palette[col_index]

        # Draw bar
        noStroke()
        fill(col)
        rect(i * bar_width, height - bar_height, bar_width - 2, bar_height)

        # Glow effect on beat
        if beat_timer > 0 and i < 10:
            fill(255, beat_timer * 8)
            rect(i * bar_width, height - bar_height, bar_width - 2, bar_height)


def drawWaveform():
    """Oscilloscope-style waveform display."""
    background(20)

    # Draw center line
    stroke(50)
    strokeWeight(1)
    line(0, height/2, width, height/2)

    # Draw waveform
    stroke(palette[0])
    strokeWeight(2)
    noFill()

    beginShape()
    for i in range(len(waveform)):
        x = map(i, 0, len(waveform), 0, width)
        y = height/2 + waveform[i] * height * 0.3
        vertex(x, y)
    endShape()

    # Beat flash
    if beat_timer > 0:
        noStroke()
        fill(255, beat_timer * 4)
        rect(0, 0, width, height)


def drawCircular():
    """Circular frequency visualization."""
    background(20)

    cx = width / 2
    cy = height / 2
    base_radius = 150

    # Draw circular spectrum
    noFill()
    strokeWeight(3)

    for i in range(num_bands):
        angle1 = map(i, 0, num_bands, 0, TWO_PI)
        angle2 = map(i + 1, 0, num_bands, 0, TWO_PI)

        # Radius based on amplitude
        r = base_radius + spectrum[i] * 200

        # Beat pulse
        if beat_timer > 0:
            r += beat_timer * 2

        x1 = cx + cos(angle1) * base_radius
        y1 = cy + sin(angle1) * base_radius
        x2 = cx + cos(angle1) * r
        y2 = cy + sin(angle1) * r

        # Color gradient
        col = lerpColor(palette[0], palette[4], float(i) / num_bands)
        stroke(col)

        line(x1, y1, x2, y2)

    # Center circle
    noStroke()
    fill(palette[2], 100)
    ellipse(cx, cy, base_radius * 2 * (0.3 + spectrum[0] * 0.7), base_radius * 2 * (0.3 + spectrum[0] * 0.7))


def drawParticleReactive():
    """Particle system reacting to audio."""
    global particles

    # Semi-transparent background for trails
    noStroke()
    fill(20, 50)
    rect(0, 0, width, height)

    # Spawn particles on beat
    if beat_timer == 29:  # Just detected
        for _ in range(30):
            particles.append({
                'x': width/2,
                'y': height/2,
                'vx': random(-10, 10),
                'vy': random(-10, 10),
                'life': 255,
                'col': palette[int(random(len(palette)))]
            })

    # Spawn particles based on bass
    if random(1) < spectrum[0] * 2:
        particles.append({
            'x': random(width),
            'y': height,
            'vx': random(-2, 2),
            'vy': random(-5, -2) * (1 + spectrum[0] * 3),
            'life': 255,
            'col': palette[int(random(len(palette)))]
        })

    # Update and draw particles
    for i in range(len(particles) - 1, -1, -1):
        p = particles[i]

        # Audio reactivity
        p['vy'] += spectrum[0] * 0.5 - 0.1

        p['x'] += p['vx']
        p['y'] += p['vy']
        p['life'] -= 3

        # Draw
        fill(red(p['col']), green(p['col']), blue(p['col']), p['life'])
        size_val = map(p['life'], 0, 255, 2, 10)
        ellipse(p['x'], p['y'], size_val, size_val)

        # Remove dead particles
        if p['life'] <= 0:
            particles.pop(i)

    # Limit particles
    while len(particles) > 500:
        particles.pop(0)

    # Particle count
    fill(255)
    textSize(10)
    text("Particles: " + str(len(particles)), 20, height - 20)


def keyPressed():
    global mode, beat_timer, particles

    if key == '1':
        mode = 0
    elif key == '2':
        mode = 1
    elif key == '3':
        mode = 2
    elif key == '4':
        mode = 3
        particles = []
    elif key == ' ':
        beat_timer = 30  # Simulate beat detection
    elif key == 's':
        filename = "sound_" + str(frameCount) + ".png"
        save(filename)
        print("Saved:", filename)


# -------------------------------------------------
# Sound Visualization Concepts:
#
# Audio Data Types:
# 1. Spectrum (FFT): Frequency amplitudes
#    - Low indices = bass (low freq)
#    - High indices = treble (high freq)
#
# 2. Waveform: Amplitude over time
#    - Values between -1 and 1
#    - Shows audio shape
#
# 3. Beat Detection: Identify rhythm
#    - Usually based on bass threshold
#
# Mapping Audio to Visuals:
# - Amplitude -> Size, brightness, position
# - Frequency -> Color, position
# - Beat -> Pulse, spawn, flash
#
# For Real Audio:
# Processing: Use Minim library
# py5: Use py5.sound module
#
# Connection to Renoir:
# Audio visualization can use artist palettes
# to create genre-specific visual styles.
# -------------------------------------------------
