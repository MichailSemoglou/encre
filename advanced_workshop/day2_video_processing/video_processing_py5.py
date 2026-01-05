"""
Advanced Workshop - Day 2: Real-time Video Processing
=====================================================

Explore advanced video effects including optical flow,
motion detection, and creative video manipulations.

Prerequisites:
    pip install opencv-python numpy

Learning Objectives:
- Implement optical flow for motion tracking
- Create video delay and slit-scan effects
- Build motion-reactive visualizations
- Apply real-time video filters

Run with: python video_processing_py5.py
"""

import py5
import cv2
import numpy as np
from collections import deque

# OpenCV setup
cap = None
prev_gray = None

# Optical flow
flow = None
flow_scale = 10

# Frame buffer for delay effects
frame_buffer = None
buffer_size = 60
buffer_index = 0

# Slit-scan
slit_image = None
slit_position = 0

# Motion detection
motion_mask = None
motion_threshold = 30
motion_history = None

# Visualization mode
mode = 0
modes = ["Optical Flow", "Motion Trail", "Slit-Scan", "Pixel Sort", "Glitch", "Time Displacement"]

# Frame
frame = None


def setup():
    global cap, frame_buffer, slit_image, motion_history

    py5.size(1280, 720)

    # Initialize webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Initialize frame buffer
    frame_buffer = deque(maxlen=buffer_size)

    # Initialize slit-scan image
    slit_image = np.zeros((720, 1280, 3), dtype=np.uint8)

    # Motion history
    motion_history = np.zeros((720, 1280), dtype=np.float32)

    print("=" * 60)
    print("Advanced Workshop Day 2: Real-time Video Processing")
    print("=" * 60)
    print("\nControls:")
    print("  1-6: Switch visualization modes")
    print("  r: Reset effect")
    print("  s: Save screenshot")
    print("  q: Quit")
    print("\nModes:")
    for i, m in enumerate(modes):
        print(f"  {i+1}: {m}")


def draw():
    global frame, prev_gray, flow

    # Capture frame
    ret, frame = cap.read()
    if not ret:
        py5.background(0)
        py5.fill(255)
        py5.text("No webcam detected", py5.width/2 - 80, py5.height/2)
        return

    # Flip horizontally
    frame = cv2.flip(frame, 1)

    # Convert to grayscale for processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate optical flow
    if prev_gray is not None:
        flow = cv2.calcOpticalFlowFarneback(
            prev_gray, gray,
            None,
            pyr_scale=0.5,
            levels=3,
            winsize=15,
            iterations=3,
            poly_n=5,
            poly_sigma=1.2,
            flags=0
        )

    prev_gray = gray.copy()

    # Store frame in buffer
    frame_buffer.append(frame.copy())

    # Render based on mode
    if mode == 0:
        draw_optical_flow()
    elif mode == 1:
        draw_motion_trail(gray)
    elif mode == 2:
        draw_slit_scan()
    elif mode == 3:
        draw_pixel_sort()
    elif mode == 4:
        draw_glitch()
    elif mode == 5:
        draw_time_displacement()

    # Draw UI
    draw_ui()


def draw_optical_flow():
    """Visualize optical flow vectors."""
    py5.background(0)

    if flow is None:
        # Show original frame while waiting
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = py5.create_image_from_numpy(frame_rgb, 'RGB')
        py5.tint(255, 100)
        py5.image(img, 0, 0)
        py5.no_tint()
        return

    # Show darkened video
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = py5.create_image_from_numpy(frame_rgb, 'RGB')
    py5.tint(255, 80)
    py5.image(img, 0, 0)
    py5.no_tint()

    # Draw flow vectors
    step = 20
    for y in range(0, py5.height, step):
        for x in range(0, py5.width, step):
            if y < flow.shape[0] and x < flow.shape[1]:
                fx, fy = flow[y, x]
                magnitude = np.sqrt(fx*fx + fy*fy)

                if magnitude > 1:
                    # Color based on direction
                    angle = np.arctan2(fy, fx)
                    hue = py5.remap(angle, -np.pi, np.pi, 0, 360)

                    py5.color_mode(py5.HSB, 360, 100, 100)
                    py5.stroke(hue, 80, 100)
                    py5.stroke_weight(py5.constrain(magnitude * 0.5, 1, 4))
                    py5.color_mode(py5.RGB, 255)

                    end_x = x + fx * flow_scale
                    end_y = y + fy * flow_scale
                    py5.line(x, y, end_x, end_y)

                    # Draw arrowhead
                    py5.push_matrix()
                    py5.translate(end_x, end_y)
                    py5.rotate(angle)
                    py5.line(0, 0, -5, -3)
                    py5.line(0, 0, -5, 3)
                    py5.pop_matrix()


