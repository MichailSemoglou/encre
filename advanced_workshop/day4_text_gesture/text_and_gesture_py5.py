"""
Advanced Workshop - Day 4: Text & Gesture Art
=============================================

Create interactive typography using texts from
Project Gutenberg, controlled by hand gestures
detected through your webcam using MediaPipe.

Prerequisites:
    pip install py5 opencv-python numpy requests mediapipe

Learning Objectives:
- Fetch and process literary texts
- Implement hand tracking with MediaPipe
- Create gesture-reactive typography
- Build text-based generative systems

Run with: python text_and_gesture_py5.py
"""

import py5
import cv2
import numpy as np
import requests
import re
from collections import deque
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import urllib.request
import os

# Camera
cap = None
frame = None

# MediaPipe Hands (Tasks API)
hand_detector = None
detection_result = None

# Hand tracking results
finger_positions = []  # List of (x, y) for detected fingertips
palm_center = None
hand_detected = False
hand_landmarks = None  # Store full landmarks for advanced use

# Model path
MODEL_PATH = None

# Text data
texts = {}
current_text = "alice"
words = []
current_word_index = 0

# Text particles
text_particles = []

# Floating words
floating_words = []

# Visualization mode
mode = 0
modes = [
    "Finger Trail",
    "Word Magnet",
    "Text Rain",
    "Gesture Writing",
    "Poetry Field",
    "Hand Typography"
]

# Animation
t = 0

# Palette
palette = []

# Trail history
finger_trails = [deque(maxlen=50) for _ in range(5)]  # One trail per finger

# Detection confidence threshold
min_detection_confidence = 0.5
min_tracking_confidence = 0.5


def download_model():
    """Download the hand landmarker model if not present."""
    global MODEL_PATH
    
    # Store model in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(script_dir, "hand_landmarker.task")
    
    if not os.path.exists(MODEL_PATH):
        print("Downloading hand landmarker model...")
        url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
        urllib.request.urlretrieve(url, MODEL_PATH)
        print("Model downloaded successfully!")
    return MODEL_PATH


def setup():
    global cap, palette, texts, words, hand_detector

    py5.size(1280, 720)

    # Initialize camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Download model if needed
    model_path = download_model()

    # Initialize MediaPipe Hand Landmarker (Tasks API)
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.IMAGE,
        num_hands=2,
        min_hand_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence
    )
    hand_detector = vision.HandLandmarker.create_from_options(options)

    # Initialize palette
    palette = [
        py5.color(41, 65, 114),    # Deep blue
        py5.color(193, 84, 55),    # Terracotta
        py5.color(85, 130, 89),    # Forest green
        py5.color(156, 136, 103),  # Warm gray
        py5.color(180, 60, 60),    # Burgundy
    ]

    # Load texts
    load_texts()
    words = texts[current_text].split()

    print("=" * 60)
    print("Advanced Workshop Day 4: Text & Gesture Art")
    print("=" * 60)
    print("\nUsing MediaPipe for robust hand detection")
    print("\nControls:")
    print("  1-6: Switch visualization modes")
    print("  t: Cycle through texts")
    print("  s: Save screenshot")
    print("  c: Clear particles")
    print("  q: Quit")
    print("\nModes:")
    for i, m in enumerate(modes):
        print(f"  {i+1}: {m}")


