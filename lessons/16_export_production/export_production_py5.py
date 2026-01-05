"""
Lesson 16: Export and Production (py5 version)
==============================================

A flowing noise-based artwork with layered waves
and organic particle trails.

Controls:
- 'p': Save PNG (screen size)
- 'h': Save high-res PNG
- 'v': Start video sequence export
- 'r': Randomize seed
- 's': Show current seed

Run with: python export_production_py5.py
"""

import py5
from pathlib import Path

# Export settings
export_width = 1920
export_height = 1080
frame_count_export = 0
exporting_sequence = False
sequence_frames = 120

# Artwork parameters
t = 0
seed_value = 42

# Color palette - deep ocean tones
palette = []

# Particle system
particles = []
num_particles = 200


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.color_idx = int(py5.random(5))
        self.speed = py5.random(1, 3)
        self.life = py5.random(100, 300)
        self.max_life = self.life

    def update(self, time_val):
        self.prev_x = self.x
        self.prev_y = self.y

        # Use noise to determine movement direction
        noise_scale = 0.003
        angle = py5.noise(self.x * noise_scale, self.y * noise_scale, time_val * 0.5) * py5.TWO_PI * 3

        self.x += py5.cos(angle) * self.speed
        self.y += py5.sin(angle) * self.speed

        self.life -= 1

        # Wrap around edges
        if self.x < 0:
            self.x = py5.width
            self.prev_x = self.x
        if self.x > py5.width:
            self.x = 0
            self.prev_x = self.x
        if self.y < 0:
            self.y = py5.height
            self.prev_y = self.y
        if self.y > py5.height:
            self.y = 0
            self.prev_y = self.y

    def is_dead(self):
        return self.life <= 0

    def draw(self, pg=None):
        target = pg if pg else py5

        alpha = py5.remap(self.life, 0, self.max_life, 0, 180)
        col = palette[self.color_idx]

        r = py5.red(col)
        g = py5.green(col)
        b = py5.blue(col)

        target.stroke(r, g, b, alpha)
        target.stroke_weight(1.5)
        target.line(self.prev_x, self.prev_y, self.x, self.y)


def setup():
    global palette, particles

    py5.size(800, 600)

    # Deep, rich palette
    palette = [
        py5.color(15, 32, 65),      # Deep navy
        py5.color(45, 80, 120),     # Ocean blue
        py5.color(90, 140, 160),    # Teal
        py5.color(180, 120, 80),    # Warm amber
        py5.color(220, 180, 140),   # Soft cream
    ]

    py5.random_seed(seed_value)
    py5.noise_seed(seed_value)

    # Initialize particles
    for _ in range(num_particles):
        particles.append(Particle(py5.random(py5.width), py5.random(py5.height)))

    # Create export folders
    Path("export").mkdir(exist_ok=True)
    Path("frames").mkdir(exist_ok=True)

    py5.background(8, 12, 20)

    print("Lesson 16: Export and Production")
    print("\nControls:")
    print("  Press 'p' to save PNG (screen size)")
    print("  Press 'h' to save high-res PNG")
    print("  Press 'v' to start video sequence")
    print("  Press 'r' to randomize seed")
    print("  Press 's' to show current seed")


def draw():
    global t, frame_count_export, particles

    # Semi-transparent overlay for trail effect
    py5.fill(8, 12, 20, 15)
    py5.no_stroke()
    py5.rect(0, 0, py5.width, py5.height)

    # Draw terrain-like noise waves in background
    draw_noise_waves()

    # Update and draw particles
    for p in particles:
        p.update(t)
        p.draw()

    # Replace dead particles
    particles = [p for p in particles if not p.is_dead()]
    while len(particles) < num_particles:
        particles.append(Particle(py5.random(py5.width), py5.random(py5.height)))

    # Handle sequence export
    if exporting_sequence:
        py5.save_frame(f"frames/frame-{py5.frame_count:04d}.png")
        frame_count_export += 1

        # Progress indicator
        py5.fill(0, 200)
        py5.no_stroke()
        py5.rect(10, py5.height - 40, 200, 30, 5)
        py5.fill(255)
        py5.text_size(12)
        py5.text(f"Exporting: {frame_count_export}/{sequence_frames}", 20, py5.height - 20)

        if frame_count_export >= sequence_frames:
            stop_sequence_export()

    t += 0.008

    # UI
    if not exporting_sequence:
        draw_ui()


