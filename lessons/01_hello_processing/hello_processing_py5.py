"""
Lesson 01: Hello Processing.py (py5 version)
=============================================

This is your first py5 sketch!
It demonstrates the basic structure and drawing functions.

Learning Objectives:
- Understand setup() and draw()
- Draw basic shapes
- Apply colors

Run with: python hello_processing_py5.py
"""

import py5


def setup():
    """
    setup() runs once when the sketch starts.
    Use it to set canvas size and initial settings.
    """
    py5.size(800, 600)  # Create an 800x600 pixel canvas
    py5.background(240)  # Light gray background
    print("Hello py5!")
    print(f"Canvas size: {py5.width} x {py5.height}")


def draw():
    """
    draw() runs continuously in a loop (~60 times per second).
    This is where animation and interaction happen.
    """
    # For now, we'll draw a static composition
    # (We'll add animation in Lesson 03)

    # Set fill color to blue
    py5.fill(66, 133, 244)
    py5.no_stroke()

    # Draw a circle at the center
    py5.ellipse(py5.width/2, py5.height/2, 200, 200)

    # Set fill color to red
    py5.fill(219, 68, 55)

    # Draw a rectangle
    py5.rect(100, 100, 150, 100)

    # Set fill color to yellow
    py5.fill(244, 180, 0)

    # Draw a triangle
    py5.triangle(600, 100, 700, 250, 500, 250)

    # Set fill color to green
    py5.fill(15, 157, 88)

    # Draw a line (lines use stroke, not fill)
    py5.stroke(15, 157, 88)
    py5.stroke_weight(5)
    py5.line(100, 450, 700, 500)

    # Add some text
    py5.fill(0)  # Black text
    py5.text_size(24)
    py5.text_align(py5.CENTER, py5.CENTER)
    py5.text("Welcome to py5!", py5.width/2, 550)

    # Stop the draw loop since this is static
    py5.no_loop()


# Exercise Ideas:
# ---------------
# 1. Change the colors to your favorites
# 2. Add more shapes (try py5.arc(), py5.quad())
# 3. Create a simple face using ellipses
# 4. Make a Mondrian-inspired composition
#    using only rectangles and primary colors

py5.run_sketch()
