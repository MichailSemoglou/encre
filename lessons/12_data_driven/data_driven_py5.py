"""
Lesson 12: Data-Driven Art (py5 version)
========================================

Create generative visualizations from renoir
statistical data exports.

Learning Objectives:
- Load and parse JSON data
- Map data to visual properties
- Create data-driven compositions
- Visualize color statistics

Run with: python data_driven_py5.py
"""

import py5

# Simulated artist data (from renoir exports)
artist_data = {}
current_view = 0
views = ["Timeline", "Comparison", "Harmony", "Temperature"]


def setup():
    py5.size(900, 600)
    load_artist_data()

    print("Lesson 12: Data-Driven Art")
    print("\nControls:")
    print("  Press 1-4 to switch views")
    print("  Press 's' to save image")


def load_artist_data():
    """Load or simulate artist data from renoir exports."""
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
    py5.background(250)

    if current_view == 0:
        draw_timeline()
    elif current_view == 1:
        draw_comparison()
    elif current_view == 2:
        draw_harmony()
    elif current_view == 3:
        draw_temperature()

    draw_title()


def draw_title():
    """Draw view title."""
    py5.fill(0)
    py5.text_size(18)
    py5.text(f"Data-Driven Art: {views[current_view]}", 30, 35)

    py5.text_size(11)
    py5.fill(100)
    py5.text("Press 1-4 to switch views", 30, 55)


def draw_timeline():
    """Visualize color evolution over time."""
    margin = 80
    graph_height = 400

    # Draw axes
    py5.stroke(150)
    py5.stroke_weight(1)
    py5.line(margin, py5.height - margin, py5.width - margin, py5.height - margin)
    py5.line(margin, py5.height - margin, margin, margin + 50)

    # Labels
    py5.fill(100)
    py5.text_size(10)
    py5.text("Year", py5.width/2, py5.height - 30)

    py5.push_matrix()
    py5.translate(25, py5.height/2)
    py5.rotate(-py5.HALF_PI)
    py5.text("Saturation / Brightness", 0, 0)
    py5.pop_matrix()

    # Draw data for each artist
    artists = ["monet", "vangogh", "renoir"]
    colors = [py5.color(66, 133, 244), py5.color(219, 68, 55), py5.color(15, 157, 88)]

    for idx, artist_id in enumerate(artists):
        data = artist_data[artist_id]
        timeline = data["timeline"]

        min_year = min([d["year"] for d in timeline])
        max_year = max([d["year"] for d in timeline])

        py5.stroke(colors[idx])
        py5.stroke_weight(2)
        py5.no_fill()
        py5.begin_shape()
        for point in timeline:
            x = py5.remap(point["year"], min_year, max_year, margin + 20, py5.width - margin - 20)
            y = py5.remap(point["saturation"], 0, 100, py5.height - margin, margin + 80)
            py5.vertex(x, y)
        py5.end_shape()

        # Legend
        py5.fill(colors[idx])
        py5.no_stroke()
        py5.rect(py5.width - 180, 80 + idx * 25, 15, 15)
        py5.fill(0)
        py5.text_size(11)
        py5.text(data["name"], py5.width - 160, 92 + idx * 25)

    # Scale labels
    py5.fill(100)
    py5.text_size(9)
    for i in range(0, 101, 25):
        y = py5.remap(i, 0, 100, py5.height - margin, margin + 80)
        py5.text(f"{i}%", margin - 30, y + 3)


