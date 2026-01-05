# Encre: Detailed Curriculum

## Module 1: Foundations (Lessons 1-4)

---

### Lesson 01: Hello Processing.py

**Duration**: 2-3 hours

**Learning Objectives**:
- Install and configure Processing with Python Mode
- Understand the Processing coordinate system
- Draw basic shapes (point, line, rect, ellipse, triangle)
- Apply colors using `fill()`, `stroke()`, `background()`
- Understand the `setup()` and `draw()` lifecycle

**Topics**:
1. What is Processing? History and philosophy
2. Installing Python Mode
3. The canvas: pixels, coordinates, dimensions
4. Basic shapes and their parameters
5. Color as RGB values
6. The animation loop: `setup()` runs once, `draw()` loops forever
7. Console output with `print()`

**Key Functions**:
```python
size(), background(), fill(), stroke(), strokeWeight(), noStroke(), noFill()
point(), line(), rect(), ellipse(), triangle(), quad(), arc()
```

**Exercise**: Create a static composition inspired by Piet Mondrian using only rectangles and primary colors.

**Connection to Renoir Course**: Recall RGB color representation from Lesson 02 (Color Space Analysis).

---

### Lesson 02: Color Systems

**Duration**: 2-3 hours

**Learning Objectives**:
- Switch between RGB and HSB color modes
- Understand alpha (transparency) and blending
- Create color gradients programmatically
- Apply colors from external palettes

**Topics**:
1. `colorMode(RGB)` vs `colorMode(HSB)`
2. When to use each: RGB for digital, HSB for perceptual
3. Alpha channel and transparency
4. Blending modes: `blendMode()`
5. Creating gradients with loops
6. Storing colors in variables and lists
7. Loading palettes from JSON files

**Key Functions**:
```python
colorMode(), color(), red(), green(), blue(), hue(), saturation(), brightness()
blendMode(), lerpColor()
```

**Exercise**: Create a gradient background that transitions through an artist's palette (exported from renoir).

**Connection to Renoir Course**: Direct application of Lessons 02-03 (Color Spaces, Artist Comparison).

---

### Lesson 03: Motion and Animation

**Duration**: 2-3 hours

**Learning Objectives**:
- Use variables to create movement
- Implement frame-based animation
- Apply easing functions for natural motion
- Use trigonometric functions for oscillation
- Introduction to Perlin noise

**Topics**:
1. Variables that change over time
2. `frameCount` and `frameRate()`
3. Linear motion: position += speed
4. Bouncing off walls: boundary detection
5. Easing: smooth acceleration/deceleration
6. `sin()` and `cos()` for circular and wave motion
7. `noise()` for organic movement

**Key Functions**:
```python
frameCount, frameRate(), millis()
sin(), cos(), radians(), degrees()
noise(), noiseDetail(), noiseSeed()
map(), constrain(), lerp()
```

**Exercise**: Animate a circle that moves in a Lissajous curve pattern, leaving a fading trail.

**Connection to Renoir Course**: Temporal concepts from Lesson 16 (Temporal Artist Evolution).

---

### Lesson 04: Interactivity

**Duration**: 2-3 hours

**Learning Objectives**:
- Respond to mouse position and clicks
- Handle keyboard input
- Create interactive drawing tools
- Implement state machines for modes

**Topics**:
1. `mouseX`, `mouseY`, `pmouseX`, `pmouseY`
2. `mousePressed`, `mouseReleased`, `mouseClicked`
3. `keyPressed`, `keyReleased`, `key`, `keyCode`
4. Drawing with the mouse
5. Buttons and hover states
6. State machines: switching modes
7. Saving canvas with `save()` and `saveFrame()`

**Key Functions**:
```python
mouseX, mouseY, pmouseX, pmouseY, mousePressed, mouseButton
keyPressed, key, keyCode
dist(), save(), saveFrame()
```

**Exercise**: Create an interactive color palette explorer where clicking selects colors and drawing applies them.

**Connection to Renoir Course**: Interactive exploration similar to notebook visualizations.

---

## Module 2: Generative Systems (Lessons 5-8)

---

### Lesson 05: Randomness and Noise

**Duration**: 2-3 hours

**Learning Objectives**:
- Use randomness with control
- Understand Perlin noise in 1D, 2D, and 3D
- Create organic, natural-feeling motion
- Seed randomness for reproducibility

**Topics**:
1. `random()` for uniform distribution
2. `randomGaussian()` for natural distribution
3. `randomSeed()` for reproducibility
4. Perlin noise: smooth randomness
5. 1D noise: animation over time
6. 2D noise: terrain, textures
7. 3D noise: animated textures

