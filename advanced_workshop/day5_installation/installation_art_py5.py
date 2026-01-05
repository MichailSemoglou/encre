"""
Advanced Workshop - Day 5: Multi-modal Installation Art
======================================================

Create an interactive installation combining all techniques
from the workshop: CV, video processing, ML art, and shaders.

Prerequisites:
    pip install opencv-python numpy py5

Learning Objectives:
- Combine multiple input modalities
- Build interactive art installations
- Create generative responsive systems
- Design for physical space

Run with: python installation_art_py5.py
"""

import py5
import cv2
import numpy as np
from collections import deque

# ============================================
# SYSTEM COMPONENTS
# ============================================

# Camera input
cap = None
frame = None
prev_gray = None

# Face detection
face_cascade = None
faces = []

# Motion detection
motion_level = 0
motion_history = None
flow = None

# Particle system
particles = []
attractors = []

# Audio simulation (would use real audio in installation)
audio_level = 0
audio_spectrum = []

# Installation modes
mode = 0
modes = [
    "Presence Field",
    "Motion Painting",
    "Face Garden",
    "Sound Sculpture",
    "Collective Memory",
    "Full Installation"
]

# Time and animation
t = 0
installation_start = 0

# Color palettes for different modes
palettes = {
    'warm': [],
    'cool': [],
    'organic': [],
    'digital': []
}

# Memory buffer for collective visualization
memory_buffer = deque(maxlen=300)


def setup():
    global cap, face_cascade, motion_history, audio_spectrum
    global installation_start, palettes

    py5.size(1280, 720)

    # Initialize camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Face detection
    cv2_data_path = cv2.data.haarcascades
    face_cascade = cv2.CascadeClassifier(cv2_data_path + 'haarcascade_frontalface_default.xml')

    # Motion history buffer
    motion_history = np.zeros((480, 640), dtype=np.float32)

    # Simulated audio spectrum
    audio_spectrum = [0] * 32

    installation_start = py5.millis()

    # Initialize palettes
    palettes['warm'] = [
        py5.color(255, 107, 107),
        py5.color(255, 159, 67),
        py5.color(254, 202, 87),
        py5.color(255, 234, 167),
    ]
    palettes['cool'] = [
        py5.color(72, 219, 251),
        py5.color(29, 209, 161),
        py5.color(0, 148, 199),
        py5.color(16, 172, 132),
    ]
    palettes['organic'] = [
        py5.color(46, 64, 83),
        py5.color(88, 140, 126),
        py5.color(180, 215, 195),
        py5.color(240, 240, 210),
    ]
    palettes['digital'] = [
        py5.color(255, 0, 128),
        py5.color(0, 255, 255),
        py5.color(128, 0, 255),
        py5.color(255, 255, 0),
    ]

    print("=" * 70)
    print("Advanced Workshop Day 5: Multi-modal Installation Art")
    print("=" * 70)
    print("\nInstallation Modes:")
    for i, m in enumerate(modes):
        print(f"  {i+1}: {m}")
    print("\nControls:")
    print("  1-6: Switch modes")
    print("  SPACE: Add attractor at mouse")
    print("  c: Clear particles/memory")
    print("  s: Save screenshot")
    print("  f: Toggle fullscreen")
    print("  q: Quit")