def draw_comparison():
    """Bar chart comparing artist statistics."""
    margin = 100
    bar_width = 80
    spacing = 30

    artists = ["monet", "vangogh", "renoir"]
    colors_list = [py5.color(66, 133, 244), py5.color(219, 68, 55), py5.color(15, 157, 88)]

    metrics = ["avg_saturation", "avg_brightness"]
    metric_names = ["Avg Saturation", "Avg Brightness"]

    for m_idx, metric in enumerate(metrics):
        base_x = margin + m_idx * 350

        py5.fill(0)
        py5.text_size(14)
        py5.text(metric_names[m_idx], base_x, 100)

        for a_idx, artist_id in enumerate(artists):
            data = artist_data[artist_id]
            value = data["color_stats"][metric]

            x = base_x + a_idx * (bar_width + spacing)
            bar_height = py5.remap(value, 0, 100, 0, 300)
            y = py5.height - margin - bar_height

            py5.fill(colors_list[a_idx])
            py5.no_stroke()
            py5.rect(x, y, bar_width, bar_height, 5, 5, 0, 0)

            py5.fill(0)
            py5.text_size(12)
            py5.text(f"{int(value)}%", x + bar_width/2 - 15, y - 10)

            py5.text_size(10)
            py5.push_matrix()
            py5.translate(x + bar_width/2, py5.height - margin + 20)
            py5.rotate(py5.HALF_PI/2)
            py5.text(data["name"].split()[0], 0, 0)
            py5.pop_matrix()


def draw_harmony():
    """Pie charts showing harmony preferences."""
    artists = ["monet", "vangogh", "renoir"]
    harmony_colors = {
        "analogous": py5.color(100, 180, 100),
        "complementary": py5.color(200, 100, 100),
        "triadic": py5.color(100, 100, 200),
        "split": py5.color(180, 180, 100)
    }

    for idx, artist_id in enumerate(artists):
        data = artist_data[artist_id]
        harmonies = data["harmonies"]

        cx = 180 + idx * 260
        cy = 300
        radius = 100

        start_angle = 0
        for harmony, value in harmonies.items():
            angle = py5.remap(value, 0, 100, 0, py5.TWO_PI)
            py5.fill(harmony_colors[harmony])
            py5.no_stroke()
            py5.arc(cx, cy, radius * 2, radius * 2, start_angle, start_angle + angle, py5.PIE)
            start_angle += angle

        py5.fill(0)
        py5.text_size(14)
        py5.text_align(py5.CENTER)
        py5.text(data["name"].split()[0], cx, cy + radius + 30)

    py5.text_align(py5.LEFT)

    # Legend
    legend_y = 480
    legend_x = 100
    for i, (harmony, col) in enumerate(harmony_colors.items()):
        py5.fill(col)
        py5.no_stroke()
        py5.rect(legend_x + i * 150, legend_y, 15, 15)
        py5.fill(0)
        py5.text_size(11)
        py5.text(harmony.capitalize(), legend_x + 20 + i * 150, legend_y + 12)


def draw_temperature():
    """Warm/cool temperature visualization."""
    margin = 100

    artists = ["monet", "vangogh", "renoir"]

    for idx, artist_id in enumerate(artists):
        data = artist_data[artist_id]
        ratio = data["color_stats"]["warm_cool_ratio"]

        y = 150 + idx * 130
        bar_width = py5.width - 2 * margin

        py5.stroke(200)
        py5.stroke_weight(1)
        py5.no_fill()
        py5.rect(margin, y, bar_width, 40, 5)

        py5.fill(100, 150, 220)
        py5.no_stroke()
        py5.rect(margin, y, bar_width * (1 - ratio), 40, 5, 0, 0, 5)

        py5.fill(220, 150, 100)
        py5.rect(margin + bar_width * (1 - ratio), y, bar_width * ratio, 40, 0, 5, 5, 0)

        py5.fill(0)
        py5.text_size(14)
        py5.text(data["name"], margin, y - 10)

        py5.text_size(11)
        py5.fill(255)
        py5.text(f"Cool: {int((1 - ratio) * 100)}%", margin + 10, y + 25)
        py5.text(f"Warm: {int(ratio * 100)}%", margin + bar_width - 80, y + 25)

    py5.fill(100)
    py5.text_size(12)
    py5.text("Color Temperature Distribution", margin, py5.height - 60)
    py5.text("Based on hue analysis from renoir", margin, py5.height - 40)


def key_pressed():
    global current_view

    if py5.key == '1':
        current_view = 0
    elif py5.key == '2':
        current_view = 1
    elif py5.key == '3':
        current_view = 2
    elif py5.key == '4':
        current_view = 3
    elif py5.key == 's':
        filename = f"datadriven_{py5.frame_count}.png"
        py5.save(filename)
        print(f"Saved: {filename}")


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
# -------------------------------------------------

py5.run_sketch()
