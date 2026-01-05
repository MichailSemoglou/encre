# Encre: Renoir Integration Guide

How to use data and palettes from the `renoir` course in your Encre/Processing.py sketches.

## Overview

The `renoir` package provides analytical tools for studying art through color. This course extends that analysis into **generative output** using Processing.py. This guide explains how to bridge the two environments.

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                        PYTHON ENVIRONMENT                        │
│                                                                 │
│   renoir (analysis)  ──►  JSON export  ──►  assets/palettes/   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     PROCESSING.PY ENVIRONMENT                   │
│                                                                 │
│   Load JSON  ──►  Convert to colors  ──►  Generative output    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Step 1: Export Data from Renoir

### Using the Palette Exporter Utility

```bash
cd utils/
python palette_exporter.py --artist claude-monet --output ../assets/palettes/monet.json
```

### Programmatic Export

```python
from renoir import ArtistAnalyzer
from renoir.color import ColorExtractor, ColorNamer
import json

# Extract palette
analyzer = ArtistAnalyzer()
extractor = ColorExtractor()
namer = ColorNamer(vocabulary="artist")

works = analyzer.extract_artist_works('claude-monet', limit=10)
colors = extractor.extract_dominant_colors(works[0]['image'], n_colors=5)

# Prepare data for Processing
palette_data = {
    'artist': 'claude-monet',
    'colors': [list(c) for c in colors],
    'named_colors': []
}

for c in colors:
    name_info = namer.name(tuple(c), return_metadata=True)
    palette_data['named_colors'].append({
        'rgb': list(c),
        'hex': name_info['hex'],
        'name': name_info['name'],
        'family': name_info['family']
    })

# Save for Processing
with open('assets/palettes/monet.json', 'w') as f:
    json.dump(palette_data, f, indent=2)
```

### Exporting Multiple Artists

```python
from utils.palette_exporter import export_multiple_artists, IMPRESSIONISTS

export_multiple_artists(
    IMPRESSIONISTS,
    'assets/palettes/',
    n_colors=5,
    n_works=10
)
```

## Step 2: Load Data in Processing.py

### Basic Palette Loading

```python
import json

palette = []

def setup():
    size(800, 600)
    global palette

    # Load palette from JSON
    with open('../../assets/palettes/monet.json') as f:
        data = json.load(f)

    # Convert to Processing colors
    palette = [color(c[0], c[1], c[2]) for c in data['colors']]

def draw():
    background(palette[0])

    for i, c in enumerate(palette):
        fill(c)
        rect(50 + i * 100, 250, 80, 80)
```

### Loading with Color Names

```python
import json

palette = []
color_names = []

def setup():
    size(800, 600)
    global palette, color_names

    with open('../../assets/palettes/monet.json') as f:
        data = json.load(f)

    for c in data['named_colors']:
        palette.append(color(c['rgb'][0], c['rgb'][1], c['rgb'][2]))
        color_names.append(c['name'])

def draw():
    background(255)
    textSize(14)

    for i, (c, name) in enumerate(zip(palette, color_names)):
        fill(c)
        rect(50 + i * 120, 250, 100, 100)

        fill(0)
        text(name, 50 + i * 120, 370)
```

## Step 3: Use Palettes Generatively

### Random Color Selection

```python
import json
from random import choice

palette = []

def setup():
    size(800, 600)
    global palette
    with open('../../assets/palettes/vangogh.json') as f:
        data = json.load(f)
    palette = [color(c[0], c[1], c[2]) for c in data['colors']]
    noStroke()

def draw():
    fill(choice(palette), 50)  # Random color, semi-transparent
    ellipse(random(width), random(height), 50, 50)
```

### Weighted Color Selection

Use color prominence (from k-means cluster sizes) for weighted selection:

```python
import json

palette = []
weights = []

def setup():
    size(800, 600)
    global palette, weights

    with open('../../assets/palettes/monet.json') as f:
        data = json.load(f)

    palette = [color(c[0], c[1], c[2]) for c in data['colors']]

    # If weights are provided in JSON
    weights = data.get('weights', [1] * len(palette))

def weightedChoice():
    """Select color based on weights."""
    total = sum(weights)
    r = random(total)
    cumulative = 0
    for i, w in enumerate(weights):
        cumulative += w
        if r <= cumulative:
            return palette[i]
    return palette[-1]

def draw():
    fill(weightedChoice(), 100)
    ellipse(random(width), random(height), 30, 30)
```

### Color Interpolation

Create smooth gradients between palette colors:

```python
import json

palette = []

def setup():
    size(800, 600)
    global palette
    with open('../../assets/palettes/monet.json') as f:
        data = json.load(f)
    palette = [color(c[0], c[1], c[2]) for c in data['colors']]

def draw():
    background(255)

    # Gradient between first two colors
    for x in range(width):
        t = map(x, 0, width, 0, 1)
        c = lerpColor(palette[0], palette[1], t)
        stroke(c)
        line(x, 0, x, height)
```

### Multi-Palette Blending

Interpolate between two artists' palettes:

```python
import json

palette1 = []
palette2 = []
blend_amount = 0.5

def setup():
    size(800, 600)
    global palette1, palette2

    with open('../../assets/palettes/monet.json') as f:
        data = json.load(f)
    palette1 = [color(c[0], c[1], c[2]) for c in data['colors']]

    with open('../../assets/palettes/vangogh.json') as f:
        data = json.load(f)
    palette2 = [color(c[0], c[1], c[2]) for c in data['colors']]

def draw():
    global blend_amount
    background(255)

    # Blend palettes based on mouse position
    blend_amount = map(mouseX, 0, width, 0, 1)

    for i in range(min(len(palette1), len(palette2))):
        blended = lerpColor(palette1[i], palette2[i], blend_amount)
        fill(blended)
        rect(50 + i * 120, 250, 100, 100)
```