**Key Concepts**:
- Controlled chaos vs pure randomness
- Noise space navigation
- Octaves and noise detail

**Exercise**: Create an animated "landscape" using 2D Perlin noise, with colors from an Impressionist palette.

**Connection to Renoir Course**: Randomness in ML models (Lesson 10, 12).

---

### Lesson 06: Particle Systems

**Duration**: 3-4 hours

**Learning Objectives**:
- Design particle classes with position, velocity, lifespan
- Apply forces (gravity, wind, attraction)
- Create particle emitters
- Implement visual effects (trails, fading, size changes)

**Topics**:
1. Object-oriented programming in Processing.py
2. The Particle class: position, velocity, acceleration
3. Newton's laws: F = ma
4. Lifespan and death
5. Emitters: spawning particles
6. Visual enhancements: trails, glow, color shifts
7. Optimizing large particle counts

**Code Structure**:
```python
class Particle:
    def __init__(self, x, y):
        self.pos = PVector(x, y)
        self.vel = PVector.random2D()
        self.acc = PVector(0, 0)
        self.lifespan = 255

    def applyForce(self, force):
        self.acc.add(force)

    def update(self):
        self.vel.add(self.acc)
        self.pos.add(self.vel)
        self.acc.mult(0)
        self.lifespan -= 2

    def display(self):
        fill(255, self.lifespan)
        ellipse(self.pos.x, self.pos.y, 8, 8)

    def isDead(self):
        return self.lifespan <= 0
```

**Exercise**: Create a fireworks display using artist-specific color palettes for each burst.

**Connection to Renoir Course**: Color diversity metrics (Lesson 04) applied to particle variety.

---

### Lesson 07: Flow Fields

**Duration**: 3-4 hours

**Learning Objectives**:
- Create vector fields using noise
- Implement steering behaviors
- Build flocking simulations
- Generate emergent patterns

**Topics**:
1. Vector fields: a grid of directions
2. Generating fields with Perlin noise
3. Particles following flow fields
4. Steering behaviors: seek, flee, arrive
5. Flocking: separation, alignment, cohesion
6. Visualizing the field itself
7. Animating the field over time

**Key Concepts**:
- Emergence: simple rules → complex behavior
- Reynolds flocking algorithm
- Field-based composition

**Exercise**: Create a flow field visualization where colors change based on the field's direction, using warm colors for rightward flow and cool colors for leftward.

**Connection to Renoir Course**: Color temperature analysis (Lesson 03) applied to directional data.

---

### Lesson 08: Recursive Structures

**Duration**: 3-4 hours

**Learning Objectives**:
- Understand recursion in visual contexts
- Draw fractals (trees, Sierpinski, Koch)
- Implement L-systems
- Apply transformation matrices

**Topics**:
1. Recursion fundamentals: base case + recursive case
2. Recursive tree drawing
3. Classic fractals: Sierpinski triangle, Koch snowflake
4. L-systems: formal grammars for growth
5. `pushMatrix()` and `popMatrix()`
6. `translate()`, `rotate()`, `scale()`
7. Combining recursion with randomness

**Key Functions**:
```python
pushMatrix(), popMatrix(), pushStyle(), popStyle()
translate(), rotate(), scale()
```

**Exercise**: Create an L-system plant that grows with colors transitioning from earth tones (roots) to greens (leaves) to flower colors from a chosen artist's palette.

**Connection to Renoir Course**: Genre analysis (Lesson 06) - landscape color distributions.

---

## Module 3: Art-Historical Integration (Lessons 9-12)

---

### Lesson 09: Palette-Driven Generation

**Duration**: 3-4 hours

**Learning Objectives**:
- Load and parse palette data from renoir exports
- Implement weighted color selection
- Create smooth color interpolation
- Build palette-aware generative systems

**Topics**:
1. Exporting palettes from renoir to JSON
2. Loading JSON in Processing.py
3. Random color selection from palettes
4. Weighted selection based on color prominence
5. `lerpColor()` for smooth transitions
6. Creating color gradients from palettes
7. Palette cycling and animation

**Integration Code**:
```python
# palette_utils.py - utility functions
def loadPalette(filename):
    with open(filename) as f:
        data = json.load(f)
    return [color(c[0], c[1], c[2]) for c in data['colors']]

def weightedChoice(palette, weights):
    total = sum(weights)
    r = random(total)
    cumulative = 0
    for i, w in enumerate(weights):
        cumulative += w
        if r <= cumulative:
            return palette[i]
    return palette[-1]
```

