"""
Advanced Workshop - Day 1: Computer Vision & Face Detection
===========================================================

Create interactive generative art that responds to faces
using OpenCV and py5.

Prerequisites:
    pip install opencv-python numpy

Learning Objectives:
- Capture webcam video in py5
- Detect faces using OpenCV Haar cascades
- Track facial landmarks
- Create face-reactive generative art
- Map facial features to visual parameters

Run with: python face_detection_py5.py
"""

import py5
import cv2
import numpy as np
from pathlib import Path

# OpenCV setup
cap = None
face_cascade = None
eye_cascade = None

# Detection results
faces = []
eyes = []

# Visualization mode
mode = 0
modes = ["Mirror", "Particle Aura", "Face Mesh", "Abstract Portrait", "Emotion Colors"]

# Particles for aura effect
particles = []

# Palette (changes based on face position)
palette = []

# Frame for processing
frame = None
frame_small = None


def setup():
    global cap, face_cascade, eye_cascade, palette

    py5.size(1280, 720)

    # Initialize webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Load Haar cascade classifiers
    cv2_data_path = cv2.data.haarcascades
    face_cascade = cv2.CascadeClassifier(cv2_data_path + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2_data_path + 'haarcascade_eye.xml')

    # Initialize palette
    palette = [
        py5.color(66, 133, 244),
        py5.color(219, 68, 55),
        py5.color(244, 180, 0),
        py5.color(15, 157, 88),
        py5.color(156, 39, 176),
    ]

    print("=" * 60)
    print("Advanced Workshop Day 1: Face Detection & Generative Art")
    print("=" * 60)
    print("\nControls:")
    print("  1-5: Switch visualization modes")
    print("  s: Save screenshot")
    print("  q: Quit")
    print("\nModes:")
    for i, m in enumerate(modes):
        print(f"  {i+1}: {m}")