def load_texts():
    """Load sample texts from Project Gutenberg or use fallbacks."""
    global texts

    # Project Gutenberg URLs (plain text versions)
    gutenberg_texts = {
        "alice": "https://www.gutenberg.org/cache/epub/11/pg11.txt",
        "pride": "https://www.gutenberg.org/cache/epub/1342/pg1342.txt",
        "frankenstein": "https://www.gutenberg.org/cache/epub/84/pg84.txt",
    }

    # Fallback excerpts if download fails
    fallback_texts = {
        "alice": """Alice was beginning to get very tired of sitting by her sister on the bank
        and of having nothing to do once or twice she had peeped into the book her sister was reading
        but it had no pictures or conversations in it and what is the use of a book thought Alice
        without pictures or conversations So she was considering in her own mind as well as she could
        for the hot day made her feel very sleepy and stupid whether the pleasure of making a daisy chain
        would be worth the trouble of getting up and picking the daisies when suddenly a White Rabbit
        with pink eyes ran close by her There was nothing so very remarkable in that nor did Alice think
        it so very much out of the way to hear the Rabbit say to itself Oh dear Oh dear I shall be late
        but when the Rabbit actually took a watch out of its waistcoat pocket and looked at it and then
        hurried on Alice started to her feet for it flashed across her mind that she had never before
        seen a rabbit with either a waistcoat pocket or a watch to take out of it and burning with curiosity
        she ran across the field after it and fortunately was just in time to see it pop down a large
        rabbit hole under the hedge In another moment down went Alice after it never once considering
        how in the world she was to get out again""",

        "pride": """It is a truth universally acknowledged that a single man in possession of a good fortune
        must be in want of a wife However little known the feelings or views of such a man may be on his
        first entering a neighbourhood this truth is so well fixed in the minds of the surrounding families
        that he is considered as the rightful property of some one or other of their daughters My dear
        Mr Bennet said his lady to him one day have you heard that Netherfield Park is let at last
        Mr Bennet replied that he had not But it is returned she for Mrs Long has just been here and
        she told me all about it Mr Bennet made no answer Do not you want to know who has taken it
        cried his wife impatiently You want to tell me and I have no objection to hearing it This was
        invitation enough Why my dear you must know Mrs Long says that Netherfield is taken by a young
        man of large fortune from the north of England that he came down on Monday in a chaise and four
        to see the place and was so much delighted with it that he agreed with Mr Morris immediately""",

        "frankenstein": """I am by birth a Genevese and my family is one of the most distinguished of that
        republic My ancestors had been for many years counsellors and syndics and my father had filled
        several public situations with honour and reputation He was respected by all who knew him for
        his integrity and indefatigable attention to public business He passed his younger days perpetually
        occupied by the affairs of his country a variety of circumstances had prevented his marrying early
        nor was it until the decline of life that he became a husband and the father of a family As the
        circumstances of his marriage illustrate his character I cannot refrain from relating them One of
        his most intimate friends was a merchant who from a flourishing state fell through numerous
        mischances into poverty This man whose name was Beaufort was of a proud and unbending disposition
        and could not bear to live in poverty and oblivion in the same country where he had formerly been
        distinguished for his rank and magnificence Having paid his debts therefore in the most honourable
        manner he retreated with his daughter to the town of Lucerne where he lived unknown and in wretchedness"""
    }

    print("\nLoading texts...")

    for name, url in gutenberg_texts.items():
        try:
            print(f"  Fetching {name}...", end=" ")
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                text = response.text
                start_markers = ["*** START OF", "***START OF"]
                end_markers = ["*** END OF", "***END OF"]

                start_idx = 0
                for marker in start_markers:
                    if marker in text:
                        start_idx = text.find(marker)
                        start_idx = text.find("\n", start_idx) + 1
                        break

                end_idx = len(text)
                for marker in end_markers:
                    if marker in text:
                        end_idx = text.find(marker)
                        break

                text = text[start_idx:end_idx]
                text = re.sub(r'[^\w\s]', '', text)
                text = re.sub(r'\s+', ' ', text)
                text = text[:5000]

                texts[name] = text.strip()
                print("OK")
            else:
                raise Exception("Download failed")
        except Exception as e:
            print(f"using fallback ({e})")
            texts[name] = fallback_texts[name]

    print(f"  Loaded {len(texts)} texts")


