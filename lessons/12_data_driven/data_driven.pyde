"""
Lesson 12: Data-Driven Art
==========================

Create generative visualizations from renoir
statistical data exports.

Learning Objectives:
- Load and parse JSON data
- Map data to visual properties
- Create data-driven compositions
- Visualize color statistics

Run this sketch in Processing with Python Mode enabled.
"""

import json

# Simulated artist data (from renoir exports)
artist_data = {}
current_view = 0
views = ["Timeline", "Comparison", "Harmony", "Temperature"]


def setup():
    size(900, 600)
    loadArtistData()

    print("Lesson 12: Data-Driven Art")
    print("\nControls:")
    print("  Press 1-4 to switch views")
    print("  Press 's' to save image")


def loadArtistData():
    """Load or simulate artist data from renoir exports."""
    # Simulated data structure (would normally load from JSON)

    artist_data["monet"] = {
        "name": "Claude Monet",
        "total_works": 1342,
        "timeline": [
            {"year": 1865, "saturation": 45, "brightness": 55, "works": 12},
            {"year": 1870, "saturation": 52, "brightness": 58, "works": 28},
            {"year": 1875, "saturation": 58, "brightness": 62, "works": 45},
            {"year": 1880, "saturation": 55, "brightness": 65, "works": 67},
            {"year": 1885, "saturation": 50, "brightness": 68, "works": 82},
            {"year": 1890, "saturation": 48, "brightness": 72, "works": 95},
            {"year": 1900, "saturation": 42, "brightness": 75, "works": 110},
            {"year": 1910, "saturation": 38, "brightness": 78, "works": 85},
        ],
        "color_stats": {
            "avg_saturation": 48,
            "avg_brightness": 67,
            "warm_cool_ratio": 0.42
        },
        "harmonies": {"analogous": 45, "complementary": 25, "triadic": 15, "split": 15}
    }

    artist_data["vangogh"] = {
        "name": "Vincent van Gogh",
        "total_works": 864,
        "timeline": [
            {"year": 1881, "saturation": 30, "brightness": 40, "works": 15},
            {"year": 1883, "saturation": 35, "brightness": 42, "works": 45},
            {"year": 1885, "saturation": 40, "brightness": 45, "works": 85},
            {"year": 1887, "saturation": 65, "brightness": 60, "works": 120},
            {"year": 1888, "saturation": 80, "brightness": 70, "works": 180},
            {"year": 1889, "saturation": 75, "brightness": 65, "works": 150},
            {"year": 1890, "saturation": 70, "brightness": 55, "works": 80},
        ],
        "color_stats": {
            "avg_saturation": 58,
            "avg_brightness": 55,
            "warm_cool_ratio": 0.65
        },
        "harmonies": {"analogous": 30, "complementary": 40, "triadic": 20, "split": 10}
    }

    artist_data["renoir"] = {
        "name": "Pierre-Auguste Renoir",
        "total_works": 4000,
        "timeline": [
            {"year": 1865, "saturation": 50, "brightness": 60, "works": 20},
            {"year": 1870, "saturation": 55, "brightness": 62, "works": 55},
            {"year": 1875, "saturation": 60, "brightness": 65, "works": 120},
            {"year": 1880, "saturation": 58, "brightness": 68, "works": 180},
            {"year": 1885, "saturation": 55, "brightness": 70, "works": 220},
            {"year": 1890, "saturation": 50, "brightness": 72, "works": 280},
            {"year": 1900, "saturation": 48, "brightness": 75, "works": 350},
            {"year": 1910, "saturation": 45, "brightness": 78, "works": 300},
        ],
        "color_stats": {
            "avg_saturation": 53,
            "avg_brightness": 69,
            "warm_cool_ratio": 0.58
        },
        "harmonies": {"analogous": 50, "complementary": 20, "triadic": 18, "split": 12}
    }


def draw():
    background(250)

    if current_view == 0:
        drawTimeline()
    elif current_view == 1:
        drawComparison()
    elif current_view == 2:
        drawHarmony()
    elif current_view == 3:
        drawTemperature()

    drawTitle()


def drawTitle():
    """Draw view title."""
    fill(0)
    textSize(18)
    text("Data-Driven Art: " + views[current_view], 30, 35)

    textSize(11)
    fill(100)
    text("Press 1-4 to switch views", 30, 55)


def drawTimeline():
    """Visualize color evolution over time."""
    margin = 80
    graph_height = 400

    # Draw axes
    stroke(150)
    strokeWeight(1)
    line(margin, height - margin, width - margin, height - margin)  # X axis
    line(margin, height - margin, margin, margin + 50)  # Y axis

    # Labels
    fill(100)
    textSize(10)
    text("Year", width/2, height - 30)

    pushMatrix()
    translate(25, height/2)
    rotate(-HALF_PI)
    text("Saturation / Brightness", 0, 0)
    popMatrix()

    # Draw data for each artist
    artists = ["monet", "vangogh", "renoir"]
    colors = [color(66, 133, 244), color(219, 68, 55), color(15, 157, 88)]

    for idx, artist_id in enumerate(artists):
        data = artist_data[artist_id]
        timeline = data["timeline"]

        # Find year range
        min_year = min([d["year"] for d in timeline])
        max_year = max([d["year"] for d in timeline])

        # Draw saturation line
        stroke(colors[idx])
        strokeWeight(2)
        noFill()
        beginShape()
        for point in timeline:
            x = map(point["year"], min_year, max_year, margin + 20, width - margin - 20)
            y = map(point["saturation"], 0, 100, height - margin, margin + 80)
            vertex(x, y)
        endShape()

        # Legend
        fill(colors[idx])
        noStroke()
        rect(width - 180, 80 + idx * 25, 15, 15)
        fill(0)
        textSize(11)
        text(data["name"], width - 160, 92 + idx * 25)

    # Scale labels
    fill(100)
    textSize(9)
    for i in range(0, 101, 25):
        y = map(i, 0, 100, height - margin, margin + 80)
        text(str(i) + "%", margin - 30, y + 3)


