# Encre: Processing.py Quick Reference

A cheatsheet for common Processing.py functions and patterns used in the Encre course.

## Program Structure

```python
def setup():
    """Runs once at the start."""
    size(800, 600)  # Set canvas size
    background(255)  # White background

def draw():
    """Loops continuously (~60 fps)."""
    ellipse(mouseX, mouseY, 50, 50)
```

## Canvas and Coordinates

```python
size(width, height)      # Set canvas size (call in setup)
size(800, 600, P3D)      # 3D mode
fullScreen()             # Full screen mode

width                    # Canvas width
height                   # Canvas height

background(gray)         # Grayscale 0-255
background(r, g, b)      # RGB color
background(r, g, b, a)   # With alpha
```

## Color

### Color Modes
```python
colorMode(RGB, 255)           # RGB mode, 0-255 range
colorMode(RGB, 255, 255, 255, 100)  # Custom ranges + alpha
colorMode(HSB, 360, 100, 100) # HSB mode (Hue, Saturation, Brightness)
```

### Setting Colors
```python
fill(gray)               # Grayscale fill
fill(r, g, b)           # RGB fill
fill(r, g, b, alpha)    # With transparency
noFill()                # No fill

stroke(gray)            # Grayscale stroke
stroke(r, g, b)         # RGB stroke
noStroke()              # No stroke

strokeWeight(pixels)    # Line thickness
```

### Color Functions
```python
c = color(r, g, b)      # Create color object
c = color(r, g, b, a)   # With alpha

red(c)                  # Extract red component
green(c)                # Extract green component
blue(c)                 # Extract blue component
alpha(c)                # Extract alpha component

hue(c)                  # Extract hue (HSB mode)
saturation(c)           # Extract saturation
brightness(c)           # Extract brightness

lerpColor(c1, c2, amt)  # Interpolate between colors (amt: 0-1)
```

### Blend Modes
```python
blendMode(BLEND)        # Default
blendMode(ADD)          # Additive
blendMode(MULTIPLY)     # Multiply
blendMode(SCREEN)       # Screen
blendMode(SUBTRACT)     # Subtract
```

## Shapes

### Basic Shapes
```python
point(x, y)
line(x1, y1, x2, y2)
rect(x, y, width, height)
rect(x, y, w, h, radius)         # Rounded corners
ellipse(x, y, width, height)
circle(x, y, diameter)
triangle(x1, y1, x2, y2, x3, y3)
quad(x1, y1, x2, y2, x3, y3, x4, y4)
arc(x, y, w, h, start, stop)     # Angles in radians
```

### Shape Modes
```python
rectMode(CORNER)        # x,y is top-left (default)
rectMode(CENTER)        # x,y is center
rectMode(CORNERS)       # x,y and w,h are opposite corners

ellipseMode(CENTER)     # x,y is center (default)
ellipseMode(CORNER)     # x,y is top-left
```

### Custom Shapes
```python
beginShape()
vertex(x, y)
vertex(x, y)
vertex(x, y)
endShape(CLOSE)         # CLOSE connects last to first

# Curved shapes
beginShape()
curveVertex(x, y)       # Catmull-Rom spline
endShape()

beginShape()
bezierVertex(cx1, cy1, cx2, cy2, x, y)  # Bezier curve
endShape()
```

## Transformations

```python
translate(x, y)         # Move origin
rotate(angle)           # Rotate (radians)
scale(s)                # Uniform scale
scale(sx, sy)           # Non-uniform scale

pushMatrix()            # Save transformation state
popMatrix()             # Restore transformation state

pushStyle()             # Save style (fill, stroke, etc.)
popStyle()              # Restore style
```

## Math Functions

```python
# Trigonometry
sin(angle)              # Sine (radians)
cos(angle)              # Cosine
tan(angle)              # Tangent
asin(value)             # Arc sine
acos(value)             # Arc cosine
atan(value)             # Arc tangent
atan2(y, x)             # Arc tangent of y/x

radians(degrees)        # Convert degrees to radians
degrees(radians)        # Convert radians to degrees

# Constants
PI                      # 3.14159...
TWO_PI                  # 6.28318...
HALF_PI                 # 1.57079...
QUARTER_PI              # 0.78539...

# Utility
abs(n)                  # Absolute value
sqrt(n)                 # Square root
pow(base, exp)          # Power
floor(n)                # Round down
ceil(n)                 # Round up
round(n)                # Round to nearest
min(a, b)               # Minimum
max(a, b)               # Maximum

map(value, start1, stop1, start2, stop2)  # Remap value
constrain(value, min, max)                 # Clamp value
lerp(start, stop, amt)                     # Linear interpolation
dist(x1, y1, x2, y2)                       # Distance between points
mag(x, y)                                  # Vector magnitude
```

## Randomness and Noise

```python
random(high)            # Random float 0 to high
random(low, high)       # Random float in range
randomSeed(seed)        # Set random seed

randomGaussian()        # Gaussian distribution (mean=0, sd=1)

noise(x)                # 1D Perlin noise
noise(x, y)             # 2D Perlin noise
noise(x, y, z)          # 3D Perlin noise
noiseDetail(octaves)    # Set noise detail level
noiseSeed(seed)         # Set noise seed
```