def draw():
    global t, frame

    t += 0.02

    # Capture frame
    ret, frame = cap.read()
    if not ret:
        py5.background(30)
        py5.fill(255)
        py5.text("No webcam detected", py5.width/2 - 80, py5.height/2)
        return

    frame = cv2.flip(frame, 1)

    # Process hand tracking
    process_hand_opencv()

    # Draw based on mode
    if mode == 0:
        draw_finger_trail()
    elif mode == 1:
        draw_word_magnet()
    elif mode == 2:
        draw_text_rain()
    elif mode == 3:
        draw_gesture_writing()
    elif mode == 4:
        draw_poetry_field()
    elif mode == 5:
        draw_hand_typography()

    # Draw UI
    draw_ui()


def process_hand_opencv():
    """Detect hand using MediaPipe Hand Landmarker (Tasks API)."""
    global finger_positions, palm_center, hand_detected, hand_landmarks

    finger_positions = []
    palm_center = None
    hand_detected = False
    hand_landmarks = None

    # Convert BGR to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Create MediaPipe Image
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Process the frame
    results = hand_detector.detect(mp_image)

    if results.hand_landmarks and len(results.hand_landmarks) > 0:
        hand_detected = True

        # Get the first detected hand
        hand_lms = results.hand_landmarks[0]
        hand_landmarks = hand_lms

        # Scale factors
        scale_x = py5.width
        scale_y = py5.height

        # MediaPipe landmark indices for fingertips
        # THUMB_TIP=4, INDEX_TIP=8, MIDDLE_TIP=12, RING_TIP=16, PINKY_TIP=20
        fingertip_indices = [4, 8, 12, 16, 20]

        for idx in fingertip_indices:
            lm = hand_lms[idx]
            # MediaPipe returns normalized coordinates (0-1)
            x = lm.x * scale_x
            y = lm.y * scale_y
            finger_positions.append((x, y))

        # Calculate palm center using wrist and middle finger MCP
        # WRIST=0, MIDDLE_FINGER_MCP=9
        wrist = hand_lms[0]
        middle_mcp = hand_lms[9]
        palm_x = ((wrist.x + middle_mcp.x) / 2) * scale_x
        palm_y = ((wrist.y + middle_mcp.y) / 2) * scale_y
        palm_center = (palm_x, palm_y)

    # Update finger trails
    for i, trail in enumerate(finger_trails):
        if i < len(finger_positions):
            trail.append(finger_positions[i])
        elif palm_center and i == 0:
            # If no fingertips but palm detected, use palm
            trail.append(palm_center)


def draw_finger_trail():
    """Words follow finger trails."""
    py5.background(250, 248, 245)

    # Draw trails with words
    for trail_idx, trail in enumerate(finger_trails):
        if len(trail) < 2:
            continue

        col = palette[trail_idx % len(palette)]

        for i, (x, y) in enumerate(trail):
            if i < len(words):
                word = words[(current_word_index + i) % len(words)]

                size = py5.remap(i, 0, len(trail), 8, 24)
                alpha = py5.remap(i, 0, len(trail), 50, 255)

                py5.fill(py5.red(col), py5.green(col), py5.blue(col), alpha)
                py5.text_size(size)
                py5.text(word, x, y)

    # Current fingertip indicators
    py5.fill(255, 100, 100, 200)
    py5.no_stroke()
    for (x, y) in finger_positions:
        py5.ellipse(x, y, 15, 15)

    # Show palm center
    if palm_center:
        py5.fill(100, 100, 255, 150)
        py5.ellipse(palm_center[0], palm_center[1], 25, 25)


