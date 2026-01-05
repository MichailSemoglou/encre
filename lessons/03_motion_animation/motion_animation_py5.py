"""
Lesson 03: Motion and Animation (py5 version)
==============================================

Learn how the draw() loop creates animation,
and explore different motion techniques.

Learning Objectives:
- Understand the animation loop
- Create smooth motion with variables
- Use trigonometry for organic movement
- Apply easing for natural motion

Run with: python motion_animation_py5.py
"""

import py5

# Animation variables
x = 0
y = 300
angle = 0
mode = 0
modes = ["Linear", "Sine Wave", "Circular", "Easing"]

# Easing variables
target_x = 400
target_y = 300
ease_x = 0
ease_y = 0


def setup():
    py5.size(800, 600)
    global ease_x, ease_y
    ease_x = py5.width / 2
    ease_y = py5.height / 2
    print("Lesson 03: Motion and Animation")
    print("\nControls:")
    print("  Press 1-4 to switch modes")
    print("  Press 's' to save image")
    print("  Click to set easing target (mode 4)")


def draw():
    py5.background(30)

    # Draw mode indicator
    py5.fill(255)
    py5.text_size(16)
    py5.text(f"Mode: {modes[mode]}", 20, 30)
    py5.text("Press 1-4 to switch", 20, 55)

    if mode == 0:
        draw_linear()
    elif mode == 1:
        draw_sine_wave()
    elif mode == 2:
        draw_circular()
    elif mode == 3:
        draw_easing()


def draw_linear():
    """Simple linear motion - constant speed."""
    global x

    # Move right at constant speed
    x += 3

    # Wrap around when off screen
    if x > py5.width + 25:
        x = -25

    # Draw moving circle
    py5.fill(66, 133, 244)
    py5.no_stroke()
    py5.ellipse(x, py5.height/2, 50, 50)

    # Draw trail
    for i in range(10):
        alpha = py5.remap(i, 0, 10, 200, 0)
        py5.fill(66, 133, 244, alpha)
        py5.ellipse(x - i * 15, py5.height/2, 50 - i * 4, 50 - i * 4)

    # Explanation
    py5.fill(255)
    py5.text_size(14)
    py5.text("Linear motion: constant velocity", 20, py5.height - 60)
    py5.text("x += speed (same amount each frame)", 20, py5.height - 40)


def draw_sine_wave():
    """Sine wave motion - smooth oscillation."""
    global angle

    angle += 0.03

    # Horizontal position based on angle
    x = py5.width / 2
    # Vertical oscillation using sine
    y = py5.height/2 + py5.sin(angle) * 150

    # Secondary ball with different phase
    y2 = py5.height/2 + py5.sin(angle + py5.PI) * 150

    # Draw balls
    py5.fill(219, 68, 55)
    py5.no_stroke()
    py5.ellipse(x - 100, y, 50, 50)

    py5.fill(244, 180, 0)
    py5.ellipse(x + 100, y2, 50, 50)

    # Draw sine wave path
    py5.stroke(255, 100)
    py5.stroke_weight(1)
    py5.no_fill()
    py5.begin_shape()
    for i in range(py5.width):
        wave_y = py5.height/2 + py5.sin(angle + i * 0.02) * 150
        py5.vertex(i, wave_y)
    py5.end_shape()

    # Explanation
    py5.no_stroke()
    py5.fill(255)
    py5.text_size(14)
    py5.text("Sine wave: smooth oscillation", 20, py5.height - 60)
    py5.text("y = sin(angle) * amplitude", 20, py5.height - 40)


def draw_circular():
    """Circular motion using sin and cos."""
    global angle

    angle += 0.02

    center_x = py5.width / 2
    center_y = py5.height / 2
    radius = 150

    # Calculate position on circle
    x = center_x + py5.cos(angle) * radius
    y = center_y + py5.sin(angle) * radius

    # Second circle with different radius and speed
    x2 = center_x + py5.cos(angle * 2) * 80
    y2 = center_y + py5.sin(angle * 2) * 80

    # Draw orbit paths
    py5.stroke(255, 50)
    py5.stroke_weight(1)
    py5.no_fill()
    py5.ellipse(center_x, center_y, radius * 2, radius * 2)
    py5.ellipse(center_x, center_y, 160, 160)

    # Draw center
    py5.fill(100)
    py5.no_stroke()
    py5.ellipse(center_x, center_y, 30, 30)

    # Draw orbiting circles
    py5.fill(15, 157, 88)
    py5.ellipse(x, y, 40, 40)

    py5.fill(156, 39, 176)
    py5.ellipse(x2, y2, 25, 25)

    # Draw connecting line
    py5.stroke(255, 100)
    py5.line(center_x, center_y, x, y)

    # Explanation
    py5.no_stroke()
    py5.fill(255)
    py5.text_size(14)
    py5.text("Circular motion: sin + cos", 20, py5.height - 60)
    py5.text("x = cos(angle) * r, y = sin(angle) * r", 20, py5.height - 40)


def draw_easing():
    """Easing motion - smooth acceleration/deceleration."""
    global ease_x, ease_y, target_x, target_y

    # Easing formula: move a fraction of remaining distance
    easing = 0.05
    ease_x += (target_x - ease_x) * easing
    ease_y += (target_y - ease_y) * easing

    # Draw target
    py5.stroke(255, 100)
    py5.stroke_weight(1)
    py5.no_fill()
    py5.ellipse(target_x, target_y, 60, 60)
    py5.line(target_x - 10, target_y, target_x + 10, target_y)
    py5.line(target_x, target_y - 10, target_x, target_y + 10)

    # Draw easing circle
    py5.fill(0, 188, 212)
    py5.no_stroke()
    py5.ellipse(ease_x, ease_y, 50, 50)

    # Draw connection line
    py5.stroke(255, 50)
    py5.line(ease_x, ease_y, target_x, target_y)

    # Explanation
    py5.no_stroke()
    py5.fill(255)
    py5.text_size(14)
    py5.text("Easing: smooth acceleration", 20, py5.height - 80)
    py5.text("x += (target - x) * easing", 20, py5.height - 60)
    py5.text("Click anywhere to set new target", 20, py5.height - 40)


def key_pressed():
    global mode

    if py5.key == '1':
        mode = 0
    elif py5.key == '2':
        mode = 1
    elif py5.key == '3':
        mode = 2
    elif py5.key == '4':
        mode = 3
    elif py5.key == 's':
        filename = f"motion_{py5.frame_count}.png"
        py5.save(filename)
        print(f"Saved: {filename}")


def mouse_pressed():
    global target_x, target_y
    if mode == 3:  # Easing mode
        target_x = py5.mouse_x
        target_y = py5.mouse_y


# -------------------------------------------------
# Animation Principles:
#
# 1. Linear: Constant speed, mechanical feel
# 2. Sine/Cosine: Natural oscillation, organic
# 3. Circular: Orbits, rotations, pendulums
# 4. Easing: Acceleration/deceleration, lifelike
#
# These principles apply when animating:
# - Particles in flow fields
# - Color transitions over time
# - Interactive elements responding to input
# -------------------------------------------------

py5.run_sketch()