def drawComparison():
    """Bar chart comparing artist statistics."""
    margin = 100
    bar_width = 80
    spacing = 30

    artists = ["monet", "vangogh", "renoir"]
    colors_list = [color(66, 133, 244), color(219, 68, 55), color(15, 157, 88)]

    # Draw bars for each metric
    metrics = ["avg_saturation", "avg_brightness"]
    metric_names = ["Avg Saturation", "Avg Brightness"]

    for m_idx, metric in enumerate(metrics):
        base_x = margin + m_idx * 350

        # Metric label
        fill(0)
        textSize(14)
        text(metric_names[m_idx], base_x, 100)

        for a_idx, artist_id in enumerate(artists):
            data = artist_data[artist_id]
            value = data["color_stats"][metric]

            x = base_x + a_idx * (bar_width + spacing)
            bar_height = map(value, 0, 100, 0, 300)
            y = height - margin - bar_height

            # Bar
            fill(colors_list[a_idx])
            noStroke()
            rect(x, y, bar_width, bar_height, 5, 5, 0, 0)

            # Value label
            fill(0)
            textSize(12)
            text(str(int(value)) + "%", x + bar_width/2 - 15, y - 10)

            # Artist name
            textSize(10)
            pushMatrix()
            translate(x + bar_width/2, height - margin + 20)
            rotate(HALF_PI/2)
            text(data["name"].split()[0], 0, 0)
            popMatrix()


def drawHarmony():
    """Pie charts showing harmony preferences."""
    artists = ["monet", "vangogh", "renoir"]
    harmony_colors = {
        "analogous": color(100, 180, 100),
        "complementary": color(200, 100, 100),
        "triadic": color(100, 100, 200),
        "split": color(180, 180, 100)
    }

    for idx, artist_id in enumerate(artists):
        data = artist_data[artist_id]
        harmonies = data["harmonies"]

        cx = 180 + idx * 260
        cy = 300
        radius = 100

        # Draw pie chart
        start_angle = 0
        for harmony, value in harmonies.items():
            angle = map(value, 0, 100, 0, TWO_PI)
            fill(harmony_colors[harmony])
            noStroke()
            arc(cx, cy, radius * 2, radius * 2, start_angle, start_angle + angle, PIE)
            start_angle += angle

        # Artist name
        fill(0)
        textSize(14)
        textAlign(CENTER)
        text(data["name"].split()[0], cx, cy + radius + 30)

    textAlign(LEFT)

    # Legend
    legend_y = 480
    legend_x = 100
    for i, (harmony, col) in enumerate(harmony_colors.items()):
        fill(col)
        noStroke()
        rect(legend_x + i * 150, legend_y, 15, 15)
        fill(0)
        textSize(11)
        text(harmony.capitalize(), legend_x + 20 + i * 150, legend_y + 12)


def drawTemperature():
    """Warm/cool temperature visualization."""
    margin = 100

    artists = ["monet", "vangogh", "renoir"]

    for idx, artist_id in enumerate(artists):
        data = artist_data[artist_id]
        ratio = data["color_stats"]["warm_cool_ratio"]

        y = 150 + idx * 130
        bar_width = width - 2 * margin

        # Background bar
        stroke(200)
        strokeWeight(1)
        noFill()
        rect(margin, y, bar_width, 40, 5)

        # Cool portion (left)
        fill(100, 150, 220)
        noStroke()
        rect(margin, y, bar_width * (1 - ratio), 40, 5, 0, 0, 5)

        # Warm portion (right)
        fill(220, 150, 100)
        rect(margin + bar_width * (1 - ratio), y, bar_width * ratio, 40, 0, 5, 5, 0)

        # Labels
        fill(0)
        textSize(14)
        text(data["name"], margin, y - 10)

        textSize(11)
        fill(255)
        text("Cool: " + str(int((1 - ratio) * 100)) + "%", margin + 10, y + 25)
        text("Warm: " + str(int(ratio * 100)) + "%", margin + bar_width - 80, y + 25)

    # Legend
    fill(100)
    textSize(12)
    text("Color Temperature Distribution", margin, height - 60)
    text("Based on hue analysis from renoir", margin, height - 40)


def keyPressed():
    global current_view

    if key == '1':
        current_view = 0
    elif key == '2':
        current_view = 1
    elif key == '3':
        current_view = 2
    elif key == '4':
        current_view = 3
    elif key == 's':
        filename = "datadriven_" + str(frameCount) + ".png"
        save(filename)
        print("Saved:", filename)


# -------------------------------------------------
# Data-Driven Art Concepts:
#
# 1. Load renoir exports (JSON)
# 2. Map numerical data to visual properties:
#    - Values -> Heights (bar charts)
#    - Percentages -> Angles (pie charts)
#    - Time -> X position (timelines)
#    - Categories -> Colors
#
# 3. Create meaningful visualizations that
#    reveal patterns in artistic data
#
# Example renoir export structure:
# {
#   "artist_id": "claude-monet",
#   "color_statistics": {
#     "average_saturation": 48.5,
#     "warm_cool_ratio": 0.42
#   },
#   "timeline": [
#     {"year": 1870, "saturation": 52}
#   ]
# }
# -------------------------------------------------