def draw():
    global t, frame, prev_gray, faces, motion_level, flow, audio_level

    t += 0.02

    # Capture and process camera
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces_small = face_cascade.detectMultiScale(
            cv2.resize(gray, (320, 240)),
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        faces = [(x*2, y*2, w*2, h*2) for (x, y, w, h) in faces_small]

        # Calculate optical flow for motion
        if prev_gray is not None:
            flow = cv2.calcOpticalFlowFarneback(
                prev_gray, gray, None,
                pyr_scale=0.5, levels=3, winsize=15,
                iterations=3, poly_n=5, poly_sigma=1.2, flags=0
            )
            motion_level = np.mean(np.abs(flow)) * 10
        prev_gray = gray.copy()

    # Update simulated audio
    update_audio_simulation()

    # Draw based on mode
    if mode == 0:
        draw_presence_field()
    elif mode == 1:
        draw_motion_painting()
    elif mode == 2:
        draw_face_garden()
    elif mode == 3:
        draw_sound_sculpture()
    elif mode == 4:
        draw_collective_memory()
    elif mode == 5:
        draw_full_installation()

    # Update and draw particles (used in multiple modes)
    update_particles()

    # Draw UI
    draw_ui()


def update_audio_simulation():
    """Simulate audio input for demo purposes."""
    global audio_level, audio_spectrum

    # Use motion as proxy for sound (in real installation, use microphone)
    audio_level = motion_level * 0.5 + py5.noise(t * 0.5) * 0.5

    # Spectrum simulation
    for i in range(len(audio_spectrum)):
        target = py5.noise(i * 0.2, t) * (1 - i / len(audio_spectrum))
        audio_spectrum[i] = py5.lerp(audio_spectrum[i], target, 0.2)


def draw_presence_field():
    """Respond to human presence in space."""
    # Animated background
    py5.background(12, 12, 20)

    # Subtle animated pattern
    py5.stroke(20, 20, 35)
    py5.stroke_weight(1)
    for i in range(0, py5.width, 40):
        offset = py5.sin(i * 0.01 + t) * 10 * motion_level
        py5.line(i, 0, i + offset, py5.height)

    # Calculate presence intensity
    num_faces = len(faces)
    presence = py5.constrain(num_faces * 0.3 + motion_level * 0.1, 0, 1)

    # Ripple effect from face positions
    palette = palettes['cool']
    py5.no_fill()

    scale_x = py5.width / 640
    scale_y = py5.height / 480

    for (fx, fy, fw, fh) in faces:
        cx = (fx + fw/2) * scale_x
        cy = (fy + fh/2) * scale_y

        # Emanating rings
        num_rings = int(10 + presence * 20)
        for i in range(num_rings):
            radius = (i * 30 + t * 50) % (py5.width * 0.5)
            alpha = py5.remap(radius, 0, py5.width * 0.5, 200, 0)

            col = palette[i % len(palette)]
            py5.stroke(py5.red(col), py5.green(col), py5.blue(col), alpha)
            py5.stroke_weight(2)
            py5.ellipse(cx, cy, radius * 2, radius * 2)

    # Ambient particles responding to presence
    if presence > 0.2:
        for _ in range(int(presence * 5)):
            spawn_particle(py5.random(py5.width), py5.random(py5.height), palette)

    # No face message
    if num_faces == 0:
        py5.fill(100)
        py5.text_size(24)
        py5.text_align(py5.CENTER)
        py5.text("Awaiting presence...", py5.width/2, py5.height/2)
        py5.text_align(py5.LEFT)


def draw_motion_painting():
    """Create painting from movement."""
    # Fade effect
    py5.no_stroke()
    py5.fill(20, 20, 30, 10)
    py5.rect(0, 0, py5.width, py5.height)

    if flow is None or frame is None:
        return

    palette = palettes['warm']
    scale_x = py5.width / 640
    scale_y = py5.height / 480

    # Sample motion vectors and paint
    step = 20
    for y in range(0, 480, step):
        for x in range(0, 640, step):
            fx, fy = flow[y, x]
            magnitude = np.sqrt(fx*fx + fy*fy)

            if magnitude > 0.5:
                # Get color from camera
                b, g, r = frame[y, x]

                # Paint stroke
                px = x * scale_x
                py_val = y * scale_y

                angle = np.arctan2(fy, fx)
                length = magnitude * 10 * scale_x

                # Artistic brush stroke
                py5.push_matrix()
                py5.translate(px, py_val)
                py5.rotate(angle)

                # Color with slight variation
                py5.fill(r + py5.random(-20, 20),
                        g + py5.random(-20, 20),
                        b + py5.random(-20, 20), 150)
                py5.no_stroke()
                py5.ellipse(0, 0, length, length * 0.3)

                py5.pop_matrix()

    # Add drips based on motion intensity
    if motion_level > 0.3:
        for _ in range(int(motion_level * 10)):
            x = py5.random(py5.width)
            y = py5.random(py5.height)
            spawn_particle(x, y, palette, gravity=0.2)


def draw_face_garden():
    """Grow garden based on faces."""
    py5.background(240, 235, 225)

    palette = palettes['organic']
    scale_x = py5.width / 640
    scale_y = py5.height / 480

    # Draw growing elements from each face
    for (fx, fy, fw, fh) in faces:
        cx = (fx + fw/2) * scale_x
        cy = (fy + fh/2) * scale_y

        # Face size influences growth
        growth = fw / 100.0

        # Draw tree/plant structure
        draw_organic_growth(cx, cy, growth)

        # Spawn pollen/particles
        if py5.random(1) < 0.3:
            spawn_particle(
                cx + py5.random(-50, 50),
                cy + py5.random(-50, 50),
                palette,
                gravity=-0.05  # Float upward
            )

    # Ground line
    py5.stroke(88, 140, 126)
    py5.stroke_weight(3)
    py5.line(0, py5.height * 0.8, py5.width, py5.height * 0.8)

    # No face - dormant state
    if len(faces) == 0:
        py5.fill(100)
        py5.text_size(18)
        py5.text_align(py5.CENTER)
        py5.text("Garden awaits visitors...", py5.width/2, py5.height/2)
        py5.text_align(py5.LEFT)


def draw_organic_growth(x, y, growth):
    """Draw organic plant-like structure."""
    palette = palettes['organic']

    # Trunk
    py5.stroke(palette[0])
    py5.stroke_weight(3)

    # Recursive branches
    py5.push_matrix()
    py5.translate(x, y)

    depth = int(4 + growth * 3)
    draw_branch(0, 0, -py5.PI/2, 80 * growth, depth, palette)

    py5.pop_matrix()


def draw_branch(x, y, angle, length, depth, palette):
    """Recursively draw branches."""
    if depth <= 0 or length < 5:
        # Draw flower/leaf at end
        py5.fill(palette[2], 150)
        py5.no_stroke()
        py5.ellipse(x, y, 10, 10)
        return

    end_x = x + py5.cos(angle) * length
    end_y = y + py5.sin(angle) * length

    # Draw branch
    weight = py5.remap(depth, 0, 6, 1, 5)
    py5.stroke(palette[0 if depth > 3 else 1])
    py5.stroke_weight(weight)
    py5.line(x, y, end_x, end_y)

    # Branch out
    branch_angle = py5.PI/6 + py5.noise(x * 0.01, y * 0.01, t) * 0.3
    draw_branch(end_x, end_y, angle - branch_angle, length * 0.7, depth - 1, palette)
    draw_branch(end_x, end_y, angle + branch_angle, length * 0.7, depth - 1, palette)


def draw_sound_sculpture():
    """Visualize sound as 3D sculpture."""
    py5.background(15)

    palette = palettes['digital']
    cx = py5.width / 2
    cy = py5.height / 2

    # Central sculpture responding to audio
    py5.push_matrix()
    py5.translate(cx, cy)

    # Rotating structure
    num_layers = len(audio_spectrum)

    for i in range(num_layers):
        level = audio_spectrum[i]
        radius = 100 + i * 20

        py5.rotate(t * 0.01 * (i % 2 * 2 - 1))

        # Draw frequency band
        num_points = 8 + i * 2
        py5.no_fill()
        col = palette[i % len(palette)]
        py5.stroke(py5.red(col), py5.green(col), py5.blue(col), 150 + level * 100)
        py5.stroke_weight(1 + level * 3)

        py5.begin_shape()
        for j in range(num_points + 1):
            angle = j * py5.TWO_PI / num_points
            r = radius * (0.8 + level * 0.5)
            r += py5.sin(angle * 3 + t * 2) * 20 * level
            px = py5.cos(angle) * r
            py_val = py5.sin(angle) * r
            py5.vertex(px, py_val)
        py5.end_shape(py5.CLOSE)

    py5.pop_matrix()

    # Bass impact - full screen pulse
    bass_level = sum(audio_spectrum[:4]) / 4
    if bass_level > 0.5:
        py5.fill(palette[0], (bass_level - 0.5) * 100)
        py5.no_stroke()
        py5.rect(0, 0, py5.width, py5.height)

    # Motion adds particles
    if motion_level > 0.2:
        for _ in range(int(motion_level * 3)):
            angle = py5.random(py5.TWO_PI)
            dist = py5.random(100, 300)
            spawn_particle(
                cx + py5.cos(angle) * dist,
                cy + py5.sin(angle) * dist,
                palette
            )


def draw_collective_memory():
    """Build collective visual memory from all visitors."""
    py5.background(5, 5, 10)

    palette = palettes['warm']

    # Store current state in memory
    if len(faces) > 0:
        for (fx, fy, fw, fh) in faces:
            memory_buffer.append({
                'x': (fx + fw/2) / 640.0,
                'y': (fy + fh/2) / 480.0,
                'size': fw / 200.0,
                'time': t
            })

    # Draw memory traces
    scale_x = py5.width
    scale_y = py5.height

    py5.no_fill()
    for i, mem in enumerate(memory_buffer):
        age = t - mem['time']
        alpha = py5.remap(age, 0, 10, 200, 0)
        alpha = max(0, alpha)

        x = mem['x'] * scale_x
        y = mem['y'] * scale_y
        size = mem['size'] * 100

        col = palette[i % len(palette)]
        py5.stroke(py5.red(col), py5.green(col), py5.blue(col), alpha)
        py5.stroke_weight(1)
        py5.ellipse(x, y, size, size)

        # Connect to next memory
        if i < len(memory_buffer) - 1:
            next_mem = memory_buffer[i + 1]
            nx = next_mem['x'] * scale_x
            ny = next_mem['y'] * scale_y
            py5.line(x, y, nx, ny)

    # Current presence indicator
    for (fx, fy, fw, fh) in faces:
        cx = (fx + fw/2) * (py5.width / 640)
        cy = (fy + fh/2) * (py5.height / 480)

        py5.fill(255, 200)
        py5.no_stroke()
        py5.ellipse(cx, cy, 20, 20)

    # Info
    py5.fill(255)
    py5.text_size(14)
    py5.text(f"Memories stored: {len(memory_buffer)}", 20, py5.height - 40)


def draw_full_installation():
    """Combine all elements for full installation experience."""
    # Dynamic background based on presence and motion
    presence = len(faces) / 3.0
    bg_r = py5.lerp(10, 30, presence)
    bg_g = py5.lerp(10, 20, presence)
    bg_b = py5.lerp(20, 40, motion_level)
    py5.background(bg_r, bg_g, bg_b)

    # Layer 1: Motion painting (subtle)
    if flow is not None:
        draw_motion_traces()

    # Layer 2: Face-reactive elements
    if len(faces) > 0:
        draw_face_responses()

    # Layer 3: Sound visualization
    draw_audio_overlay()

    # Layer 4: Particles tie everything together
    # (particles drawn in main draw loop)

    # Layer 5: Memory traces
    draw_memory_overlay()


def draw_motion_traces():
    """Subtle motion visualization for full installation."""
    scale_x = py5.width / 640
    scale_y = py5.height / 480

    py5.stroke(255, 30)
    py5.stroke_weight(1)

    step = 30
    for y in range(0, 480, step):
        for x in range(0, 640, step):
            fx, fy = flow[y, x]
            magnitude = np.sqrt(fx*fx + fy*fy)

            if magnitude > 1:
                px = x * scale_x
                py_val = y * scale_y
                py5.line(px, py_val, px + fx * 5, py_val + fy * 5)


def draw_face_responses():
    """Face-reactive elements for full installation."""
    palette = palettes['cool']
    scale_x = py5.width / 640
    scale_y = py5.height / 480

    for (fx, fy, fw, fh) in faces:
        cx = (fx + fw/2) * scale_x
        cy = (fy + fh/2) * scale_y

        # Gentle glow
        for i in range(5):
            alpha = 50 - i * 10
            size = fw * scale_x * (1 + i * 0.3)
            col = palette[i % len(palette)]
            py5.fill(py5.red(col), py5.green(col), py5.blue(col), alpha)
            py5.no_stroke()
            py5.ellipse(cx, cy, size, size)

        # Spawn particles
        if py5.random(1) < 0.5:
            spawn_particle(cx, cy, palette)


def draw_audio_overlay():
    """Audio visualization overlay for full installation."""
    palette = palettes['digital']

    # Vertical bars at edges
    bar_width = py5.width / len(audio_spectrum) / 2

    py5.no_stroke()
    for i, level in enumerate(audio_spectrum):
        # Left side
        height = level * py5.height * 0.3
        col = palette[i % len(palette)]
        py5.fill(py5.red(col), py5.green(col), py5.blue(col), 100)
        py5.rect(i * bar_width, py5.height - height, bar_width - 2, height)

        # Right side (mirrored)
        py5.rect(py5.width - (i + 1) * bar_width, py5.height - height, bar_width - 2, height)


def draw_memory_overlay():
    """Memory traces overlay for full installation."""
    # Show recent memory as connecting lines
    if len(memory_buffer) > 1:
        py5.stroke(255, 50)
        py5.stroke_weight(1)
        py5.no_fill()

        py5.begin_shape()
        for mem in list(memory_buffer)[-50:]:  # Last 50 memories
            x = mem['x'] * py5.width
            y = mem['y'] * py5.height
            py5.vertex(x, y)
        py5.end_shape()


def spawn_particle(x, y, palette, gravity=0):
    """Spawn a particle at position."""
    particles.append({
        'x': x,
        'y': y,
        'vx': py5.random(-2, 2),
        'vy': py5.random(-2, 2),
        'gravity': gravity,
        'life': 255,
        'size': py5.random(3, 10),
        'col': palette[int(py5.random(len(palette)))]
    })


def update_particles():
    """Update and draw all particles."""
    # Limit particles
    while len(particles) > 500:
        particles.pop(0)

    py5.no_stroke()
    for i in range(len(particles) - 1, -1, -1):
        p = particles[i]

        # Apply attractors
        for att in attractors:
            dx = att['x'] - p['x']
            dy = att['y'] - p['y']
            dist = max(10, py5.sqrt(dx*dx + dy*dy))
            force = att['strength'] / (dist * dist) * 50
            p['vx'] += (dx / dist) * force
            p['vy'] += (dy / dist) * force

        # Update
        p['x'] += p['vx']
        p['y'] += p['vy']
        p['vy'] += p['gravity']
        p['vx'] *= 0.99
        p['vy'] *= 0.99
        p['life'] -= 2

        # Draw
        py5.fill(py5.red(p['col']), py5.green(p['col']), py5.blue(p['col']), p['life'])
        py5.ellipse(p['x'], p['y'], p['size'], p['size'])

        # Remove dead
        if p['life'] <= 0:
            particles.pop(i)


def draw_ui():
    """Draw installation info."""
    py5.fill(0, 150)
    py5.no_stroke()
    py5.rect(10, 10, 350, 90, 5)

    py5.fill(255)
    py5.text_size(14)
    py5.text(f"Installation Mode: {modes[mode]}", 20, 32)

    py5.text_size(11)
    elapsed = (py5.millis() - installation_start) / 1000
    py5.text(f"Time: {int(elapsed)}s | Faces: {len(faces)} | Motion: {motion_level:.2f}", 20, 55)
    py5.text(f"Particles: {len(particles)} | Memories: {len(memory_buffer)}", 20, 70)
    py5.text(f"Press 1-{len(modes)} to switch modes", 20, 85)


def key_pressed():
    global mode, particles, attractors, memory_buffer

    if py5.key in '123456':
        mode = int(py5.key) - 1
        particles = []  # Clear particles on mode change
    elif py5.key == ' ':
        # Add attractor at mouse
        attractors.append({
            'x': py5.mouse_x,
            'y': py5.mouse_y,
            'strength': 1.0
        })
        # Limit attractors
        if len(attractors) > 5:
            attractors.pop(0)
    elif py5.key == 'c':
        particles = []
        attractors = []
        memory_buffer.clear()
        print("Cleared particles, attractors, and memory")
    elif py5.key == 'f':
        # Toggle fullscreen (platform dependent)
        pass
    elif py5.key == 's':
        filename = f"installation_{modes[mode].replace(' ', '_')}_{py5.millis()}.png"
        py5.save(filename)
        print(f"Saved: {filename}")
    elif py5.key == 'q':
        cleanup()
        py5.exit_sketch()


def cleanup():
    """Release resources."""
    global cap
    if cap is not None:
        cap.release()


import atexit
atexit.register(cleanup)


# -------------------------------------------------
# Installation Art Concepts:
#
# 1. Multi-modal Input:
#    - Camera for presence/motion
#    - Face detection for interaction
#    - Audio for sound response
#    - Time for evolution
#
# 2. Layered Visualization:
#    - Background (shader/ambient)
#    - Motion layer
#    - Face-reactive layer
#    - Audio layer
#    - Particle system
#    - Memory/history
#
# 3. Installation Design:
#    - Consider physical space
#    - Calibrate for environment
#    - Test with multiple visitors
#    - Plan for edge cases
#
# 4. Technical Requirements:
#    - Reliable camera input
#    - Consistent frame rate
#    - Error recovery
#    - Long-duration stability
#
# Extensions:
# - Add MIDI controller support
# - Implement OSC for networked control
# - Create projection mapping
# - Build physical interface
# - Add data logging/playback
# -------------------------------------------------

py5.run_sketch()