def draw_motion_trail(gray):
    """Create motion trails using frame differencing."""
    global motion_history

    if len(frame_buffer) < 2:
        return

    # Frame difference
    prev_frame = cv2.cvtColor(frame_buffer[-2], cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gray, prev_frame)

    # Threshold
    _, motion_mask = cv2.threshold(diff, motion_threshold, 255, cv2.THRESH_BINARY)

    # Update motion history
    motion_history = motion_history * 0.95
    motion_history[motion_mask > 0] = 255

    # Create colored visualization
    py5.background(20)

    # Show current frame dimmed
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = py5.create_image_from_numpy(frame_rgb, 'RGB')
    py5.tint(255, 60)
    py5.image(img, 0, 0)
    py5.no_tint()

    # Draw motion history as colored overlay
    history_normalized = (motion_history / 255.0).astype(np.float32)

    # Create color-coded motion image
    motion_colored = np.zeros((motion_history.shape[0], motion_history.shape[1], 3), dtype=np.uint8)
    motion_colored[:, :, 0] = (history_normalized * 100).astype(np.uint8)  # R
    motion_colored[:, :, 1] = (history_normalized * 200).astype(np.uint8)  # G
    motion_colored[:, :, 2] = (history_normalized * 255).astype(np.uint8)  # B

    motion_img = py5.create_image_from_numpy(motion_colored, 'RGB')
    py5.blend_mode(py5.ADD)
    py5.image(motion_img, 0, 0)
    py5.blend_mode(py5.BLEND)


def draw_slit_scan():
    """Create slit-scan effect - each column from different time."""
    global slit_image, slit_position

    if len(frame_buffer) < buffer_size:
        # Show loading progress
        py5.background(0)
        py5.fill(255)
        py5.text_size(18)
        py5.text(f"Buffering frames: {len(frame_buffer)}/{buffer_size}", 20, py5.height/2)
        return

    # Take a vertical slice from current frame
    if slit_position < py5.width:
        slit_image[:, slit_position] = frame[:, slit_position]
        slit_position += 2  # Speed of scan

    # Display slit-scan image
    slit_rgb = cv2.cvtColor(slit_image, cv2.COLOR_BGR2RGB)
    img = py5.create_image_from_numpy(slit_rgb, 'RGB')
    py5.image(img, 0, 0)

    # Draw scan line
    py5.stroke(255, 0, 0)
    py5.stroke_weight(2)
    py5.line(slit_position, 0, slit_position, py5.height)

    # Info
    py5.fill(255)
    py5.text_size(12)
    py5.text(f"Scan position: {slit_position}/{py5.width}", 20, py5.height - 20)


def draw_pixel_sort():
    """Sort pixels based on brightness."""
    # Convert frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Sort pixels in each row based on brightness threshold
    sorted_frame = frame_rgb.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    threshold_low = 60
    threshold_high = 200

    for y in range(0, frame_rgb.shape[0], 2):  # Every other row for performance
        row = frame_rgb[y].copy()
        brightness = gray[y]

        # Find regions to sort (between thresholds)
        mask = (brightness > threshold_low) & (brightness < threshold_high)

        # Find contiguous regions
        start = None
        for x in range(len(mask)):
            if mask[x] and start is None:
                start = x
            elif not mask[x] and start is not None:
                # Sort this region by brightness
                region = row[start:x]
                region_brightness = brightness[start:x]
                sorted_indices = np.argsort(region_brightness)
                sorted_frame[y, start:x] = region[sorted_indices]
                start = None

    img = py5.create_image_from_numpy(sorted_frame, 'RGB')
    py5.image(img, 0, 0)