def draw_word_magnet():
    """Words are attracted to or repelled by hand."""
    global floating_words

    py5.background(30, 30, 40)

    # Initialize floating words if needed
    if len(floating_words) < 100:
        for _ in range(100 - len(floating_words)):
            floating_words.append({
                'word': words[int(py5.random(len(words)))],
                'x': py5.random(py5.width),
                'y': py5.random(py5.height),
                'vx': 0,
                'vy': 0,
                'size': py5.random(12, 28),
                'col': palette[int(py5.random(len(palette)))]
            })

    # Determine gesture - spread fingers = repel, closed = attract
    fingers_spread = len(finger_positions) > 3

    # Update and draw words
    for fw in floating_words:
        # Apply forces from detected points
        force_points = finger_positions if finger_positions else ([palm_center] if palm_center else [])

        for fp in force_points:
            if fp is None:
                continue
            dx = fw['x'] - fp[0]
            dy = fw['y'] - fp[1]
            dist = max(10, np.sqrt(dx*dx + dy*dy))

            # Attract if closed, repel if spread
            if fingers_spread:
                force = 300 / (dist * dist)
            else:
                force = -200 / (dist * dist)

            fw['vx'] += (dx / dist) * force
            fw['vy'] += (dy / dist) * force

        fw['vx'] *= 0.95
        fw['vy'] *= 0.95

        fw['x'] += fw['vx']
        fw['y'] += fw['vy']

        if fw['x'] < 0: fw['x'] = py5.width
        if fw['x'] > py5.width: fw['x'] = 0
        if fw['y'] < 0: fw['y'] = py5.height
        if fw['y'] > py5.height: fw['y'] = 0

        col = fw['col']
        py5.fill(py5.red(col), py5.green(col), py5.blue(col))
        py5.text_size(fw['size'])
        py5.text(fw['word'], fw['x'], fw['y'])

    # Draw hand indicator
    if palm_center:
        py5.no_fill()
        py5.stroke(255, 100)
        py5.stroke_weight(2)
        size = 80 if fingers_spread else 30
        py5.ellipse(palm_center[0], palm_center[1], size, size)


def draw_text_rain():
    """Words rain down, blocked by hand."""
    global text_particles

    py5.background(20, 25, 35)

    # Spawn new particles
    if py5.random(1) < 0.3:
        text_particles.append({
            'word': words[int(py5.random(len(words)))],
            'x': py5.random(py5.width),
            'y': -20,
            'vy': py5.random(2, 5),
            'size': py5.random(10, 20),
            'col': palette[int(py5.random(len(palette)))]
        })

    # Collision points
    collision_points = finger_positions + ([palm_center] if palm_center else [])

    # Update and draw
    for i in range(len(text_particles) - 1, -1, -1):
        p = text_particles[i]

        # Check collision with hand
        blocked = False
        for cp in collision_points:
            if cp and abs(p['x'] - cp[0]) < 60 and abs(p['y'] - cp[1]) < 60:
                p['x'] += (p['x'] - cp[0]) * 0.3
                p['vy'] *= 0.5
                blocked = True

        if not blocked:
            p['y'] += p['vy']
            p['vy'] += 0.1

        col = p['col']
        alpha = py5.remap(p['y'], 0, py5.height, 255, 100)
        py5.fill(py5.red(col), py5.green(col), py5.blue(col), alpha)
        py5.text_size(p['size'])
        py5.text(p['word'], p['x'], p['y'])

        if p['y'] > py5.height + 50:
            text_particles.pop(i)

    while len(text_particles) > 200:
        text_particles.pop(0)

    # Draw finger positions
    py5.fill(255, 200)
    py5.no_stroke()
    for cp in collision_points:
        if cp:
            py5.ellipse(cp[0], cp[1], 25, 25)