## Available Export Types

### 1. Artist Palette (`palette_exporter.py`)

Basic color palette with optional names.

```json
{
  "artist": "claude-monet",
  "colors": [[142, 178, 197], [89, 112, 95], ...],
  "named_colors": [
    {"rgb": [142, 178, 197], "name": "Cerulean Blue", "hex": "#8eb2c5"}
  ]
}
```

### 2. Artist Statistics (`data_bridge.py`)

Comprehensive artist analysis.

```json
{
  "artist_id": "claude-monet",
  "total_works": 1342,
  "genres": {"landscape": 45, "portrait": 12},
  "color_statistics": {
    "average_saturation": 42.5,
    "average_brightness": 68.3,
    "warm_cool_ratio": 0.35
  }
}
```

### 3. Temporal Data (`data_bridge.py`)

Color evolution over time.

```json
{
  "artist_id": "claude-monet",
  "timeline": [
    {"year": 1865, "saturation": 38, "brightness": 55, "palette": [...]},
    {"year": 1870, "saturation": 45, "brightness": 62, "palette": [...]}
  ]
}
```

### 4. Harmony Analysis (`data_bridge.py`)

Color harmony patterns.

```json
{
  "artist_id": "claude-monet",
  "harmony_preferences": {"analogous": 15, "complementary": 8},
  "average_harmony_score": 0.72
}
```

### 5. Movement Comparison (`data_bridge.py`)

Cross-movement analysis.

```json
{
  "Impressionism": {
    "artists": [
      {"id": "claude-monet", "avg_saturation": 42, "palette": [...]}
    ]
  },
  "Expressionism": {
    "artists": [...]
  }
}
```

## Best Practices

### 1. Organize Your Data

```
sketch_folder/
├── sketch.pyde
└── data/
    ├── monet.json
    ├── vangogh.json
    └── impressionists/
        ├── renoir.json
        └── degas.json
```

### 2. Cache Palettes

Load palettes once in `setup()`, not in `draw()`:

```python
# Good
def setup():
    global palette
    palette = loadPalette('data/monet.json')

# Bad - loads every frame!
def draw():
    palette = loadPalette('data/monet.json')
```

### 3. Create Utility Functions

```python
def loadPalette(filename):
    """Load palette from JSON file."""
    with open(filename) as f:
        data = json.load(f)
    return [color(c[0], c[1], c[2]) for c in data['colors']]

def randomFromPalette(pal):
    """Get random color from palette."""
    return pal[int(random(len(pal)))]

def paletteGradient(pal, t):
    """Get color at position t (0-1) along palette gradient."""
    t = constrain(t, 0, 0.999)
    segment = t * (len(pal) - 1)
    i = int(segment)
    local_t = segment - i
    return lerpColor(pal[i], pal[i + 1], local_t)
```

### 4. Handle Missing Data Gracefully

```python
def setup():
    global palette
    try:
        with open('data/monet.json') as f:
            data = json.load(f)
        palette = [color(c[0], c[1], c[2]) for c in data['colors']]
    except:
        print("Could not load palette, using defaults")
        palette = [color(255, 0, 0), color(0, 255, 0), color(0, 0, 255)]
```

## Connecting Concepts

| Renoir Course | Processing Course |
|---------------|-------------------|
| K-means clustering | Palette-driven particle colors |
| HSV color space | `colorMode(HSB)` for natural selection |
| Color temperature | Warm/cool directional mapping |
| Harmony detection | Harmonious generative compositions |
| Artist signatures | Style-specific generative systems |
| Temporal analysis | Animated historical visualizations |

## Example: Complete Integration

```python
"""
Generative Monet
Creates an impressionist-style generative composition
using colors extracted via renoir.
"""
import json

palette = []
particles = []

class Brushstroke:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.col = palette[int(random(len(palette)))]
        self.angle = noise(x * 0.01, y * 0.01) * TWO_PI
        self.length = random(10, 30)
        self.weight = random(2, 6)

    def display(self):
        pushMatrix()
        translate(self.x, self.y)
        rotate(self.angle)
        stroke(self.col, 200)
        strokeWeight(self.weight)
        line(-self.length/2, 0, self.length/2, 0)
        popMatrix()

def setup():
    size(800, 600)
    global palette

    # Load Monet palette from renoir export
    with open('data/monet.json') as f:
        data = json.load(f)
    palette = [color(c[0], c[1], c[2]) for c in data['colors']]

    background(palette[0])  # Base color from palette

def draw():
    # Add brushstrokes following noise field
    for _ in range(5):
        x = random(width)
        y = random(height)
        stroke = Brushstroke(x, y)
        stroke.display()

def keyPressed():
    if key == 's':
        save("monet_generative.png")
    if key == 'c':
        background(palette[0])
```

## Troubleshooting

### "File not found" errors

- Use relative paths from sketch location
- Place JSON files in `data/` subfolder
- Check file permissions

### Colors look wrong

- Ensure `colorMode(RGB, 255)` is set
- Check JSON format: `[r, g, b]` not `"#hex"`
- Verify color values are 0-255

### Performance issues

- Load data in `setup()`, not `draw()`
- Limit particle counts
- Use `noLoop()` for static images

## Further Resources

- [Renoir Documentation](https://github.com/MichailSemoglou/renoir)
- [Processing.py Reference](https://py.processing.org/reference/)
- [Color Theory Review](../lessons/02_color_systems/)
