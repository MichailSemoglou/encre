"""
Lesson 16: Export and Production
================================

A flowing noise-based artwork with layered waves
and organic particle trails.

Controls:
- 'p': Save PNG (screen size)
- 'h': Save high-res PNG
- 'v': Start video sequence export
- 'r': Randomize seed
- 's': Show current seed

Run this sketch in Processing with Python Mode enabled.
"""

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
        self.color_idx = int(random(5))
        self.speed = random(1, 3)
        self.life = random(100, 300)
        self.max_life = self.life

    def update(self, time_val):
        self.prev_x = self.x
        self.prev_y = self.y

        # Use noise to determine movement direction
        noise_scale = 0.003
        angle = noise(self.x * noise_scale, self.y * noise_scale, time_val * 0.5) * TWO_PI * 3

        self.x += cos(angle) * self.speed
        self.y += sin(angle) * self.speed

        self.life -= 1

        # Wrap around edges
        if self.x < 0:
            self.x = width
            self.prev_x = self.x
        if self.x > width:
            self.x = 0
            self.prev_x = self.x
        if self.y < 0:
            self.y = height
            self.prev_y = self.y
        if self.y > height:
            self.y = 0
            self.prev_y = self.y

    def is_dead(self):
        return self.life <= 0

    def draw_particle(self, pg=None):
        alpha = map(self.life, 0, self.max_life, 0, 180)
        col = palette[self.color_idx]

        r = red(col)
        g = green(col)
        b = blue(col)

        if pg:
            pg.stroke(r, g, b, alpha)
            pg.strokeWeight(1.5)
            pg.line(self.prev_x, self.prev_y, self.x, self.y)
        else:
            stroke(r, g, b, alpha)
            strokeWeight(1.5)
            line(self.prev_x, self.prev_y, self.x, self.y)


def setup():
    global palette, particles

    size(800, 600)

    # Deep, rich palette
    palette = [
        color(15, 32, 65),      # Deep navy
        color(45, 80, 120),     # Ocean blue
        color(90, 140, 160),    # Teal
        color(180, 120, 80),    # Warm amber
        color(220, 180, 140),   # Soft cream
    ]

    randomSeed(seed_value)
    noiseSeed(seed_value)

    # Initialize particles
    for _ in range(num_particles):
        particles.append(Particle(random(width), random(height)))

    background(8, 12, 20)

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
    fill(8, 12, 20, 15)
    noStroke()
    rect(0, 0, width, height)

    # Draw terrain-like noise waves in background
    drawNoiseWaves()

    # Update and draw particles
    for p in particles:
        p.update(t)
        p.draw_particle()

    # Replace dead particles
    particles = [p for p in particles if not p.is_dead()]
    while len(particles) < num_particles:
        particles.append(Particle(random(width), random(height)))

    # Handle sequence export
    if exporting_sequence:
        saveFrame("frames/frame-####.png")
        frame_count_export += 1

        # Progress indicator
        fill(0, 200)
        noStroke()
        rect(10, height - 40, 200, 30, 5)
        fill(255)
        textSize(12)
        text("Exporting: " + str(frame_count_export) + "/" + str(sequence_frames), 20, height - 20)

        if frame_count_export >= sequence_frames:
            stopSequenceExport()

    t += 0.008

    # UI
    if not exporting_sequence:
        drawUI()


def drawNoiseWaves():
    """Draw layered noise-based wave forms."""
    noFill()

    # Multiple wave layers
    for layer in range(3):
        layer_offset = layer * 0.5
        y_offset = layer * 60

        stroke(palette[layer + 1])
        strokeWeight(1)

        beginShape()
        for x in range(0, width + 10, 8):
            # Combine multiple noise octaves
            n1 = noise(x * 0.008 + layer_offset, t + layer_offset) * 100
            n2 = noise(x * 0.015 + layer_offset, t * 1.5 + layer_offset) * 50
            n3 = noise(x * 0.003 + layer_offset, t * 0.5 + layer_offset) * 150

            y = height * 0.4 + n1 + n2 + n3 + y_offset

            curveVertex(x, y)
        endShape()


def drawUI():
    """Draw minimal UI overlay."""
    fill(255, 180)
    noStroke()
    rect(10, 10, 180, 90, 5)

    fill(20)
    textSize(13)
    text("Export Options", 20, 30)

    textSize(10)
    fill(60)
    text("p: PNG  |  h: High-res", 20, 48)
    text("v: Video sequence", 20, 62)
    text("r: New seed", 20, 76)
    text("Seed: " + str(seed_value), 20, 90)