def draw_gesture_writing():
    """Draw with words following gesture path."""
    py5.background(250, 248, 245)

    # Draw all accumulated text particles
    for p in text_particles:
        col = p['col']
        alpha = p.get('alpha', 255)
        py5.fill(py5.red(col), py5.green(col), py5.blue(col), alpha)
        py5.text_size(p['size'])
        py5.push_matrix()
        py5.translate(p['x'], p['y'])
        py5.rotate(p.get('angle', 0))
        py5.text(p['word'], 0, 0)
        py5.pop_matrix()

        p['alpha'] = p.get('alpha', 255) - 0.3
        if p['alpha'] < 0:
            p['alpha'] = 0

    # Add new words at finger/palm positions
    active_points = finger_positions if finger_positions else ([palm_center] if palm_center else [])

    if len(active_points) > 0 and py5.frame_count % 3 == 0:
        for i, (x, y) in enumerate(active_points[:3]):
            # Check if moved enough
            trail_idx = min(i, len(finger_trails) - 1)
            if len(finger_trails[trail_idx]) >= 2:
                prev = finger_trails[trail_idx][-2]
                dx = x - prev[0]
                dy = y - prev[1]
                dist = np.sqrt(dx*dx + dy*dy)

                if dist > 10:
                    angle = np.arctan2(dy, dx)
                    text_particles.append({
                        'word': words[current_word_index % len(words)],
                        'x': x,
                        'y': y,
                        'size': py5.remap(dist, 0, 50, 10, 30),
                        'col': palette[i % len(palette)],
                        'angle': angle,
                        'alpha': 255
                    })
                    advance_word()

    while len(text_particles) > 500:
        text_particles.pop(0)

    py5.fill(100)
    py5.text_size(14)
    py5.text("Move your hand to write with words", 20, py5.height - 20)


def draw_poetry_field():
    """Words arranged in a flow field, disturbed by hand."""
    py5.background(245, 242, 235)

    global floating_words
    if len(floating_words) < 150:
        floating_words = []
        cols = 15
        rows = 10
        for i in range(cols):
            for j in range(rows):
                floating_words.append({
                    'word': words[(i * rows + j) % len(words)],
                    'base_x': (i + 0.5) * (py5.width / cols),
                    'base_y': (j + 0.5) * (py5.height / rows),
                    'x': (i + 0.5) * (py5.width / cols),
                    'y': (j + 0.5) * (py5.height / rows),
                    'size': 14,
                    'col': palette[(i + j) % len(palette)]
                })

    # Force points
    force_points = finger_positions + ([palm_center] if palm_center else [])

    for fw in floating_words:
        noise_val = py5.noise(fw['base_x'] * 0.003, fw['base_y'] * 0.003, t * 0.5)
        angle = noise_val * py5.TWO_PI * 2

        flow_x = np.cos(angle) * 20
        flow_y = np.sin(angle) * 20

        hand_x, hand_y = 0, 0
        for fp in force_points:
            if fp is None:
                continue
            dx = fw['base_x'] - fp[0]
            dy = fw['base_y'] - fp[1]
            dist = max(20, np.sqrt(dx*dx + dy*dy))
            force = 3000 / (dist * dist)
            hand_x += (dx / dist) * force
            hand_y += (dy / dist) * force

        target_x = fw['base_x'] + flow_x + hand_x
        target_y = fw['base_y'] + flow_y + hand_y

        fw['x'] = py5.lerp(fw['x'], target_x, 0.1)
        fw['y'] = py5.lerp(fw['y'], target_y, 0.1)

        col = fw['col']
        py5.fill(py5.red(col), py5.green(col), py5.blue(col))
        py5.text_size(fw['size'])
        py5.text_align(py5.CENTER)
        py5.text(fw['word'], fw['x'], fw['y'])

    py5.text_align(py5.LEFT)


