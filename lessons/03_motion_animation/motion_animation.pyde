"""
Lesson 03: Motion and Animation
===============================

Learn how the draw() loop creates animation,
and explore different motion techniques.

Learning Objectives:
- Understand the animation loop
- Create smooth motion with variables
- Use trigonometry for organic movement
- Apply easing for natural motion

Run this sketch in Processing with Python Mode enabled.
"""

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
    size(800, 600)
    global ease_x, ease_y
    ease_x = width / 2
    ease_y = height / 2
    print("Lesson 03: Motion and Animation")
    print("\nControls:")
    print("  Press 1-4 to switch modes")
    print("  Press 's' to save image")
    print("  Click to set easing target (mode 4)")


def draw():
    background(30)

    # Draw mode indicator
    fill(255)
    textSize(16)
    text("Mode: " + modes[mode], 20, 30)
    text("Press 1-4 to switch", 20, 55)

    if mode == 0:
        drawLinear()
    elif mode == 1:
        drawSineWave()
    elif mode == 2:
        drawCircular()
    elif mode == 3:
        drawEasing()


def drawLinear():
    """Simple linear motion - constant speed."""
    global x

    # Move right at constant speed
    x += 3

    # Wrap around when off screen
    if x > width + 25:
        x = -25

    # Draw moving circle
    fill(66, 133, 244)
    noStroke()
    ellipse(x, height/2, 50, 50)

    # Draw trail
    for i in range(10):
        alpha = map(i, 0, 10, 200, 0)
        fill(66, 133, 244, alpha)
        ellipse(x - i * 15, height/2, 50 - i * 4, 50 - i * 4)

    # Explanation
    fill(255)
    textSize(14)
    text("Linear motion: constant velocity", 20, height - 60)
    text("x += speed (same amount each frame)", 20, height - 40)


def drawSineWave():
    """Sine wave motion - smooth oscillation."""
    global angle

    angle += 0.03

    # Horizontal position based on angle
    x = width / 2
    # Vertical oscillation using sine
    y = height/2 + sin(angle) * 150

    # Secondary ball with different phase
    y2 = height/2 + sin(angle + PI) * 150

    # Draw balls
    fill(219, 68, 55)
    noStroke()
    ellipse(x - 100, y, 50, 50)

    fill(244, 180, 0)
    ellipse(x + 100, y2, 50, 50)

    # Draw sine wave path
    stroke(255, 100)
    strokeWeight(1)
    noFill()
    beginShape()
    for i in range(width):
        wave_y = height/2 + sin(angle + i * 0.02) * 150
        vertex(i, wave_y)
    endShape()

    # Explanation
    noStroke()
    fill(255)
    textSize(14)
    text("Sine wave: smooth oscillation", 20, height - 60)
    text("y = sin(angle) * amplitude", 20, height - 40)


def drawCircular():
    """Circular motion using sin and cos."""
    global angle

    angle += 0.02

    centerX = width / 2
    centerY = height / 2
    radius = 150

    # Calculate position on circle
    x = centerX + cos(angle) * radius
    y = centerY + sin(angle) * radius

    # Second circle with different radius and speed
    x2 = centerX + cos(angle * 2) * 80
    y2 = centerY + sin(angle * 2) * 80

    # Draw orbit paths
    stroke(255, 50)
    strokeWeight(1)
    noFill()
    ellipse(centerX, centerY, radius * 2, radius * 2)
    ellipse(centerX, centerY, 160, 160)

    # Draw center
    fill(100)
    noStroke()
    ellipse(centerX, centerY, 30, 30)

    # Draw orbiting circles
    fill(15, 157, 88)
    ellipse(x, y, 40, 40)

    fill(156, 39, 176)
    ellipse(x2, y2, 25, 25)

    # Draw connecting line
    stroke(255, 100)
    line(centerX, centerY, x, y)

    # Explanation
    noStroke()
    fill(255)
    textSize(14)
    text("Circular motion: sin + cos", 20, height - 60)
    text("x = cos(angle) * r, y = sin(angle) * r", 20, height - 40)


def drawEasing():
    """Easing motion - smooth acceleration/deceleration."""
    global ease_x, ease_y, target_x, target_y

    # Easing formula: move a fraction of remaining distance
    easing = 0.05
    ease_x += (target_x - ease_x) * easing
    ease_y += (target_y - ease_y) * easing

    # Draw target
    stroke(255, 100)
    strokeWeight(1)
    noFill()
    ellipse(target_x, target_y, 60, 60)
    line(target_x - 10, target_y, target_x + 10, target_y)
    line(target_x, target_y - 10, target_x, target_y + 10)

    # Draw easing circle
    fill(0, 188, 212)
    noStroke()
    ellipse(ease_x, ease_y, 50, 50)

    # Draw connection line
    stroke(255, 50)
    line(ease_x, ease_y, target_x, target_y)

    # Explanation
    noStroke()
    fill(255)
    textSize(14)
    text("Easing: smooth acceleration", 20, height - 80)
    text("x += (target - x) * easing", 20, height - 60)
    text("Click anywhere to set new target", 20, height - 40)


def keyPressed():
    global mode

    if key == '1':
        mode = 0
    elif key == '2':
        mode = 1
    elif key == '3':
        mode = 2
    elif key == '4':
        mode = 3
    elif key == 's':
        filename = "motion_" + str(frameCount) + ".png"
        save(filename)
        print("Saved:", filename)


def mousePressed():
    global target_x, target_y
    if mode == 3:  # Easing mode
        target_x = mouseX
        target_y = mouseY


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