## Interaction

### Mouse
```python
mouseX                  # Current X position
mouseY                  # Current Y position
pmouseX                 # Previous X position
pmouseY                 # Previous Y position
mousePressed            # Boolean: is mouse pressed?
mouseButton             # LEFT, RIGHT, or CENTER

def mousePressed():     # Called when mouse pressed
    pass

def mouseReleased():    # Called when mouse released
    pass

def mouseClicked():     # Called on click
    pass

def mouseMoved():       # Called when mouse moves (no button)
    pass

def mouseDragged():     # Called when mouse drags (button held)
    pass
```

### Keyboard
```python
keyPressed              # Boolean: is key pressed?
key                     # Character of key pressed
keyCode                 # Code for special keys

def keyPressed():       # Called when key pressed
    if key == 's':
        save("image.png")
    if keyCode == UP:
        # Up arrow pressed
        pass

def keyReleased():      # Called when key released
    pass

# Special key codes
UP, DOWN, LEFT, RIGHT
ENTER, RETURN, TAB, BACKSPACE, DELETE, ESCAPE
SHIFT, CONTROL, ALT
```

## Images

```python
img = loadImage("filename.png")  # Load image
image(img, x, y)                 # Draw image
image(img, x, y, w, h)          # Draw with size

img.width                        # Image width
img.height                       # Image height

get(x, y)                        # Get pixel color
set(x, y, color)                 # Set pixel color

loadPixels()                     # Load pixel array
pixels[index]                    # Access pixel
updatePixels()                   # Apply changes

# Index calculation: y * width + x

tint(r, g, b)                   # Tint images
tint(r, g, b, a)                # Tint with alpha
noTint()                        # Remove tint
```

## Text

```python
text("Hello", x, y)             # Draw text
text("Hello", x, y, w, h)       # Text in box

textSize(size)                  # Set font size
textAlign(LEFT)                 # LEFT, CENTER, RIGHT
textAlign(CENTER, CENTER)       # Horizontal, vertical

font = createFont("Arial", 32)  # Create font
textFont(font)                  # Use font

textWidth("string")             # Get text width
```

## Time and Animation

```python
frameCount              # Number of frames since start
frameRate(fps)          # Set frame rate
frameRate               # Current frame rate

millis()                # Milliseconds since start

# Stop/start looping
noLoop()                # Stop draw() loop
loop()                  # Resume draw() loop
redraw()                # Call draw() once
```

## Saving Output

```python
save("filename.png")            # Save current frame
save("filename.jpg")
save("filename.tif")

saveFrame("frame-####.png")     # Save with frame number
# #### becomes 0001, 0002, etc.

# For high-res export
pg = createGraphics(w, h)
pg.beginDraw()
# Draw to pg
pg.endDraw()
pg.save("highres.png")
```

## PVector (2D/3D Vectors)

```python
v = PVector(x, y)       # Create 2D vector
v = PVector(x, y, z)    # Create 3D vector

v.x, v.y, v.z           # Access components

v.add(other)            # Add vectors
v.sub(other)            # Subtract
v.mult(scalar)          # Multiply by scalar
v.div(scalar)           # Divide by scalar

v.mag()                 # Magnitude (length)
v.normalize()           # Set magnitude to 1
v.setMag(len)           # Set magnitude
v.limit(max)            # Limit magnitude

v.heading()             # Angle of 2D vector
v.rotate(angle)         # Rotate 2D vector

PVector.random2D()      # Random unit vector 2D
PVector.random3D()      # Random unit vector 3D
PVector.dist(v1, v2)    # Distance between vectors
PVector.lerp(v1, v2, t) # Interpolate
```

## Loading External Data

```python
import json

# In setup() or draw()
with open("data/palette.json") as f:
    data = json.load(f)

colors = data['colors']  # Access data
```

## Common Patterns

### Animation Loop
```python
x = 0

def setup():
    size(800, 600)

def draw():
    global x
    background(255)
    ellipse(x, height/2, 50, 50)
    x = (x + 2) % width  # Wrap around
```

### Object-Oriented Particle
```python
class Particle:
    def __init__(self, x, y):
        self.pos = PVector(x, y)
        self.vel = PVector.random2D()
        self.vel.mult(random(2, 5))

    def update(self):
        self.pos.add(self.vel)

    def display(self):
        ellipse(self.pos.x, self.pos.y, 10, 10)

particles = []

def setup():
    size(800, 600)
    for i in range(100):
        particles.append(Particle(width/2, height/2))

def draw():
    background(0)
    for p in particles:
        p.update()
        p.display()
```

### Perlin Noise Flow
```python
def setup():
    size(800, 600)
    noStroke()

def draw():
    for x in range(0, width, 10):
        for y in range(0, height, 10):
            angle = noise(x * 0.01, y * 0.01, frameCount * 0.01) * TWO_PI
            fill(angle / TWO_PI * 255, 100, 200)
            pushMatrix()
            translate(x, y)
            rotate(angle)
            rect(0, 0, 8, 2)
            popMatrix()
```