def draw_hand_typography():
    """Large typography that reacts to hand shape."""
    py5.background(20, 20, 30)

    sentence_words = words[current_word_index:current_word_index + 8]
    sentence = " ".join(sentence_words)

    base_y = py5.height / 2
    char_x = 100
    char_idx = 0

    # All interaction points
    interact_points = finger_positions + ([palm_center] if palm_center else [])

    for char in sentence:
        if char == ' ':
            char_x += 30
            continue

        min_dist = float('inf')
        for fp in interact_points:
            if fp:
                dist = np.sqrt((char_x - fp[0])**2 + (base_y - fp[1])**2)
                if dist < min_dist:
                    min_dist = dist

        if min_dist < 200:
            size_mult = py5.remap(min_dist, 0, 200, 3, 1)
            y_offset = py5.remap(min_dist, 0, 200, -50, 0)
            alpha = 255
        else:
            size_mult = 1
            y_offset = 0
            alpha = 150

        col = palette[char_idx % len(palette)]

        py5.fill(py5.red(col), py5.green(col), py5.blue(col), alpha)
        py5.text_size(48 * size_mult)
        py5.text(char, char_x, base_y + y_offset)

        char_x += 35 * size_mult
        char_idx += 1

        if char_x > py5.width - 100:
            break

    # Draw hand outline
    if palm_center:
        py5.no_fill()
        py5.stroke(255, 50)
        py5.stroke_weight(1)
        py5.ellipse(palm_center[0], palm_center[1], 100, 100)


def advance_word():
    global current_word_index
    current_word_index = (current_word_index + 1) % len(words)


def draw_ui():
    """Draw info panel."""
    py5.fill(0, 180)
    py5.no_stroke()
    py5.rect(10, 10, 350, 90, 5)

    py5.fill(255)
    py5.text_size(14)
    py5.text_align(py5.LEFT)
    py5.text(f"Mode: {modes[mode]}", 20, 32)

    py5.text_size(11)
    py5.text(f"Text: {current_text} | Words: {len(words)}", 20, 55)
    hand_status = f"Detected ({len(finger_positions)} fingertips)" if hand_detected else "Not detected"
    py5.text(f"Hand: {hand_status}", 20, 70)
    py5.text("MediaPipe Hand Tracking | Keys: 1-6 modes, t = text, s = ave, c = clear", 20, 85)


def key_pressed():
    global mode, current_text, words, current_word_index
    global text_particles, floating_words

    if py5.key in '123456':
        mode = int(py5.key) - 1
        text_particles = []
        floating_words = []
    elif py5.key == 't':
        text_names = list(texts.keys())
        idx = text_names.index(current_text)
        current_text = text_names[(idx + 1) % len(text_names)]
        words = texts[current_text].split()
        current_word_index = 0
        text_particles = []
        floating_words = []
        print(f"Switched to: {current_text}")
    elif py5.key == 'c':
        text_particles = []
        floating_words = []
        for trail in finger_trails:
            trail.clear()
    elif py5.key == 's':
        filename = f"text_gesture_{modes[mode].replace(' ', '_')}_{py5.millis()}.png"
        py5.save(filename)
        print(f"Saved: {filename}")
    elif py5.key == 'q':
        cleanup()
        py5.exit_sketch()


def cleanup():
    global cap, hand_detector
    if cap is not None:
        cap.release()
    if hand_detector is not None:
        hand_detector.close()


import atexit
atexit.register(cleanup)


# -------------------------------------------------
# Hand Detection with MediaPipe Tasks API:
#
# MediaPipe Hand Landmarker provides robust hand tracking
# using machine learning models. Key features:
#
# 1. 21 Hand Landmarks:
#    - Wrist (0)
#    - Thumb: CMC(1), MCP(2), IP(3), TIP(4)
#    - Index: MCP(5), PIP(6), DIP(7), TIP(8)
#    - Middle: MCP(9), PIP(10), DIP(11), TIP(12)
#    - Ring: MCP(13), PIP(14), DIP(15), TIP(16)
#    - Pinky: MCP(17), PIP(18), DIP(19), TIP(20)
#
# 2. Benefits over skin detection:
#    - Works in varying lighting conditions
#    - Robust to different skin tones
#    - Provides precise fingertip positions
#    - Detects up to 2 hands simultaneously
#
# 3. Performance:
#    - Runs efficiently on CPU
#    - ~30 FPS on modern hardware
#
# 4. Tasks API (new):
#    - Modern MediaPipe API
#    - Downloads model automatically
#    - More flexible configuration
# -------------------------------------------------

py5.run_sketch()
