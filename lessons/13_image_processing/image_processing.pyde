"""
Lesson 13: Image Processing
===========================

Learn to load, manipulate, and transform images
using pixel-level operations.

Learning Objectives:
- Load and display images
- Access and modify pixels
- Apply filters and effects
- Create artistic image transformations

Run this sketch in Processing with Python Mode enabled.
Note: Place an image named 'source.jpg' in the data/ folder.
"""

# Image and mode
img = None
mode = 0
modes = ["Original", "Grayscale", "Threshold", "Pixelate", "Pointillism", "Color Shift"]

# Effect parameters
threshold_val = 128
pixel_size = 10
point_density = 5000

# Palette for pointillism
palette = []


def setup():
    size(800, 600)
    global img, palette

    # Try to load image
    try:
        img = loadImage("data/source.jpg")
        if img:
            img.resize(800, 600)
    except:
        img = None

    # Fallback: create a gradient image
    if img is None:
        img = createImage(800, 600, RGB)
        img.loadPixels()
        for y in range(img.height):
            for x in range(img.width):
                r = map(x, 0, img.width, 50, 200)
                g = map(y, 0, img.height, 100, 180)
                b = 150
                img.pixels[y * img.width + x] = color(r, g, b)
        img.updatePixels()
        print("No image found - using generated gradient")
        print("Place 'source.jpg' in data/ folder for real images")

    # Art palette for pointillism
    palette = [
        color(142, 178, 197),
        color(219, 68, 55),
        color(244, 180, 0),
        color(15, 157, 88),
        color(156, 39, 176),
    ]

    print("Lesson 13: Image Processing")
    print("\nControls:")
    print("  Press 1-6 to switch effects")
    print("  Up/Down to adjust parameters")
    print("  Press 's' to save image")


def draw():
    background(30)

    if mode == 0:
        drawOriginal()
    elif mode == 1:
        drawGrayscale()
    elif mode == 2:
        drawThreshold()
    elif mode == 3:
        drawPixelate()
    elif mode == 4:
        drawPointillism()
    elif mode == 5:
        drawColorShift()

    drawUI()


def drawOriginal():
    """Display original image."""
    image(img, 0, 0)


def drawGrayscale():
    """Convert to grayscale."""
    result = createImage(img.width, img.height, RGB)
    img.loadPixels()
    result.loadPixels()

    for i in range(len(img.pixels)):
        c = img.pixels[i]
        r = red(c)
        g = green(c)
        b = blue(c)
        # Luminance formula
        gray = 0.299 * r + 0.587 * g + 0.114 * b
        result.pixels[i] = color(gray)

    result.updatePixels()
    image(result, 0, 0)


def drawThreshold():
    """Binary threshold effect."""
    result = createImage(img.width, img.height, RGB)
    img.loadPixels()
    result.loadPixels()

    for i in range(len(img.pixels)):
        c = img.pixels[i]
        gray = (red(c) + green(c) + blue(c)) / 3

        if gray > threshold_val:
            result.pixels[i] = color(255)
        else:
            result.pixels[i] = color(0)

    result.updatePixels()
    image(result, 0, 0)


def drawPixelate():
    """Pixelation effect."""
    noStroke()

    for y in range(0, img.height, pixel_size):
        for x in range(0, img.width, pixel_size):
            # Sample center of block
            c = img.get(x + pixel_size/2, y + pixel_size/2)
            fill(c)
            rect(x, y, pixel_size, pixel_size)


def drawPointillism():
    """Pointillist rendering using palette colors."""
    background(240)
    noStroke()

    for _ in range(point_density):
        x = int(random(img.width))
        y = int(random(img.height))

        # Get image color
        c = img.get(x, y)

        # Find closest palette color
        closest = findClosestColor(c)

        # Draw dot
        fill(closest, 200)
        size_val = random(3, 8)
        ellipse(x, y, size_val, size_val)


def findClosestColor(target):
    """Find closest color in palette."""
    min_dist = float('inf')
    closest = palette[0]

    tr = red(target)
    tg = green(target)
    tb = blue(target)

    for c in palette:
        pr = red(c)
        pg = green(c)
        pb = blue(c)

        d = sqrt((tr - pr)**2 + (tg - pg)**2 + (tb - pb)**2)
        if d < min_dist:
            min_dist = d
            closest = c

    return closest


def drawColorShift():
    """Shift colors in HSB space."""
    result = createImage(img.width, img.height, RGB)
    img.loadPixels()
    result.loadPixels()

    shift = map(mouseX, 0, width, 0, 360)

    colorMode(HSB, 360, 100, 100)

    for i in range(len(img.pixels)):
        c = img.pixels[i]
        h = hue(c)
        s = saturation(c)
        b = brightness(c)

        # Shift hue
        new_h = (h + shift) % 360
        result.pixels[i] = color(new_h, s, b)

    colorMode(RGB, 255)
    result.updatePixels()
    image(result, 0, 0)


def drawUI():
    """Draw effect info."""
    fill(0, 180)
    noStroke()
    rect(10, 10, 200, 70, 5)

    fill(255)
    textSize(14)
    text("Effect: " + modes[mode], 20, 32)

    textSize(11)
    if mode == 2:
        text("Threshold: " + str(threshold_val), 20, 52)
        text("Up/Down to adjust", 20, 68)
    elif mode == 3:
        text("Pixel size: " + str(pixel_size), 20, 52)
        text("Up/Down to adjust", 20, 68)
    elif mode == 4:
        text("Density: " + str(point_density), 20, 52)
        text("Up/Down to adjust", 20, 68)
    elif mode == 5:
        text("Move mouse to shift hue", 20, 52)


def keyPressed():
    global mode, threshold_val, pixel_size, point_density

    if key == '1':
        mode = 0
    elif key == '2':
        mode = 1
    elif key == '3':
        mode = 2
    elif key == '4':
        mode = 3
    elif key == '5':
        mode = 4
    elif key == '6':
        mode = 5
    elif keyCode == UP:
        if mode == 2:
            threshold_val = min(threshold_val + 10, 255)
        elif mode == 3:
            pixel_size = min(pixel_size + 2, 50)
        elif mode == 4:
            point_density = min(point_density + 500, 20000)
    elif keyCode == DOWN:
        if mode == 2:
            threshold_val = max(threshold_val - 10, 0)
        elif mode == 3:
            pixel_size = max(pixel_size - 2, 2)
        elif mode == 4:
            point_density = max(point_density - 500, 500)
    elif key == 's':
        filename = "processed_" + str(frameCount) + ".png"
        save(filename)
        print("Saved:", filename)


# -------------------------------------------------
# Image Processing Concepts:
#
# 1. Pixel Access:
#    img.loadPixels()  - Load into pixels[]
#    img.pixels[i]     - Access pixel i
#    img.updatePixels() - Apply changes
#    img.get(x, y)     - Get color at x,y
#
# 2. Color Components:
#    red(c), green(c), blue(c)
#    hue(c), saturation(c), brightness(c)
#
# 3. Common Operations:
#    - Grayscale: Average RGB or use luminance
#    - Threshold: Binary black/white
#    - Pixelate: Sample blocks
#    - Color shift: Modify HSB values
#
# Connection to Renoir:
# Image processing can extract color palettes
# from artwork images, which is exactly what
# renoir's ColorExtractor does using k-means
# clustering.
# -------------------------------------------------
