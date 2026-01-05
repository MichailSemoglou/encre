"""
Lesson 01: Hello Processing.py
==============================

This is your first Processing.py sketch!
It demonstrates the basic structure and drawing functions.

Learning Objectives:
- Understand setup() and draw()
- Draw basic shapes
- Apply colors

Run this sketch in Processing with Python Mode enabled.
"""

def setup():
    """
    setup() runs once when the sketch starts.
    Use it to set canvas size and initial settings.
    """
    size(800, 600)  # Create an 800x600 pixel canvas
    background(240)  # Light gray background
    print("Hello Processing.py!")
    print("Canvas size:", width, "x", height)


def draw():
    """
    draw() runs continuously in a loop (~60 times per second).
    This is where animation and interaction happen.
    """
    # For now, we'll draw a static composition
    # (We'll add animation in Lesson 03)

    # Set fill color to blue
    fill(66, 133, 244)
    noStroke()

    # Draw a circle at the center
    ellipse(width/2, height/2, 200, 200)

    # Set fill color to red
    fill(219, 68, 55)

    # Draw a rectangle
    rect(100, 100, 150, 100)

    # Set fill color to yellow
    fill(244, 180, 0)

    # Draw a triangle
    triangle(600, 100, 700, 250, 500, 250)

    # Set fill color to green
    fill(15, 157, 88)

    # Draw a line (lines use stroke, not fill)
    stroke(15, 157, 88)
    strokeWeight(5)
    line(100, 450, 700, 500)

    # Add some text
    fill(0)  # Black text
    textSize(24)
    textAlign(CENTER, CENTER)
    text("Welcome to py5!", width/2, 550)

    # Stop the draw loop since this is static
    noLoop()


# Exercise Ideas:
# ---------------
# 1. Change the colors to your favorites
# 2. Add more shapes (try arc(), quad())
# 3. Create a simple face using ellipses
# 4. Make a Mondrian-inspired composition
#    using only rectangles and primary colors
