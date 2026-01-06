# Encre: Generative Art with Processing.py

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18160393.svg)](https://doi.org/10.5281/zenodo.18160393)

_Encre_ (French for "ink") is a 17-lesson intermediate/advanced course in creative coding and generative art using Processing.py (Python mode). This course builds upon the color analysis foundations from the [renoir](https://github.com/MichailSemoglou/renoir) course, transforming analytical skills into generative visual outputs.

## Prerequisites

- Completion of the **Color Analysis with Renoir** course (or equivalent)
- Familiarity with Python programming
- Basic understanding of color theory (RGB, HSV, color harmonies)
- Understanding of data structures (lists, dictionaries, classes)

## Course Overview

This course bridges **analytical** and **generative** approaches to computational art. Students will learn to:

1. Transform color palettes extracted from art history into dynamic visual compositions
2. Create interactive visualizations that respond to user input
3. Build generative systems inspired by artistic movements
4. Develop a personal creative coding practice grounded in art historical precedent

## Learning Outcomes

By the end of this course, students will be able to:

- Write Processing.py sketches using shapes, color, and animation
- Implement particle systems, flow fields, and emergent behaviors
- Create interactive artworks responding to mouse, keyboard, and external data
- Apply color theory computationally (harmonies, gradients, palettes)
- Generate artwork inspired by specific artists or movements
- Export high-resolution images and video for exhibition/portfolio
- Integrate external data sources (including renoir) into generative systems

## Software Requirements

- [Processing 4.x](https://processing.org/download) with Python Mode installed
- Python 3.8+ (for renoir integration utilities)
- renoir-wikiart package (`pip install renoir-wikiart`)

### Installing Python Mode in Processing

1. Open Processing
2. Click the mode selector (top-right, says "Java")
3. Click "Add Mode..."
4. Search for "Python" and install "Python Mode for Processing 4"

## Curriculum Structure

### Module 1: Foundations (Lessons 1-4)

Building blocks of creative coding in Processing.py

| Lesson | Title                    | Topics                                                                 |
| ------ | ------------------------ | ---------------------------------------------------------------------- |
| 01     | **Hello Processing.py**  | Setup, coordinate system, basic shapes, colors, `setup()` and `draw()` |
| 02     | **Color Systems**        | RGB/HSV in Processing, `colorMode()`, transparency, blending modes     |
| 03     | **Motion and Animation** | Variables, frame-based animation, easing, oscillation, noise           |
| 04     | **Interactivity**        | Mouse and keyboard input, responsive compositions, state machines      |

### Module 2: Generative Systems (Lessons 5-8)

Core techniques for creating emergent visual complexity

| Lesson | Title                    | Topics                                                         |
| ------ | ------------------------ | -------------------------------------------------------------- |
| 05     | **Randomness and Noise** | `random()`, Perlin noise, controlled chaos, organic movement   |
| 06     | **Particle Systems**     | Object-oriented particles, forces, lifespan, trails            |
| 07     | **Flow Fields**          | Vector fields, steering behaviors, flocking, emergent patterns |
| 08     | **Recursive Structures** | Fractals, L-systems, recursive drawing, self-similarity        |

### Module 3: Art-Historical Integration (Lessons 9-12)

Connecting generative techniques to art historical precedent via renoir

| Lesson | Title                         | Topics                                                                    |
| ------ | ----------------------------- | ------------------------------------------------------------------------- |
| 09     | **Palette-Driven Generation** | Loading renoir palettes, color interpolation, weighted selection          |
| 10     | **Movement Aesthetics**       | Impressionist brushstrokes, Expressionist distortion, Abstract geometries |
| 11     | **Artist Style Transfer**     | Recreating artist color signatures, genre-specific compositions           |
| 12     | **Data-Driven Art**           | Visualizing WikiArt metadata, temporal patterns, comparative visuals      |

### Module 4: Advanced Techniques (Lessons 13-16)

Professional-level creative coding skills

| Lesson | Title                     | Topics                                                             |
| ------ | ------------------------- | ------------------------------------------------------------------ |
| 13     | **Image Processing**      | Pixel manipulation, filters, image-based color extraction          |
| 14     | **Typography and Text**   | Generative typography, text as visual element, concrete poetry     |
| 15     | **Sound and Music**       | Audio-reactive visuals, frequency analysis, rhythm-based animation |
| 16     | **Export and Production** | High-res export, video recording, print preparation, exhibition    |

### Module 5: Capstone (Lesson 17)

| Lesson | Title                | Topics                                                              |
| ------ | -------------------- | ------------------------------------------------------------------- |
| 17     | **Capstone Project** | Complete generative art series inspired by a chosen artist/movement |

## Directory Structure

```
encre/
├── README.md                 # This file
├── lessons/                  # Lesson materials and starter code
│   ├── 01_hello_processing/
│   ├── 02_color_systems/
│   ├── ...
│   └── 17_capstone/
├── examples/                 # Complete example sketches
├── assets/                   # Shared resources
│   ├── palettes/             # JSON palettes exported from renoir
│   └── images/               # Reference images
├── utils/                    # Python utilities for renoir integration
│   ├── palette_exporter.py   # Export renoir palettes for Processing
│   └── data_bridge.py        # Bridge between renoir and Processing
└── docs/                     # Additional documentation
    ├── processing_cheatsheet.md
    └── renoir_integration.md
```

## Integration with Renoir

This course extends the analytical work from the renoir course into generative outputs:

### From Analysis to Generation

| Renoir Course           | →   | Encre Course                                |
| ----------------------- | --- | ------------------------------------------- |
| Extract artist palettes | →   | Generate compositions using those palettes  |
| Analyze color harmonies | →   | Create dynamic harmony-based animations     |
| Classify art movements  | →   | Develop movement-specific generative styles |
| Track artist evolution  | →   | Animate temporal changes in color/style     |
| Color naming            | →   | Typography with evocative color names       |

### Data Pipeline

```python
# In Python (using renoir)
from renoir import ArtistAnalyzer
from renoir.color import ColorExtractor

analyzer = ArtistAnalyzer()
works = analyzer.extract_artist_works('claude-monet', limit=10)
extractor = ColorExtractor()
palette = extractor.extract_dominant_colors(works[0]['image'], n_colors=5)

# Export for Processing
import json
with open('assets/palettes/monet.json', 'w') as f:
    json.dump({'colors': [list(c) for c in palette]}, f)
```

```python
# In Processing.py
import json

def setup():
    size(800, 600)
    with open('../../assets/palettes/monet.json') as f:
        data = json.load(f)
    global palette
    palette = [color(c[0], c[1], c[2]) for c in data['colors']]

def draw():
    background(palette[0])
    fill(palette[1])
    ellipse(mouseX, mouseY, 50, 50)
```

## Assessment

### Weekly Exercises (40%)

Each lesson includes coding exercises that build toward the capstone.

### Midterm Project (20%)

Lessons 1-8: Create an interactive generative sketch demonstrating mastery of foundational techniques.

### Capstone Project (40%)

Lesson 17: Develop a cohesive series of 3-5 generative artworks inspired by a chosen artist or movement, accompanied by an artist statement connecting the work to art historical precedent.

## Resources

### Essential Reading

- _Generative Design_ by Hartmut Bohnacker et al.
- _The Nature of Code_ by Daniel Shiffman (free online)
- _Processing: A Programming Handbook_ by Casey Reas & Ben Fry

### Online Resources

- [Processing.py Reference](https://py.processing.org/reference/)
- [The Coding Train](https://thecodingtrain.com/) (YouTube)
- [OpenProcessing](https://openprocessing.org/) (Community gallery)

## Author

**Michail Semoglou**<br>
College of Design and Innovation, Tongji University<br>
m.semoglou@tongji.edu.cn

## License

MIT License - Educational materials may be freely adapted with attribution.

## Acknowledgments

- Processing Foundation for the Processing environment
- WikiArt dataset creators
- Students whose feedback shaped both this course and its prerequisite