def draw_noise_waves():
    """Draw layered noise-based wave forms."""
    py5.no_fill()

    # Multiple wave layers
    for layer in range(3):
        layer_offset = layer * 0.5
        y_offset = layer * 60

        py5.stroke(palette[layer + 1])
        py5.stroke_weight(1)

        py5.begin_shape()
        for x in range(0, py5.width + 10, 8):
            # Combine multiple noise octaves
            n1 = py5.noise(x * 0.008 + layer_offset, t + layer_offset) * 100
            n2 = py5.noise(x * 0.015 + layer_offset, t * 1.5 + layer_offset) * 50
            n3 = py5.noise(x * 0.003 + layer_offset, t * 0.5 + layer_offset) * 150

            y = py5.height * 0.4 + n1 + n2 + n3 + y_offset

            py5.curve_vertex(x, y)
        py5.end_shape()


def draw_ui():
    """Draw minimal UI overlay."""
    py5.fill(255, 180)
    py5.no_stroke()
    py5.rect(10, 10, 180, 90, 5)

    py5.fill(20)
    py5.text_size(13)
    py5.text("Export Options", 20, 30)

    py5.text_size(10)
    py5.fill(60)
    py5.text("p: PNG  |  h: High-res", 20, 48)
    py5.text("v: Video sequence", 20, 62)
    py5.text("r: New seed", 20, 76)
    py5.text(f"Seed: {seed_value}", 20, 90)