def saveHighRes():
    """Save high-resolution version of the artwork."""
    pg = createGraphics(export_width, export_height)

    scale_x = export_width / float(width)
    scale_y = export_height / float(height)

    # Reset seeds for reproducibility
    randomSeed(seed_value)
    noiseSeed(seed_value)

    pg.beginDraw()
    pg.background(8, 12, 20)

    # Build up the image over multiple iterations
    hi_res_particles = []
    for _ in range(int(num_particles * 1.5)):
        hi_res_particles.append({
            'x': random(export_width),
            'y': random(export_height),
            'prev_x': 0,
            'prev_y': 0,
            'color_idx': int(random(5)),
            'speed': random(1, 3) * scale_x,
            'life': random(100, 300),
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
        pg.noStroke()
        pg.rect(0, 0, export_width, export_height)

        # Draw waves
        pg.noFill()
        for layer in range(3):
            layer_offset = layer * 0.5
            y_offset = layer * 60 * scale_y

            col = palette[layer + 1]
            pg.stroke(red(col), green(col), blue(col))
            pg.strokeWeight(1 * scale_x)

            pg.beginShape()
            for x in range(0, export_width + 10, int(8 * scale_x)):
                n1 = noise(x * 0.008 / scale_x + layer_offset, sim_time + layer_offset) * 100 * scale_y
                n2 = noise(x * 0.015 / scale_x + layer_offset, sim_time * 1.5 + layer_offset) * 50 * scale_y
                n3 = noise(x * 0.003 / scale_x + layer_offset, sim_time * 0.5 + layer_offset) * 150 * scale_y

                y = export_height * 0.4 + n1 + n2 + n3 + y_offset
                pg.curveVertex(x, y)
            pg.endShape()

        # Update and draw particles
        for p in hi_res_particles:
            p['prev_x'] = p['x']
            p['prev_y'] = p['y']

            noise_scale = 0.003 / scale_x
            angle = noise(p['x'] * noise_scale, p['y'] * noise_scale, sim_time * 0.5) * TWO_PI * 3

            p['x'] += cos(angle) * p['speed']
            p['y'] += sin(angle) * p['speed']
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
                alpha = map(p['life'], 0, p['max_life'], 0, 180)
                col = palette[p['color_idx']]
                pg.stroke(red(col), green(col), blue(col), alpha)
                pg.strokeWeight(1.5 * scale_x)
                pg.line(p['prev_x'], p['prev_y'], p['x'], p['y'])

            # Respawn dead particles
            if p['life'] <= 0:
                p['x'] = random(export_width)
                p['y'] = random(export_height)
                p['prev_x'] = p['x']
                p['prev_y'] = p['y']
                p['life'] = random(100, 300)
                p['max_life'] = p['life']

        sim_time += 0.008

    pg.endDraw()

    filename = "export/highres_" + str(seed_value) + "_" + str(millis()) + ".png"
    pg.save(filename)
    print("Saved high-res: " + filename)
    print("Size: " + str(export_width) + " x " + str(export_height))


def startSequenceExport():
    """Start exporting frame sequence."""
    global exporting_sequence, frame_count_export, t, particles

    exporting_sequence = True
    frame_count_export = 0
    t = 0

    randomSeed(seed_value)
    noiseSeed(seed_value)

    # Reset particles
    particles = []
    for _ in range(num_particles):
        particles.append(Particle(random(width), random(height)))

    background(8, 12, 20)

    print("Starting sequence export...")
    print("Frames: " + str(sequence_frames))


def stopSequenceExport():
    """Stop sequence export."""
    global exporting_sequence

    exporting_sequence = False
    print("Sequence export complete!")
    print("Frames saved to frames/ folder")
    print("\nTo create video, use ffmpeg:")
    print("ffmpeg -framerate 30 -i frames/frame-%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4")


def keyPressed():
    global seed_value, particles, t

    if key == 'p':
        filename = "export/screen_" + str(seed_value) + "_" + str(millis()) + ".png"
        save(filename)
        print("Saved: " + filename)

    elif key == 'h':
        print("Generating high-res image (this may take a moment)...")
        saveHighRes()

    elif key == 'v':
        if not exporting_sequence:
            startSequenceExport()

    elif key == 'r':
        seed_value = int(random(100000))
        randomSeed(seed_value)
        noiseSeed(seed_value)
        t = 0

        # Reset particles with new seed
        particles = []
        for _ in range(num_particles):
            particles.append(Particle(random(width), random(height)))

        background(8, 12, 20)
        print("New seed: " + str(seed_value))

    elif key == 's':
        print("Current seed: " + str(seed_value))