**Exercise**: Create a generative composition that uses Monet's palette for background elements and Van Gogh's palette for foreground, demonstrating visual contrast between Impressionism and Post-Impressionism.

**Connection to Renoir Course**: Direct use of Lesson 01-04 palette extraction.

---

### Lesson 10: Movement Aesthetics

**Duration**: 3-4 hours

**Learning Objectives**:
- Recreate visual characteristics of art movements computationally
- Implement brushstroke simulations
- Create movement-specific generative styles

**Topics**:
1. Impressionism: broken color, light, small strokes
2. Expressionism: bold strokes, distortion, emotion
3. Cubism: fragmentation, multiple perspectives
4. Abstract Expressionism: gesture, all-over composition
5. Minimalism: reduction, geometric precision
6. Implementing each as a generative system

**Movement Techniques**:
```python
# Impressionist brushstroke
def impressionistStroke(x, y, col):
    pushMatrix()
    translate(x, y)
    rotate(noise(x*0.01, y*0.01) * TWO_PI)
    strokeWeight(random(2, 5))
    stroke(col)
    line(-5, 0, 5, 0)
    popMatrix()

# Expressionist distortion
def expressionistShape(x, y, size, col):
    fill(col)
    beginShape()
    for a in range(0, 360, 30):
        r = size + noise(a*0.1, frameCount*0.01) * 20 - 10
        vertex(x + cos(radians(a))*r, y + sin(radians(a))*r)
    endShape(CLOSE)
```

**Exercise**: Create three versions of the same composition (e.g., a landscape) in Impressionist, Expressionist, and Minimalist styles, each using appropriate color palettes from renoir.

**Connection to Renoir Course**: Movement classification (Lesson 12) now as generation targets.

---

### Lesson 11: Artist Style Transfer

**Duration**: 3-4 hours

**Learning Objectives**:
- Analyze artist-specific color signatures
- Recreate compositional tendencies
- Combine color + stroke + composition into style

**Topics**:
1. What defines an artist's style computationally?
2. Color signature: dominant hues, saturation levels
3. Compositional tendencies: center vs edge, symmetry
4. Stroke characteristics: size, direction, density
5. Genre influences: how portraits differ from landscapes
6. Building artist-specific generators

**Case Studies**:
- Monet: atmospheric, light-focused, cool shadows
- Van Gogh: swirling, directional, complementary pairs
- Rothko: color field, soft edges, luminosity
- Mondrian: grid, primary colors, black lines

**Exercise**: Create a "style dial" that interpolates between two artists' generative styles based on mouse position.

**Connection to Renoir Course**: Artist Color DNA (Lesson 14), style classification.

---

### Lesson 12: Data-Driven Art

**Duration**: 3-4 hours

**Learning Objectives**:
- Visualize art historical data from WikiArt
- Create data-driven compositions
- Animate historical patterns

**Topics**:
1. Exporting WikiArt metadata from renoir
2. Visualizing genre distributions as compositions
3. Temporal data: animating through art history
4. Comparative visualizations: artist vs artist
5. Encoding data in visual properties (size, position, color)
6. Interactive data exploration

**Data Visualization Approaches**:
- Genre pie charts as radial compositions
- Timeline of color evolution
- Scatter plots of saturation vs brightness
- Network visualizations of artist similarities

**Exercise**: Create an animated timeline showing how Impressionist color palettes evolved from 1860-1890, using real data from renoir's temporal analysis.

**Connection to Renoir Course**: Direct visualization of Lesson 08, 12, 14, 16 outputs.

---

## Module 4: Advanced Techniques (Lessons 13-16)

---

### Lesson 13: Image Processing

**Duration**: 3-4 hours

**Learning Objectives**:
- Load and manipulate images in Processing
- Access and modify pixel data
- Create custom filters and effects
- Extract colors from reference images

**Topics**:
1. `loadImage()` and `image()`
2. `pixels[]` array access
3. Color extraction from images
4. Custom filters: blur, sharpen, edge detection
5. Image remixing: pointillism, mosaic
6. Blending images with generative elements

**Key Functions**:
```python
loadImage(), image(), get(), set(), pixels[], loadPixels(), updatePixels()
tint(), filter()
```

**Exercise**: Load a masterwork, extract its palette dynamically, then recreate the image using only geometric shapes in those colors (computational pointillism).

**Connection to Renoir Course**: Same image analysis techniques, now with creative output.

---

### Lesson 14: Typography and Text

**Duration**: 2-3 hours

**Learning Objectives**:
- Render text in Processing
- Create generative typography
- Use text as visual element
- Implement concrete poetry