def draw():
    global frame, frame_small, faces, eyes

    # Capture frame from webcam
    ret, frame = cap.read()
    if not ret:
        py5.background(0)
        py5.fill(255)
        py5.text("No webcam detected", py5.width/2 - 80, py5.height/2)
        return

    # Flip horizontally for mirror effect
    frame = cv2.flip(frame, 1)

    # Convert to grayscale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces (use smaller frame for performance)
    frame_small = cv2.resize(gray, (0, 0), fx=0.5, fy=0.5)
    faces_small = face_cascade.detectMultiScale(
        frame_small,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Scale back to original size
    faces = [(x*2, y*2, w*2, h*2) for (x, y, w, h) in faces_small]

    # Detect eyes within each face
    eyes = []
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        detected_eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in detected_eyes:
            eyes.append((x + ex, y + ey, ew, eh))

    # Render based on mode
    if mode == 0:
        draw_mirror()
    elif mode == 1:
        draw_particle_aura()
    elif mode == 2:
        draw_face_mesh()
    elif mode == 3:
        draw_abstract_portrait()
    elif mode == 4:
        draw_emotion_colors()

    # Draw UI
    draw_ui()


def draw_mirror():
    """Simple mirror with face detection overlay."""
    # Convert BGR to RGB for py5
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = py5.create_image_from_numpy(frame_rgb, 'RGB')
    py5.image(img, 0, 0)

    # Draw face rectangles
    py5.no_fill()
    py5.stroke(0, 255, 0)
    py5.stroke_weight(3)

    for (x, y, w, h) in faces:
        py5.rect(x, y, w, h)

    # Draw eye circles
    py5.stroke(0, 255, 255)
    py5.stroke_weight(2)

    for (x, y, w, h) in eyes:
        py5.ellipse(x + w/2, y + h/2, w, h)


def draw_particle_aura():
    """Particles emanate from detected faces."""
    global particles

    py5.background(20)

    # Spawn particles from face centers
    for (x, y, w, h) in faces:
        center_x = x + w/2
        center_y = y + h/2

        # Spawn particles based on face size
        num_spawn = int(w * h / 5000) + 3
        for _ in range(num_spawn):
            angle = py5.random(py5.TWO_PI)
            speed = py5.random(2, 6)
            particles.append({
                'x': center_x + py5.random(-w/4, w/4),
                'y': center_y + py5.random(-h/4, h/4),
                'vx': py5.cos(angle) * speed,
                'vy': py5.sin(angle) * speed,
                'life': 255,
                'size': py5.random(5, 15),
                'col': palette[int(py5.random(len(palette)))]
            })

    # Update and draw particles
    py5.no_stroke()
    for i in range(len(particles) - 1, -1, -1):
        p = particles[i]
        p['x'] += p['vx']
        p['y'] += p['vy']
        p['vy'] += 0.1  # Slight gravity
        p['life'] -= 4

        py5.fill(py5.red(p['col']), py5.green(p['col']), py5.blue(p['col']), p['life'])
        py5.ellipse(p['x'], p['y'], p['size'], p['size'])

        if p['life'] <= 0:
            particles.pop(i)

    # Limit particles
    while len(particles) > 1000:
        particles.pop(0)

    # Draw face silhouettes
    py5.fill(255, 30)
    py5.no_stroke()
    for (x, y, w, h) in faces:
        py5.ellipse(x + w/2, y + h/2, w, h * 1.3)

    # Particle count
    py5.fill(255)
    py5.text_size(12)
    py5.text(f"Particles: {len(particles)}", 20, py5.height - 20)


def draw_face_mesh():
    """Generative mesh based on face proportions."""
    py5.background(30)

    if not faces:
        py5.fill(100)
        py5.text_size(24)
        py5.text_align(py5.CENTER)
        py5.text("No face detected - show your face to the camera", py5.width/2, py5.height/2)
        py5.text_align(py5.LEFT)
        return

    for (x, y, w, h) in faces:
        cx = x + w/2
        cy = y + h/2

        # Create mesh based on face dimensions
        cols = 20
        rows = 25
        cell_w = w / cols
        cell_h = h / rows

        py5.stroke(255, 100)
        py5.stroke_weight(1)
        py5.no_fill()

        # Draw distorted mesh
        for i in range(cols):
            for j in range(rows):
                px = x + i * cell_w
                py_val = y + j * cell_h

                # Distortion based on distance from center
                dx = px - cx
                dy = py_val - cy
                dist = py5.sqrt(dx*dx + dy*dy)
                distortion = py5.sin(dist * 0.05 + py5.frame_count * 0.05) * 10

                px += distortion * (dx / (dist + 1)) * 0.3
                py_val += distortion * (dy / (dist + 1)) * 0.3

                # Color based on position
                hue = py5.remap(i + j, 0, cols + rows, 0, 360)
                py5.color_mode(py5.HSB, 360, 100, 100)
                py5.stroke(hue, 70, 90, 150)
                py5.color_mode(py5.RGB, 255)

                py5.point(px, py_val)

                # Connect to neighbors
                if i < cols - 1:
                    next_px = x + (i+1) * cell_w
                    next_py = y + j * cell_h
                    py5.line(px, py_val, next_px, next_py)

                if j < rows - 1:
                    next_px = x + i * cell_w
                    next_py = y + (j+1) * cell_h
                    py5.line(px, py_val, next_px, next_py)

        # Eyes as focal points
        for (ex, ey, ew, eh) in eyes:
            py5.fill(255)
            py5.no_stroke()
            py5.ellipse(ex + ew/2, ey + eh/2, 10, 10)


def draw_abstract_portrait():
    """Abstract interpretation of detected face."""
    # Fade background
    py5.no_stroke()
    py5.fill(20, 30)
    py5.rect(0, 0, py5.width, py5.height)

    if not faces:
        return

    for (x, y, w, h) in faces:
        cx = x + w/2
        cy = y + h/2

        # Abstract face shapes
        py5.no_fill()
        py5.stroke_weight(2)

        # Head outline - multiple circles
        for i in range(5):
            offset = py5.sin(py5.frame_count * 0.03 + i) * 20
            py5.stroke(palette[i % len(palette)], 100)
            py5.ellipse(cx + offset, cy, w + i * 20, h * 1.2 + i * 20)

        # Eye interpretations
        for (ex, ey, ew, eh) in eyes:
            ecx = ex + ew/2
            ecy = ey + eh/2

            # Concentric circles
            for r in range(5):
                py5.stroke(255, 200 - r * 40)
                py5.ellipse(ecx, ecy, ew + r * 15, eh + r * 15)

            # Radiating lines
            py5.stroke(palette[0], 150)
            for angle in range(0, 360, 30):
                rad = py5.radians(angle + py5.frame_count)
                py5.line(ecx, ecy,
                        ecx + py5.cos(rad) * 50,
                        ecy + py5.sin(rad) * 50)

        # Flowing lines from face center
        py5.stroke(palette[2], 80)
        py5.stroke_weight(1)
        for i in range(10):
            angle = py5.noise(i * 0.5, py5.frame_count * 0.01) * py5.TWO_PI * 2
            length = w * 0.8
            py5.line(cx, cy,
                    cx + py5.cos(angle) * length,
                    cy + py5.sin(angle) * length)


def draw_emotion_colors():
    """Color field that responds to face position and size."""
    py5.background(30)

    if not faces:
        # Ambient animation when no face
        py5.color_mode(py5.HSB, 360, 100, 100)
        for i in range(20):
            for j in range(15):
                x = i * (py5.width / 20)
                y = j * (py5.height / 15)
                hue = (i * 20 + j * 10 + py5.frame_count) % 360
                py5.fill(hue, 30, 50)
                py5.no_stroke()
                py5.rect(x, y, py5.width/20 + 1, py5.height/15 + 1)
        py5.color_mode(py5.RGB, 255)

        py5.fill(255)
        py5.text_size(18)
        py5.text_align(py5.CENTER)
        py5.text("Show your face to influence the colors", py5.width/2, py5.height - 50)
        py5.text_align(py5.LEFT)
        return

    # Face influences color field
    for (fx, fy, fw, fh) in faces:
        face_cx = fx + fw/2
        face_cy = fy + fh/2

        py5.color_mode(py5.HSB, 360, 100, 100)
        py5.no_stroke()

        cell_size = 40
        for x in range(0, py5.width, cell_size):
            for y in range(0, py5.height, cell_size):
                # Distance from face center
                dx = x - face_cx
                dy = y - face_cy
                dist = py5.sqrt(dx*dx + dy*dy)

                # Hue based on angle to face
                angle = py5.atan2(dy, dx)
                hue = (py5.degrees(angle) + 180 + py5.frame_count) % 360

                # Saturation based on distance
                sat = py5.remap(dist, 0, 500, 100, 30)
                sat = py5.constrain(sat, 30, 100)

                # Brightness influenced by face size
                bri = py5.remap(fw, 100, 400, 40, 90)
                bri = py5.constrain(bri, 40, 90)

                py5.fill(hue, sat, bri)
                py5.rect(x, y, cell_size + 1, cell_size + 1)

        py5.color_mode(py5.RGB, 255)

        # Face indicator
        py5.no_fill()
        py5.stroke(255)
        py5.stroke_weight(2)
        py5.ellipse(face_cx, face_cy, fw * 0.3, fh * 0.3)


def draw_ui():
    """Draw mode indicator."""
    py5.fill(0, 180)
    py5.no_stroke()
    py5.rect(10, 10, 250, 55, 5)

    py5.fill(255)
    py5.text_size(14)
    py5.text(f"Mode {mode + 1}: {modes[mode]}", 20, 32)
    py5.text_size(11)
    py5.text(f"Faces: {len(faces)} | Eyes: {len(eyes)}", 20, 55)


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
    elif py5.key == '5':
        mode = 4
    elif py5.key == 's':
        filename = f"face_art_{py5.millis()}.png"
        py5.save(filename)
        print(f"Saved: {filename}")
    elif py5.key == 'q':
        cleanup()
        py5.exit_sketch()


def cleanup():
    """Release webcam resources."""
    global cap
    if cap is not None:
        cap.release()


# Ensure cleanup on exit
import atexit
atexit.register(cleanup)


# -------------------------------------------------
# Advanced Concepts:
#
# 1. OpenCV Integration:
#    - cv2.VideoCapture for webcam
#    - Haar cascades for detection
#    - Image format conversion (BGR->RGB)
#
# 2. Face Detection:
#    - detectMultiScale() parameters
#    - ROI (Region of Interest) for eyes
#    - Performance optimization (scaling)
#
# 3. Creative Applications:
#    - Face as input for generative systems
#    - Mapping facial features to parameters
#    - Real-time responsive art
#
# Extensions:
# - Add facial landmark detection (dlib)
# - Implement emotion detection (ML)
# - Create face-swapping effects
# - Build interactive installations
# -------------------------------------------------

py5.run_sketch()