def draw_glitch():
    """Create glitch art effect."""
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    glitched = frame_rgb.copy()

    # Random horizontal displacement
    if py5.random(1) < 0.3:
        num_glitches = int(py5.random(3, 10))
        for _ in range(num_glitches):
            y_start = int(py5.random(glitched.shape[0] - 20))
            y_end = y_start + int(py5.random(5, 50))
            x_shift = int(py5.random(-50, 50))

            if x_shift > 0:
                glitched[y_start:y_end, x_shift:] = frame_rgb[y_start:y_end, :-x_shift]
            elif x_shift < 0:
                glitched[y_start:y_end, :x_shift] = frame_rgb[y_start:y_end, -x_shift:]

    # RGB channel separation
    if py5.random(1) < 0.2:
        shift = int(py5.random(5, 20))
        glitched[:, shift:, 0] = frame_rgb[:, :-shift, 0]  # Red shift
        glitched[:, :-shift, 2] = frame_rgb[:, shift:, 2]  # Blue shift

    # Random block corruption
    if py5.random(1) < 0.15:
        num_blocks = int(py5.random(2, 6))
        for _ in range(num_blocks):
            bx = int(py5.random(glitched.shape[1] - 100))
            by = int(py5.random(glitched.shape[0] - 100))
            bw = int(py5.random(20, 100))
            bh = int(py5.random(20, 100))

            # Copy from random location
            sx = int(py5.random(glitched.shape[1] - bw))
            sy = int(py5.random(glitched.shape[0] - bh))
            glitched[by:by+bh, bx:bx+bw] = frame_rgb[sy:sy+bh, sx:sx+bw]

    img = py5.create_image_from_numpy(glitched, 'RGB')
    py5.image(img, 0, 0)

    # Scanlines
    py5.stroke(0, 50)
    py5.stroke_weight(1)
    for y in range(0, py5.height, 4):
        py5.line(0, y, py5.width, y)


def draw_time_displacement():
    """Each row shows a different moment in time."""
    if len(frame_buffer) < buffer_size:
        py5.background(0)
        py5.fill(255)
        py5.text(f"Buffering: {len(frame_buffer)}/{buffer_size}", 20, py5.height/2)
        return

    # Create composite image
    composite = np.zeros_like(frame)

    for y in range(frame.shape[0]):
        # Map row to frame index
        frame_idx = int(py5.remap(y, 0, frame.shape[0], 0, len(frame_buffer) - 1))
        # Add wave distortion
        wave = int(py5.sin(y * 0.05 + py5.frame_count * 0.1) * 10)
        frame_idx = py5.constrain(frame_idx + wave, 0, len(frame_buffer) - 1)

        composite[y] = frame_buffer[frame_idx][y]

    composite_rgb = cv2.cvtColor(composite, cv2.COLOR_BGR2RGB)
    img = py5.create_image_from_numpy(composite_rgb, 'RGB')
    py5.image(img, 0, 0)


def draw_ui():
    """Draw mode indicator."""
    py5.fill(0, 180)
    py5.no_stroke()
    py5.rect(10, 10, 280, 55, 5)

    py5.fill(255)
    py5.text_size(14)
    py5.text(f"Mode {mode + 1}: {modes[mode]}", 20, 32)
    py5.text_size(11)
    py5.text(f"FPS: {int(py5.get_frame_rate())} | Buffer: {len(frame_buffer)}/{buffer_size}", 20, 55)


def key_pressed():
    global mode, slit_position, slit_image, motion_history

    if py5.key == '1':
        mode = 0
    elif py5.key == '2':
        mode = 1
        motion_history = np.zeros((720, 1280), dtype=np.float32)
    elif py5.key == '3':
        mode = 2
    elif py5.key == '4':
        mode = 3
    elif py5.key == '5':
        mode = 4
    elif py5.key == '6':
        mode = 5
    elif py5.key == 'r':
        # Reset current effect
        slit_position = 0
        slit_image = np.zeros((720, 1280, 3), dtype=np.uint8)
        motion_history = np.zeros((720, 1280), dtype=np.float32)
        print("Effect reset")
    elif py5.key == 's':
        filename = f"video_art_{py5.millis()}.png"
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
# 1. Optical Flow:
#    - Farneback algorithm for dense flow
#    - Visualize motion vectors
#    - Map flow to visual properties
#
# 2. Temporal Effects:
#    - Frame buffering for time manipulation
#    - Slit-scan photography simulation
#    - Time displacement mapping
#
# 3. Pixel Manipulation:
#    - Pixel sorting by brightness
#    - Glitch effects through data corruption
#    - Channel separation
#
# Extensions:
# - Add audio reactivity to effects
# - Implement background subtraction
# - Create video feedback loops
# - Build video synthesizer
# -------------------------------------------------

py5.run_sketch()