**Topics**:
1. `text()` and `textFont()`
2. Loading custom fonts
3. Text alignment and sizing
4. Character-by-character manipulation
5. Text along paths
6. Generative letter forms
7. Concrete/visual poetry

**Creative Applications**:
- Color names (from renoir's ColorNamer) as visual elements
- Artist names forming their palette colors
- Movement manifestos as generative art

**Exercise**: Create a visual poem using evocative color names from renoir's ColorNamer module, with each word rendered in its corresponding color.

**Connection to Renoir Course**: ColorNamer vocabulary (Lesson 11).

---

### Lesson 15: Sound and Music

**Duration**: 3-4 hours

**Learning Objectives**:
- Load and play audio in Processing
- Analyze audio frequency data
- Create audio-reactive visuals
- Sync animation to rhythm

**Topics**:
1. Processing Sound library setup
2. Loading and playing audio files
3. Amplitude analysis: volume-reactive visuals
4. FFT: frequency spectrum visualization
5. Beat detection
6. MIDI input (optional)
7. Generative music visualization

**Key Concepts**:
- Frequency → color mapping
- Amplitude → size/opacity
- Beat → particle emission
- Genre → visual style

**Exercise**: Create a music visualizer that uses warm colors for bass frequencies and cool colors for treble, with the palette drawn from renoir's color temperature analysis.

**Connection to Renoir Course**: Color temperature and psychology (Lesson 09).

---

### Lesson 16: Export and Production

**Duration**: 2-3 hours

**Learning Objectives**:
- Export high-resolution images
- Record video from sketches
- Prepare work for print
- Create exhibition-ready outputs

**Topics**:
1. `save()` for single images
2. `saveFrame()` for image sequences
3. High-resolution export techniques
4. Video encoding with FFmpeg
5. Print preparation: DPI, color profiles
6. Creating loops for digital display
7. Documentation and portfolio presentation

**Production Techniques**:
```python
# High-res export
def keyPressed():
    if key == 's':
        # Scale up for high-res
        scaleFactor = 4
        pg = createGraphics(width*scaleFactor, height*scaleFactor)
        pg.beginDraw()
        pg.scale(scaleFactor)
        # Redraw at high resolution
        drawComposition(pg)
        pg.endDraw()
        pg.save("highres_" + str(frameCount) + ".png")
```

**Exercise**: Export a final composition at print resolution (300 DPI, A2 size) with proper color management.

**Connection to Renoir Course**: Publication-ready output from both courses.

---

## Module 5: Capstone (Lesson 17)

---

### Lesson 17: Capstone Project

**Duration**: 6-8 hours (spread across multiple sessions)

**Project Brief**:

Create a cohesive series of 3-5 generative artworks that:
1. Are inspired by a specific artist, movement, or theme from art history
2. Use color palettes extracted via renoir
3. Demonstrate mastery of at least 3 techniques from Modules 1-4
4. Include at least one interactive piece
5. Are documented with an artist statement

**Deliverables**:
1. **3-5 Final Artworks** (high-resolution exports)
2. **Source Code** (well-commented Processing.py sketches)
3. **Artist Statement** (500-750 words) explaining:
   - Concept and inspiration
   - Technical approach
   - Connection to art historical precedent
   - Personal reflection on the creative process
4. **Process Documentation** (screenshots, variations, failed experiments)

**Assessment Criteria**:
- Technical proficiency (30%)
- Conceptual coherence (25%)
- Art historical engagement (20%)
- Visual quality (15%)
- Documentation (10%)

**Example Project Ideas**:
1. "Digital Impressions": Particle systems recreating Monet's water lily studies
2. "Starry Night Variations": Flow fields inspired by Van Gogh's swirling skies
3. "Color Field Meditations": Interactive Rothko-inspired color explorations
4. "Computational Cubism": Fragmented portraits using Picasso's palette
5. "Movement Timeline": Animated journey through art history's color evolution

**Connection to Renoir Course**: Culmination of both courses - from analysis to generation.

---

## Appendix: Technical Setup

### Installing Python Mode

1. Download Processing 4 from processing.org
2. Open Processing
3. Click mode selector → "Add Mode..."
4. Install "Python Mode for Processing 4"
5. Switch to Python Mode

### Installing Sound Library

1. Sketch → Import Library → Add Library
2. Search "Sound"
3. Install "Sound" by The Processing Foundation

### Renoir Integration Setup

```bash
pip install renoir-wikiart
```

Then use the utilities in `utils/` to export palettes for Processing.
