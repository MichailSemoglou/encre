"""
Lesson 15: Sound and Music Visualization (py5 version)
======================================================

Create visual responses to audio input using
simulated audio data.

Learning Objectives:
- Understand audio visualization concepts
- Map audio data to visual properties
- Create frequency-based animations
- Build responsive visual systems

Note: This lesson uses simulated audio data.
For real audio, you can use py5's sound capabilities
or external libraries like sounddevice.

Run with: python sound_music_py5.py
"""

import py5

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

    py5.size(800, 600)

    # Initialize simulated spectrum
    spectrum = [0] * num_bands
    waveform = [0] * 256

    palette = [
        py5.color(66, 133, 244),
        py5.color(219, 68, 55),
        py5.color(244, 180, 0),
        py5.color(15, 157, 88),
        py5.color(156, 39, 176),
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
    update_simulated_audio()

    # Decay beat timer
    if beat_timer > 0:
        beat_timer -= 1

    if mode == 0:
        draw_spectrum()
    elif mode == 1:
        draw_waveform()
    elif mode == 2:
        draw_circular()
    elif mode == 3:
        draw_particle_reactive()

    # Mode indicator
    py5.fill(255)
    py5.text_size(12)
    py5.text(f"Mode: {modes[mode]} | Press SPACE for beat", 20, 25)


def update_simulated_audio():
    """Generate simulated audio data using noise."""
    global spectrum, waveform

    # Simulate spectrum (bass heavy with decay)
    for i in range(num_bands):
        target = py5.noise(i * 0.1, t) * (1 - i / float(num_bands))
        # Add beat boost to low frequencies
        if beat_timer > 0 and i < 8:
            target += 0.5 * (beat_timer / 30.0)
        spectrum[i] = py5.lerp(spectrum[i], target, 0.3)

    # Simulate waveform
    for i in range(len(waveform)):
        waveform[i] = py5.noise(i * 0.02, t * 3) * 2 - 1
        # Add beat influence
        if beat_timer > 0:
            waveform[i] *= 1 + (beat_timer / 60.0)


def draw_spectrum():
    """Classic bar spectrum visualization."""
    py5.background(20)

    bar_width = py5.width / float(num_bands)

    for i in range(num_bands):
        bar_height = spectrum[i] * py5.height * 0.8

        col_index = int(py5.remap(i, 0, num_bands, 0, len(palette)))
        col_index = py5.constrain(col_index, 0, len(palette) - 1)
        col = palette[col_index]

        py5.no_stroke()
        py5.fill(col)
        py5.rect(i * bar_width, py5.height - bar_height, bar_width - 2, bar_height)

        if beat_timer > 0 and i < 10:
            py5.fill(255, beat_timer * 8)
            py5.rect(i * bar_width, py5.height - bar_height, bar_width - 2, bar_height)


def draw_waveform():
    """Oscilloscope-style waveform display."""
    py5.background(20)

    py5.stroke(50)
    py5.stroke_weight(1)
    py5.line(0, py5.height/2, py5.width, py5.height/2)

    py5.stroke(palette[0])
    py5.stroke_weight(2)
    py5.no_fill()

    py5.begin_shape()
    for i in range(len(waveform)):
        x = py5.remap(i, 0, len(waveform), 0, py5.width)
        y = py5.height/2 + waveform[i] * py5.height * 0.3
        py5.vertex(x, y)
    py5.end_shape()

    if beat_timer > 0:
        py5.no_stroke()
        py5.fill(255, beat_timer * 4)
        py5.rect(0, 0, py5.width, py5.height)


def draw_circular():
    """Circular frequency visualization."""
    py5.background(20)

    cx = py5.width / 2
    cy = py5.height / 2
    base_radius = 150

    py5.no_fill()
    py5.stroke_weight(3)

    for i in range(num_bands):
        angle1 = py5.remap(i, 0, num_bands, 0, py5.TWO_PI)

        r = base_radius + spectrum[i] * 200

        if beat_timer > 0:
            r += beat_timer * 2

        x1 = cx + py5.cos(angle1) * base_radius
        y1 = cy + py5.sin(angle1) * base_radius
        x2 = cx + py5.cos(angle1) * r
        y2 = cy + py5.sin(angle1) * r

        col = py5.lerp_color(palette[0], palette[4], float(i) / num_bands)
        py5.stroke(col)

        py5.line(x1, y1, x2, y2)

    py5.no_stroke()
    py5.fill(palette[2], 100)
    size_val = base_radius * 2 * (0.3 + spectrum[0] * 0.7)
    py5.ellipse(cx, cy, size_val, size_val)


def draw_particle_reactive():
    """Particle system reacting to audio."""
    global particles

    py5.no_stroke()
    py5.fill(20, 50)
    py5.rect(0, 0, py5.width, py5.height)

    if beat_timer == 29:
        for _ in range(30):
            particles.append({
                'x': py5.width/2,
                'y': py5.height/2,
                'vx': py5.random(-10, 10),
                'vy': py5.random(-10, 10),
                'life': 255,
                'col': palette[int(py5.random(len(palette)))]
            })

    if py5.random(1) < spectrum[0] * 2:
        particles.append({
            'x': py5.random(py5.width),
            'y': py5.height,
            'vx': py5.random(-2, 2),
            'vy': py5.random(-5, -2) * (1 + spectrum[0] * 3),
            'life': 255,
            'col': palette[int(py5.random(len(palette)))]
        })

    for i in range(len(particles) - 1, -1, -1):
        p = particles[i]

        p['vy'] += spectrum[0] * 0.5 - 0.1

        p['x'] += p['vx']
        p['y'] += p['vy']
        p['life'] -= 3

        py5.fill(py5.red(p['col']), py5.green(p['col']), py5.blue(p['col']), p['life'])
        size_val = py5.remap(p['life'], 0, 255, 2, 10)
        py5.ellipse(p['x'], p['y'], size_val, size_val)

        if p['life'] <= 0:
            particles.pop(i)

    while len(particles) > 500:
        particles.pop(0)

    py5.fill(255)
    py5.text_size(10)
    py5.text(f"Particles: {len(particles)}", 20, py5.height - 20)


def key_pressed():
    global mode, beat_timer, particles

    if py5.key == '1':
        mode = 0
    elif py5.key == '2':
        mode = 1
    elif py5.key == '3':
        mode = 2
    elif py5.key == '4':
        mode = 3
        particles = []
    elif py5.key == ' ':
        beat_timer = 30
    elif py5.key == 's':
        filename = f"sound_{py5.frame_count}.png"
        py5.save(filename)
        print(f"Saved: {filename}")


# -------------------------------------------------
# Sound Visualization Concepts:
#
# Audio Data Types:
# 1. Spectrum (FFT): Frequency amplitudes
# 2. Waveform: Amplitude over time
# 3. Beat Detection: Identify rhythm
#
# Mapping Audio to Visuals:
# - Amplitude -> Size, brightness, position
# - Frequency -> Color, position
# - Beat -> Pulse, spawn, flash
#
# For Real Audio:
# py5 can work with sounddevice or other
# audio libraries for real-time input.
# -------------------------------------------------

py5.run_sketch()
