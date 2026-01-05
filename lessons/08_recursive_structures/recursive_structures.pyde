"""
Lesson 08: Recursive Structures
===============================

Explore recursion to create fractals, trees,
and self-similar patterns.

Learning Objectives:
- Understand recursive functions
- Create fractal patterns
- Build generative trees
- Control recursion depth

Run this sketch in Processing with Python Mode enabled.
"""

# Mode and settings
mode = 0
modes = ["Tree", "Sierpinski", "Koch Curve", "Circles"]
max_depth = 6

# Animation
angle_offset = 0
animate = False

# Palette
palette = []


def setup():
    global palette

    size(800, 600)

    palette = [
        color(139, 90, 43),    # Branch brown
        color(34, 139, 34),    # Forest green
        color(107, 142, 35),   # Olive drab
        color(85, 107, 47),    # Dark olive
        color(46, 139, 87),    # Sea green
    ]

    print("Lesson 08: Recursive Structures")
    print("\nControls:")
    print("  Press 1-4 to switch patterns")
    print("  Up/Down to change depth")
    print("  Press 'a' to toggle animation")
    print("  Press 's' to save image")


def draw():
    background(245)

    if mode == 0:
        drawTree()
    elif mode == 1:
        drawSierpinski()
    elif mode == 2:
        drawKoch()
    elif mode == 3:
        drawCircles()

    # UI
    drawUI()

    # Animation
    if animate:
        global angle_offset
        angle_offset += 0.02


def drawTree():
    """Recursive tree structure."""
    translate(width/2, height - 50)

    stroke(palette[0])
    strokeWeight(8)

    branch(120, max_depth)


def branch(length, depth):
    """Recursively draw tree branches."""
    if depth <= 0:
        return

    # Draw this branch
    weight = map(depth, 0, max_depth, 1, 8)
    strokeWeight(weight)

    # Color changes with depth
    if depth <= 2:
        stroke(palette[int(random(1, len(palette)))])  # Leaves
    else:
        stroke(palette[0])  # Trunk

    line(0, 0, 0, -length)

    # Move to end of branch
    translate(0, -length)

    # Calculate branch angle with optional animation
    base_angle = PI/6
    angle = base_angle + sin(angle_offset + depth * 0.5) * 0.1 if animate else base_angle

    # Right branch
    pushMatrix()
    rotate(angle)
    branch(length * 0.7, depth - 1)
    popMatrix()

    # Left branch
    pushMatrix()
    rotate(-angle)
    branch(length * 0.7, depth - 1)
    popMatrix()

    # Sometimes add a middle branch
    if depth > 2 and random(1) > 0.5:
        pushMatrix()
        rotate(random(-0.1, 0.1))
        branch(length * 0.5, depth - 2)
        popMatrix()


def drawSierpinski():
    """Sierpinski triangle fractal."""
    # Start points
    size_val = 500
    x1 = width/2
    y1 = height/2 - size_val/2
    x2 = width/2 - size_val/2
    y2 = height/2 + size_val/3
    x3 = width/2 + size_val/2
    y3 = height/2 + size_val/3

    noStroke()
    sierpinski(x1, y1, x2, y2, x3, y3, max_depth)


def sierpinski(x1, y1, x2, y2, x3, y3, depth):
    """Recursively draw Sierpinski triangle."""
    if depth <= 0:
        # Draw filled triangle
        fill(lerpColor(palette[1], palette[4], random(1)))
        triangle(x1, y1, x2, y2, x3, y3)
        return

    # Calculate midpoints
    mx1 = (x1 + x2) / 2
    my1 = (y1 + y2) / 2
    mx2 = (x2 + x3) / 2
    my2 = (y2 + y3) / 2
    mx3 = (x1 + x3) / 2
    my3 = (y1 + y3) / 2

    # Recurse on three sub-triangles
    sierpinski(x1, y1, mx1, my1, mx3, my3, depth - 1)
    sierpinski(mx1, my1, x2, y2, mx2, my2, depth - 1)
    sierpinski(mx3, my3, mx2, my2, x3, y3, depth - 1)