def save_high_res():
    """Save high-resolution version of the artwork."""
    global particles

    pg = py5.create_graphics(export_width, export_height)

    scale_x = export_width / float(py5.width)
    scale_y = export_height / float(py5.height)

    # Reset seeds for reproducibility
    py5.random_seed(seed_value)
    py5.noise_seed(seed_value)

    pg.begin_draw()
    pg.background(8, 12, 20)

    # Build up the image over multiple iterations
    hi_res_particles = []
    for _ in range(int(num_particles * 1.5)):
        hi_res_particles.append({
            'x': py5.random(export_width),
            'y': py5.random(export_height),
            'prev_x': 0,
            'prev_y': 0,
            'color_idx': int(py5.random(5)),
            'speed': py5.random(1, 3) * scale_x,
            'life': py5.random(100, 300),
            'max_life': 0
        })
        hi_res_particles[-1]['prev_x'] = hi_res_particles[-1]['x']
        hi_res_particles[-1]['prev_y'] = hi_res_particles[-1]['y']
        hi_res_particles[-1]['max_life'] = hi_res_particles[-1]['life']

    # Simulate many frames
    sim_time = 0
    for frame in range(400):
        # Fade effect
        pg.fill(8, 12, 20, 12)
        pg.no_stroke()
        pg.rect(0, 0, export_width, export_height)

        # Draw waves
        pg.no_fill()
        for layer in range(3):
            layer_offset = layer * 0.5
            y_offset = layer * 60 * scale_y

            col = palette[layer + 1]
            pg.stroke(py5.red(col), py5.green(col), py5.blue(col))
            pg.stroke_weight(1 * scale_x)

            pg.begin_shape()
            for x in range(0, export_width + 10, int(8 * scale_x)):
                n1 = py5.noise(x * 0.008 / scale_x + layer_offset, sim_time + layer_offset) * 100 * scale_y
                n2 = py5.noise(x * 0.015 / scale_x + layer_offset, sim_time * 1.5 + layer_offset) * 50 * scale_y
                n3 = py5.noise(x * 0.003 / scale_x + layer_offset, sim_time * 0.5 + layer_offset) * 150 * scale_y

                y = export_height * 0.4 + n1 + n2 + n3 + y_offset
                pg.curve_vertex(x, y)
            pg.end_shape()

        # Update and draw particles
        for p in hi_res_particles:
            p['prev_x'] = p['x']
            p['prev_y'] = p['y']

            noise_scale = 0.003 / scale_x
            angle = py5.noise(p['x'] * noise_scale, p['y'] * noise_scale, sim_time * 0.5) * py5.TWO_PI * 3

            p['x'] += py5.cos(angle) * p['speed']
            p['y'] += py5.sin(angle) * p['speed']
            p['life'] -= 1

            # Wrap
            if p['x'] < 0:
                p['x'] = export_width
                p['prev_x'] = p['x']
            if p['x'] > export_width:
                p['x'] = 0
                p['prev_x'] = p['x']
            if p['y'] < 0:
                p['y'] = export_height
                p['prev_y'] = p['y']
            if p['y'] > export_height:
                p['y'] = 0
                p['prev_y'] = p['y']

            # Draw
            if p['life'] > 0:
                alpha = py5.remap(p['life'], 0, p['max_life'], 0, 180)
                col = palette[p['color_idx']]
                pg.stroke(py5.red(col), py5.green(col), py5.blue(col), alpha)
                pg.stroke_weight(1.5 * scale_x)
                pg.line(p['prev_x'], p['prev_y'], p['x'], p['y'])

            # Respawn dead particles
            if p['life'] <= 0:
                p['x'] = py5.random(export_width)
                p['y'] = py5.random(export_height)
                p['prev_x'] = p['x']
                p['prev_y'] = p['y']
                p['life'] = py5.random(100, 300)
                p['max_life'] = p['life']

        sim_time += 0.008

    pg.end_draw()

    filename = f"export/highres_{seed_value}_{py5.millis()}.png"
    pg.save(filename)
    print(f"Saved high-res: {filename}")
    print(f"Size: {export_width} x {export_height}")


def start_sequence_export():
    """Start exporting frame sequence."""
    global exporting_sequence, frame_count_export, t, particles

    exporting_sequence = True
    frame_count_export = 0
    t = 0

    py5.random_seed(seed_value)
    py5.noise_seed(seed_value)

    # Reset particles
    particles = []
    for _ in range(num_particles):
        particles.append(Particle(py5.random(py5.width), py5.random(py5.height)))

    py5.background(8, 12, 20)

    print("Starting sequence export...")
    print(f"Frames: {sequence_frames}")


def stop_sequence_export():
    """Stop sequence export."""
    global exporting_sequence

    exporting_sequence = False
    print("Sequence export complete!")
    print("Frames saved to frames/ folder")
    print("\nTo create video, use ffmpeg:")
    print("ffmpeg -framerate 30 -i frames/frame-%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4")


def key_pressed():
    global seed_value, particles, t

    if py5.key == 'p':
        filename = f"export/screen_{seed_value}_{py5.millis()}.png"
        py5.save(filename)
        print(f"Saved: {filename}")

    elif py5.key == 'h':
        print("Generating high-res image (this may take a moment)...")
        save_high_res()

    elif py5.key == 'v':
        if not exporting_sequence:
            start_sequence_export()

    elif py5.key == 'r':
        seed_value = int(py5.random(100000))
        py5.random_seed(seed_value)
        py5.noise_seed(seed_value)
        t = 0

        # Reset particles with new seed
        particles = []
        for _ in range(num_particles):
            particles.append(Particle(py5.random(py5.width), py5.random(py5.height)))

        py5.background(8, 12, 20)
        print(f"New seed: {seed_value}")

    elif py5.key == 's':
        print(f"Current seed: {seed_value}")


py5.run_sketch()
