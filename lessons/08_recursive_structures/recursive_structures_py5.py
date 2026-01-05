"""
Lesson 08: Recursive Structures (py5 version)
=============================================

Explore recursion to create fractals, trees,
and self-similar patterns.

Learning Objectives:
- Understand recursive functions
- Create fractal patterns
- Build generative trees
- Control recursion depth

Run with: python recursive_structures_py5.py
"""

import py5

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

    py5.size(800, 600)

    palette = [
        py5.color(139, 90, 43),    # Branch brown
        py5.color(34, 139, 34),    # Forest green
        py5.color(107, 142, 35),   # Olive drab
        py5.color(85, 107, 47),    # Dark olive
        py5.color(46, 139, 87),    # Sea green
    ]

    print("Lesson 08: Recursive Structures")
    print("\nControls:")
    print("  Press 1-4 to switch patterns")
    print("  Up/Down to change depth")
    print("  Press 'a' to toggle animation")
    print("  Press 's' to save image")


def draw():
    py5.background(245)

    if mode == 0:
        draw_tree()
    elif mode == 1:
        draw_sierpinski()
    elif mode == 2:
        draw_koch()
    elif mode == 3:
        draw_circles()

    # UI
    draw_ui()

    # Animation
    if animate:
        global angle_offset
        angle_offset += 0.02


def draw_tree():
    """Recursive tree structure."""
    py5.translate(py5.width/2, py5.height - 50)

    py5.stroke(palette[0])
    py5.stroke_weight(8)

    branch(120, max_depth)


def branch(length, depth):
    """Recursively draw tree branches."""
    if depth <= 0:
        return

    # Draw this branch
    weight = py5.remap(depth, 0, max_depth, 1, 8)
    py5.stroke_weight(weight)

    # Color changes with depth
    if depth <= 2:
        py5.stroke(palette[int(py5.random(1, len(palette)))])  # Leaves
    else:
        py5.stroke(palette[0])  # Trunk

    py5.line(0, 0, 0, -length)

    # Move to end of branch
    py5.translate(0, -length)

    # Calculate branch angle with optional animation
    base_angle = py5.PI/6
    angle = base_angle + py5.sin(angle_offset + depth * 0.5) * 0.1 if animate else base_angle

    # Right branch
    py5.push_matrix()
    py5.rotate(angle)
    branch(length * 0.7, depth - 1)
    py5.pop_matrix()

    # Left branch
    py5.push_matrix()
    py5.rotate(-angle)
    branch(length * 0.7, depth - 1)
    py5.pop_matrix()

    # Sometimes add a middle branch
    if depth > 2 and py5.random(1) > 0.5:
        py5.push_matrix()
        py5.rotate(py5.random(-0.1, 0.1))
        branch(length * 0.5, depth - 2)
        py5.pop_matrix()


def draw_sierpinski():
    """Sierpinski triangle fractal."""
    # Start points
    size_val = 500
    x1 = py5.width/2
    y1 = py5.height/2 - size_val/2
    x2 = py5.width/2 - size_val/2
    y2 = py5.height/2 + size_val/3
    x3 = py5.width/2 + size_val/2
    y3 = py5.height/2 + size_val/3

    py5.no_stroke()
    sierpinski(x1, y1, x2, y2, x3, y3, max_depth)


def sierpinski(x1, y1, x2, y2, x3, y3, depth):
    """Recursively draw Sierpinski triangle."""
    if depth <= 0:
        # Draw filled triangle
        py5.fill(py5.lerp_color(palette[1], palette[4], py5.random(1)))
        py5.triangle(x1, y1, x2, y2, x3, y3)
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


def draw_koch():
    """Koch snowflake curve."""
    py5.stroke(66, 133, 244)
    py5.stroke_weight(2)
    py5.no_fill()

    # Draw three sides of the snowflake
    size_val = 400
    h = size_val * py5.sqrt(3) / 2

    x1 = py5.width/2 - size_val/2
    y1 = py5.height/2 + h/3
    x2 = py5.width/2 + size_val/2
    y2 = py5.height/2 + h/3
    x3 = py5.width/2
    y3 = py5.height/2 - 2*h/3

    koch(x1, y1, x2, y2, max_depth)
    koch(x2, y2, x3, y3, max_depth)
    koch(x3, y3, x1, y1, max_depth)


def koch(x1, y1, x2, y2, depth):
    """Recursively draw Koch curve segment."""
    if depth <= 0:
        py5.line(x1, y1, x2, y2)
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
    angle = py5.atan2(dy, dx) - py5.PI/3
    length = py5.sqrt(dx*dx + dy*dy) / 3
    px = ax + py5.cos(angle) * length
    py_val = ay + py5.sin(angle) * length

    # Recurse on four segments
    koch(x1, y1, ax, ay, depth - 1)
    koch(ax, ay, px, py_val, depth - 1)
    koch(px, py_val, bx, by, depth - 1)
    koch(bx, by, x2, y2, depth - 1)


def draw_circles():
    """Recursive packed circles."""
    py5.no_stroke()
    recursive_circle(py5.width/2, py5.height/2, 250, max_depth)


def recursive_circle(x, y, radius, depth):
    """Recursively draw circles with smaller circles inside."""
    if depth <= 0 or radius < 5:
        return

    # Draw main circle
    py5.fill(palette[depth % len(palette)], 150)
    py5.ellipse(x, y, radius * 2, radius * 2)

    # Draw smaller circles around the edge
    num_circles = 6
    small_radius = radius / 3

    for i in range(num_circles):
        angle = i * py5.TWO_PI / num_circles + (angle_offset if animate else 0)
        cx = x + py5.cos(angle) * (radius - small_radius)
        cy = y + py5.sin(angle) * (radius - small_radius)
        recursive_circle(cx, cy, small_radius * 0.8, depth - 1)


def draw_ui():
    """Draw mode and depth info."""
    py5.fill(0)
    py5.no_stroke()
    py5.text_size(14)
    py5.text(f"Pattern: {modes[mode]}", 20, 25)
    py5.text(f"Depth: {max_depth}", 20, 45)
    py5.text(f"Animation: {'ON' if animate else 'OFF'}", 20, 65)


def key_pressed():
    global mode, max_depth, animate

    if py5.key == '1':
        mode = 0
    elif py5.key == '2':
        mode = 1
    elif py5.key == '3':
        mode = 2
    elif py5.key == '4':
        mode = 3
    elif py5.key_code == py5.UP:
        max_depth = min(max_depth + 1, 10)
        print(f"Depth: {max_depth}")
    elif py5.key_code == py5.DOWN:
        max_depth = max(max_depth - 1, 1)
        print(f"Depth: {max_depth}")
    elif py5.key == 'a':
        animate = not animate
        print(f"Animation: {'ON' if animate else 'OFF'}")
    elif py5.key == 's':
        filename = f"recursive_{py5.frame_count}.png"
        py5.save(filename)
        print(f"Saved: {filename}")


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

py5.run_sketch()