def drawKoch():
    """Koch snowflake curve."""
    stroke(66, 133, 244)
    strokeWeight(2)
    noFill()

    # Draw three sides of the snowflake
    size_val = 400
    h = size_val * sqrt(3) / 2

    x1 = width/2 - size_val/2
    y1 = height/2 + h/3
    x2 = width/2 + size_val/2
    y2 = height/2 + h/3
    x3 = width/2
    y3 = height/2 - 2*h/3

    koch(x1, y1, x2, y2, max_depth)
    koch(x2, y2, x3, y3, max_depth)
    koch(x3, y3, x1, y1, max_depth)


def koch(x1, y1, x2, y2, depth):
    """Recursively draw Koch curve segment."""
    if depth <= 0:
        line(x1, y1, x2, y2)
        return

    # Calculate the four new points
    dx = x2 - x1
    dy = y2 - y1

    # Point at 1/3
    ax = x1 + dx/3
    ay = y1 + dy/3

    # Point at 2/3
    bx = x1 + 2*dx/3
    by = y1 + 2*dy/3

    # Peak point (equilateral triangle)
    angle = atan2(dy, dx) - PI/3
    length = sqrt(dx*dx + dy*dy) / 3
    px = ax + cos(angle) * length
    py = ay + sin(angle) * length

    # Recurse on four segments
    koch(x1, y1, ax, ay, depth - 1)
    koch(ax, ay, px, py, depth - 1)
    koch(px, py, bx, by, depth - 1)
    koch(bx, by, x2, y2, depth - 1)


def drawCircles():
    """Recursive packed circles."""
    noStroke()
    recursiveCircle(width/2, height/2, 250, max_depth)


def recursiveCircle(x, y, radius, depth):
    """Recursively draw circles with smaller circles inside."""
    if depth <= 0 or radius < 5:
        return

    # Draw main circle
    fill(palette[depth % len(palette)], 150)
    ellipse(x, y, radius * 2, radius * 2)

    # Draw smaller circles around the edge
    num_circles = 6
    small_radius = radius / 3

    for i in range(num_circles):
        angle = i * TWO_PI / num_circles + (angle_offset if animate else 0)
        cx = x + cos(angle) * (radius - small_radius)
        cy = y + sin(angle) * (radius - small_radius)
        recursiveCircle(cx, cy, small_radius * 0.8, depth - 1)


def drawUI():
    """Draw mode and depth info."""
    fill(0)
    noStroke()
    textSize(14)
    text("Pattern: " + modes[mode], 20, 25)
    text("Depth: " + str(max_depth), 20, 45)
    text("Animation: " + ("ON" if animate else "OFF"), 20, 65)


def keyPressed():
    global mode, max_depth, animate

    if key == '1':
        mode = 0
    elif key == '2':
        mode = 1
    elif key == '3':
        mode = 2
    elif key == '4':
        mode = 3
    elif keyCode == UP:
        max_depth = min(max_depth + 1, 10)
        print("Depth:", max_depth)
    elif keyCode == DOWN:
        max_depth = max(max_depth - 1, 1)
        print("Depth:", max_depth)
    elif key == 'a':
        animate = not animate
        print("Animation:", "ON" if animate else "OFF")
    elif key == 's':
        filename = "recursive_" + str(frameCount) + ".png"
        save(filename)
        print("Saved:", filename)


# -------------------------------------------------
# Recursion Concepts:
#
# 1. Base case: When to stop (depth <= 0)
# 2. Recursive case: Call self with modified params
# 3. Each call handles a smaller problem
#
# Key patterns:
# - Tree: Split into branches at each level
# - Sierpinski: Divide triangle into sub-triangles
# - Koch: Replace line with peaked shape
# - Circles: Nest smaller circles
#
# Connection to Renoir:
# Many natural forms exhibit self-similarity:
# - Tree branches (fractal branching)
# - Cloud formations
# - Rock textures
# - Wave patterns
# Artists often intuitively capture these patterns.
# -------------------------------------------------
