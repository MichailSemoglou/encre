# Advanced Workshop: Creative Coding with Computer Vision, ML & Physics

A 6-day intensive workshop exploring advanced techniques in generative art, combining computer vision, machine learning, text processing, physics simulation, and installation art.

## Prerequisites

```bash
pip install py5 opencv-python numpy requests
# Optional for Day 3:
pip install torch torchvision pillow
# Optional for Day 4 (hand tracking):
pip install mediapipe  # Requires Python 3.9-3.11
```

## Workshop Structure

### Day 1: Computer Vision & Face Detection
**File:** `day1_face_detection/face_detection_py5.py`

Learn to integrate OpenCV face detection with py5 for interactive art:
- Webcam capture and processing
- Haar cascade classifiers
- Face and eye detection
- 5 visualization modes (Mirror, Particle Aura, Face Mesh, Abstract Portrait, Emotion Colors)

### Day 2: Real-time Video Processing
**File:** `day2_video_processing/video_processing_py5.py`

Explore advanced video manipulation techniques:
- Optical flow calculation
- Motion detection and trails
- Slit-scan photography
- Pixel sorting
- Glitch effects
- Time displacement

### Day 3: Machine Learning Art
**File:** `day3_ml_art/ml_style_transfer_py5.py`

Create art using ML-inspired techniques:
- Edge-based artistic rendering
- Impressionist brushstroke simulation
- Pointillist effects (Seurat-style)
- Abstract expressionism
- Neural texture synthesis
- Deep dream-style visualization

### Day 4: Text & Gesture Art
**File:** `day4_text_gesture/text_and_gesture_py5.py`

Create interactive typography using Project Gutenberg texts:
- Fetch literary texts from Project Gutenberg
- Hand/gesture tracking (MediaPipe or motion detection)
- Finger trail typography
- Word magnet interactions
- Text rain effects
- Gesture-based writing
- Poetry flow fields

### Day 5: Multi-modal Installation Art
**File:** `day5_installation/installation_art_py5.py`

Combine all techniques for installation art:
- Presence Field (face-reactive ripples)
- Motion Painting (gesture-based art)
- Face Garden (organic growth)
- Sound Sculpture (audio visualization)
- Collective Memory (visitor traces)
- Full Installation (all layers combined)

### Day 6: Physics-Based Generative Art
**File:** `day6_physics_simulation/physics_simulation_py5.py`

Explore Newton's Laws of Motion for dynamic simulations:
- Newton's 1st Law (Inertia): Objects maintain their state of motion
- Newton's 2nd Law (F=ma): Force equals mass times acceleration
- Newton's 3rd Law (Action-Reaction): Equal and opposite forces
- Gravity wells and orbital mechanics
- Spring physics (Hooke's Law)
- Kinetic sculptures with spring networks

## Running the Workshops

Each day's lesson is self-contained. Run with:

```bash
python day1_face_detection/face_detection_py5.py
python day2_video_processing/video_processing_py5.py
python day3_ml_art/ml_style_transfer_py5.py
python day4_text_gesture/text_and_gesture_py5.py
python day5_installation/installation_art_py5.py
python day6_physics_simulation/physics_simulation_py5.py
```

## Common Controls

| Key | Action |
|-----|--------|
| 1-6 | Switch visualization modes |
| s | Save screenshot |
| q | Quit |
| Mouse | Interactive control |

## Hardware Requirements

- Webcam (required for all days)
- 8GB+ RAM recommended

## Notes

These workshops use py5 only (no .pyde versions) because they require external libraries (OpenCV, NumPy, requests) that are not available in Processing's Python Mode.

Day 4 works best with MediaPipe for hand tracking, but falls back to motion detection if MediaPipe isn't available (e.g., on Python 3.13+).

For the complete Encre course (17 lessons), see the `lessons/` directory which includes both `.pyde` and `_py5.py` versions.
