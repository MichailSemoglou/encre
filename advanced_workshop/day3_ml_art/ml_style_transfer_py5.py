"""
Advanced Workshop - Day 3: Machine Learning Art
===============================================

Explore neural style transfer and ML-based image
generation techniques for creative coding.

Prerequisites:
    pip install opencv-python numpy torch torchvision pillow

Learning Objectives:
- Understand neural style transfer concepts
- Apply pre-trained models for artistic effects
- Create real-time ML-enhanced visualizations
- Combine traditional and ML techniques

Note: This lesson uses simplified neural approaches
suitable for real-time processing. Full style transfer
models require more computation.

Run with: python ml_style_transfer_py5.py
"""

import py5
import cv2
import numpy as np
from pathlib import Path

# Try to import torch for neural effects
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("PyTorch not available - using OpenCV-only effects")

# OpenCV setup
cap = None
frame = None

# Neural style parameters
style_strength = 0.5
color_preservation = 0.5

# Pre-computed style kernels (artistic edge detection)
artistic_kernels = {}

# Store original frame colors for preservation
original_colors = None

# Effect mode
mode = 0
modes = [
    "Edge Art",
    "Impressionist",
    "Pointillist",
    "Abstract Expression",
    "Neural Texture",
    "Pop Art"
]

# Animation parameters
t = 0

# Palette (artistic colors)
palette = []


def setup():
    global cap, palette, artistic_kernels

    py5.size(1280, 720)

    # Initialize webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Artistic palette
    palette = [
        py5.color(66, 133, 244),   # Blue
        py5.color(219, 68, 55),    # Red
        py5.color(244, 180, 0),    # Yellow
        py5.color(15, 157, 88),    # Green
        py5.color(156, 39, 176),   # Purple
        py5.color(255, 138, 101),  # Coral
    ]

    # Initialize artistic kernels
    init_artistic_kernels()

    print("=" * 60)
    print("Advanced Workshop Day 3: Machine Learning Art")
    print("=" * 60)
    print(f"\nPyTorch available: {TORCH_AVAILABLE}")
    print("\nControls:")
    print("  1-6: Switch art styles")
    print("  UP/DOWN: Adjust style strength")
    print("  LEFT/RIGHT: Adjust color preservation")
    print("  s: Save artwork")
    print("  q: Quit")
    print("\nStyles:")
    for i, m in enumerate(modes):
        print(f"  {i+1}: {m}")


def preserve_colors(stylized_rgb, original_rgb, amount):
    """
    Preserve original colors in stylized image using LAB color space.

    Args:
        stylized_rgb: The stylized image (RGB, numpy array)
        original_rgb: The original image (RGB, numpy array)
        amount: How much to preserve (0 = full style, 1 = full original colors)

    Returns:
        Color-preserved image (RGB, numpy array)
    """
    if amount <= 0:
        return stylized_rgb

    # Ensure same size
    if stylized_rgb.shape != original_rgb.shape:
        original_rgb = cv2.resize(original_rgb, (stylized_rgb.shape[1], stylized_rgb.shape[0]))

    # Convert to LAB color space
    stylized_lab = cv2.cvtColor(stylized_rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    original_lab = cv2.cvtColor(original_rgb, cv2.COLOR_RGB2LAB).astype(np.float32)

    # Keep luminance from stylized, blend color channels from original
    # L channel (index 0) = luminance/brightness from style
    # A channel (index 1) = green-red from original
    # B channel (index 2) = blue-yellow from original
    result_lab = stylized_lab.copy()
    result_lab[:, :, 1] = stylized_lab[:, :, 1] * (1 - amount) + original_lab[:, :, 1] * amount
    result_lab[:, :, 2] = stylized_lab[:, :, 2] * (1 - amount) + original_lab[:, :, 2] * amount

    # Convert back to RGB
    result_lab = np.clip(result_lab, 0, 255).astype(np.uint8)
    return cv2.cvtColor(result_lab, cv2.COLOR_LAB2RGB)


def init_artistic_kernels():
    """Initialize convolution kernels for artistic effects."""
    global artistic_kernels

    # Emboss kernel
    artistic_kernels['emboss'] = np.array([
        [-2, -1, 0],
        [-1, 1, 1],
        [0, 1, 2]
    ], dtype=np.float32)

    # Sharpen
    artistic_kernels['sharpen'] = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ], dtype=np.float32)

    # Edge detection
    artistic_kernels['edge'] = np.array([
        [-1, -1, -1],
        [-1, 8, -1],
        [-1, -1, -1]
    ], dtype=np.float32)

    # Blur
    artistic_kernels['blur'] = np.ones((5, 5), dtype=np.float32) / 25


def draw():
    global frame, original_colors, t

    t += 0.02

    # Capture frame
    ret, frame = cap.read()
    if not ret:
        py5.background(0)
        py5.fill(255)
        py5.text("No webcam detected", py5.width/2 - 80, py5.height/2)
        return

    # Flip and resize for processing
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (640, 480))

    # Store original colors for preservation
    original_colors = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Apply selected style
    if mode == 0:
        draw_edge_art()
    elif mode == 1:
        draw_impressionist()
    elif mode == 2:
        draw_pointillist()
    elif mode == 3:
        draw_abstract_expression()
    elif mode == 4:
        draw_neural_texture()
    elif mode == 5:
        draw_deep_dream_style()

    # Draw UI
    draw_ui()


def draw_edge_art():
    """Create artistic edge-based visualization."""
    py5.background(250)

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Multi-scale edge detection
    edges1 = cv2.Canny(gray, 50, 150)
    edges2 = cv2.Canny(gray, 100, 200)

    # Blend edges
    edges = cv2.addWeighted(edges1, 0.5, edges2, 0.5, 0)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Scale to canvas
    scale_x = py5.width / 640
    scale_y = py5.height / 480

    # Draw artistic contours
    py5.no_fill()
    for i, contour in enumerate(contours[:200]):  # Limit for performance
        if len(contour) > 10:
            # Color from palette based on contour position
            avg_y = np.mean(contour[:, 0, 1])
            col_idx = int(py5.remap(avg_y, 0, 480, 0, len(palette) - 1))
            col = palette[col_idx]

            py5.stroke(py5.red(col), py5.green(col), py5.blue(col), 150)
            py5.stroke_weight(py5.random(1, 3))

            py5.begin_shape()
            for point in contour[::2]:  # Skip points for artistic effect
                x = point[0][0] * scale_x
                y = point[0][1] * scale_y
                # Add slight noise for hand-drawn effect
                x += py5.random(-2, 2)
                y += py5.random(-2, 2)
                py5.curve_vertex(x, y)
            py5.end_shape()


def draw_impressionist():
    """Create impressionist brushstroke effect."""
    # Only partially clear for trailing effect
    py5.no_stroke()
    py5.fill(245, 240, 230, 30)
    py5.rect(0, 0, py5.width, py5.height)

    # Convert frame to RGB and apply color preservation
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Apply color preservation - blend stylized palette with original colors
    if color_preservation > 0:
        # Create a slightly desaturated/shifted version as "style"
        hsv = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
        # Impressionist style: warmer, more saturated
        hsv[:, :, 0] = (hsv[:, :, 0] + 10) % 180  # Shift hue warm
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.2, 0, 255)  # Boost saturation
        stylized = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
        frame_rgb = preserve_colors(stylized, original_colors, color_preservation)

    # Scale factors
    scale_x = py5.width / 640
    scale_y = py5.height / 480

    # Draw brushstrokes
    num_strokes = 200
    for _ in range(num_strokes):
        # Random position
        fx = int(py5.random(640))
        fy = int(py5.random(480))

        # Get color from color-preserved frame
        r, g, b = frame_rgb[fy, fx]

        # Calculate gradient direction for stroke angle
        if fx > 0 and fx < 639 and fy > 0 and fy < 479:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            dx = float(gray[fy, fx+1]) - float(gray[fy, fx-1])
            dy = float(gray[fy+1, fx]) - float(gray[fy-1, fx])
            angle = np.arctan2(dy, dx) + np.pi/2
        else:
            angle = py5.random(py5.TWO_PI)

        # Canvas coordinates
        x = fx * scale_x
        y = fy * scale_y

        # Brushstroke
        stroke_length = py5.random(15, 40) * style_strength
        stroke_width = py5.random(3, 10)

        py5.push_matrix()
        py5.translate(x, y)
        py5.rotate(angle)

        # Slight color variation
        r_var = py5.constrain(r + py5.random(-20, 20), 0, 255)
        g_var = py5.constrain(g + py5.random(-20, 20), 0, 255)
        b_var = py5.constrain(b + py5.random(-20, 20), 0, 255)

        py5.fill(r_var, g_var, b_var, 200)
        py5.no_stroke()
        py5.ellipse(0, 0, stroke_length, stroke_width)

        py5.pop_matrix()


def draw_pointillist():
    """Create Seurat-style pointillist effect."""
    py5.background(240, 235, 225)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Apply color preservation
    if color_preservation > 0:
        # Pointillist style: higher contrast, purer colors
        hsv = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.4, 0, 255)  # More saturated
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.1, 0, 255)  # Brighter
        stylized = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
        frame_rgb = preserve_colors(stylized, original_colors, color_preservation)

    scale_x = py5.width / 640
    scale_y = py5.height / 480

    # Grid of dots
    dot_spacing = int(8 / style_strength) if style_strength > 0 else 8
    dot_spacing = max(4, min(15, dot_spacing))

    py5.no_stroke()

    for fy in range(0, 480, dot_spacing):
        for fx in range(0, 640, dot_spacing):
            r, g, b = frame_rgb[fy, fx]

            x = fx * scale_x
            y = fy * scale_y

            # Primary color dot
            dot_size = py5.random(dot_spacing * 0.5, dot_spacing * 0.9)
            py5.fill(r, g, b)
            py5.ellipse(x, y, dot_size, dot_size)

            # Add complementary color dots (pointillist technique)
            if py5.random(1) < 0.3:
                # Complementary offset
                offset = dot_spacing * 0.3
                comp_r = 255 - r
                comp_g = 255 - g
                comp_b = 255 - b
                py5.fill(comp_r, comp_g, comp_b, 100)
                py5.ellipse(x + offset, y + offset, dot_size * 0.5, dot_size * 0.5)


def draw_abstract_expression():
    """Create abstract expressionist visualization - action painting style."""
    # Dark canvas with slow fade for layering effect
    py5.no_stroke()
    py5.fill(15, 12, 20, 8)
    py5.rect(0, 0, py5.width, py5.height)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Apply color preservation with bold, saturated colors
    if color_preservation > 0:
        hsv = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.6, 0, 255)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.3, 0, 255)
        stylized = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
        frame_rgb = preserve_colors(stylized, original_colors, color_preservation)

    scale_x = py5.width / 640
    scale_y = py5.height / 480

    # Bold color blocks - large gestural areas (like Rothko/de Kooning)
    block_count = int(5 + 10 * style_strength)
    for _ in range(block_count):
        fx = int(py5.random(640))
        fy = int(py5.random(480))
        r, g, b = frame_rgb[fy, fx]

        x = fx * scale_x
        y = fy * scale_y

        # Large, bold rectangular strokes
        w = py5.random(100, 300) * style_strength
        h = py5.random(50, 150) * style_strength
        angle = py5.random(-0.3, 0.3)

        py5.push_matrix()
        py5.translate(x, y)
        py5.rotate(angle)

        # Layered color with rough edges
        py5.no_stroke()
        py5.fill(r, g, b, 40)
        py5.rect(-w/2, -h/2, w, h)

        # Rougher inner stroke
        py5.fill(r, g, b, 80)
        py5.rect(-w/3, -h/3, w*0.6, h*0.6)
        py5.pop_matrix()

    # Dripping paint effect
    drip_count = int(15 * style_strength)
    for _ in range(drip_count):
        fx = int(py5.random(640))
        fy = int(py5.random(480))
        r, g, b = frame_rgb[fy, fx]

        x = fx * scale_x
        start_y = fy * scale_y

        # Drip length varies
        drip_length = py5.random(50, 200) * style_strength
        drip_width = py5.random(2, 8)

        py5.stroke(r, g, b, 200)
        py5.stroke_weight(drip_width)

        # Wavy drip path
        py5.no_fill()
        py5.begin_shape()
        for dy in range(0, int(drip_length), 5):
            wobble = py5.sin(dy * 0.1 + t) * (drip_width * 2)
            py5.vertex(x + wobble, start_y + dy)
        py5.end_shape()

        # Drip blob at end
        py5.no_stroke()
        py5.fill(r, g, b, 180)
        py5.ellipse(x, start_y + drip_length, drip_width * 2, drip_width * 3)

    # Energetic splatter/splash marks (Pollock-style)
    splatter_count = int(20 * style_strength)
    for _ in range(splatter_count):
        fx = int(py5.random(640))
        fy = int(py5.random(480))
        r, g, b = frame_rgb[fy, fx]

        x = fx * scale_x
        y = fy * scale_y

        # Central splash
        py5.no_stroke()
        py5.fill(r, g, b, 200)
        splash_size = py5.random(5, 20)
        py5.ellipse(x, y, splash_size, splash_size * py5.random(0.5, 1.5))

        # Radiating splatter droplets
        num_drops = int(py5.random(3, 8))
        for _ in range(num_drops):
            angle = py5.random(py5.TWO_PI)
            dist = py5.random(10, 50)
            drop_x = x + py5.cos(angle) * dist
            drop_y = y + py5.sin(angle) * dist
            drop_size = py5.random(2, 8)
            py5.fill(r, g, b, 150)
            py5.ellipse(drop_x, drop_y, drop_size, drop_size)

    # Bold gestural lines across canvas
    if py5.frame_count % 5 == 0:
        fx = int(py5.random(640))
        fy = int(py5.random(480))
        r, g, b = frame_rgb[fy, fx]

        py5.stroke(r, g, b, 120)
        py5.stroke_weight(py5.random(3, 15))
        py5.no_fill()

        # Sweeping gesture
        py5.begin_shape()
        start_x = py5.random(py5.width)
        start_y = py5.random(py5.height)
        for i in range(10):
            px = start_x + py5.random(-50, 50) + i * py5.random(20, 60)
            py_coord = start_y + py5.sin(i * 0.5) * py5.random(50, 150)
            py5.curve_vertex(px, py_coord)
        py5.end_shape()


def draw_neural_texture():
    """Create neural network-inspired texture synthesis."""
    py5.background(30)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Apply color preservation
    if color_preservation > 0:
        # Neural texture style: slightly cooler, more digital look
        hsv = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
        hsv[:, :, 0] = (hsv[:, :, 0] - 5) % 180  # Shift hue cool
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 0.9, 0, 255)  # Slightly desaturated
        stylized = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
        frame_rgb = preserve_colors(stylized, original_colors, color_preservation)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply artistic kernels
    embossed = cv2.filter2D(gray, -1, artistic_kernels['emboss'])
    edges = cv2.filter2D(gray, -1, artistic_kernels['edge'])

    # Combine layers
    combined = cv2.addWeighted(embossed, 0.5, edges, 0.5 * style_strength, 0)

    # Color mapping based on intensity
    scale_x = py5.width / 640
    scale_y = py5.height / 480

    # Draw texture as colored blocks
    block_size = 10

    for fy in range(0, 480, block_size):
        for fx in range(0, 640, block_size):
            # Get local statistics
            region = combined[fy:fy+block_size, fx:fx+block_size]
            mean_val = np.mean(region)
            std_val = np.std(region)

            x = fx * scale_x
            y = fy * scale_y

            # Map to color from color-preserved frame
            r, g, b = frame_rgb[fy, fx]

            # Texture-based alpha
            alpha = py5.remap(std_val, 0, 50, 50, 255)

            py5.fill(r, g, b, alpha)
            py5.no_stroke()

            # Shape based on local texture
            w = block_size * scale_x
            h = block_size * scale_y

            if std_val > 30:  # High texture - use triangles
                py5.triangle(x, y + h, x + w/2, y, x + w, y + h)
            elif std_val > 15:  # Medium - use ellipses
                py5.ellipse(x + w/2, y + h/2, w, h)
            else:  # Low - use rectangles
                py5.rect(x, y, w, h)

    # Overlay edge highlights
    py5.stroke(255, 50)
    py5.stroke_weight(1)
    edges_thresh = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY)[1]
    contours, _ = cv2.findContours(edges_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours[:100]:
        if len(contour) > 5:
            py5.begin_shape()
            for point in contour[::2]:
                px = point[0][0] * scale_x
                py_val = point[0][1] * scale_y
                py5.vertex(px, py_val)
            py5.end_shape()


def draw_deep_dream_style():
    """Create Andy Warhol-inspired pop art with posterization."""
    # Get base image
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # === POSTERIZATION ===
    # Reduce number of colors for that screen-print look
    num_levels = max(2, int(3 + 5 * (1 - style_strength)))  # 2-8 levels
    
    # Posterize each channel
    posterized = frame_rgb.copy().astype(np.float32)
    for i in range(3):
        channel = posterized[:, :, i]
        # Quantize to discrete levels
        channel = np.floor(channel / 255.0 * num_levels) / num_levels * 255.0
        posterized[:, :, i] = channel
    posterized = posterized.astype(np.uint8)

    # === HIGH CONTRAST ===
    # Boost contrast for that bold pop art look
    lab = cv2.cvtColor(posterized, cv2.COLOR_RGB2LAB).astype(np.float32)
    lab[:, :, 0] = np.clip((lab[:, :, 0] - 128) * 1.5 + 128, 0, 255)  # L channel contrast
    posterized = cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2RGB)

    # === WARHOL COLOR SCHEMES ===
    # Define bold pop art color palettes (Warhol-inspired)
    warhol_palettes = [
        # Marilyn Monroe inspired
        [(255, 20, 147), (255, 215, 0), (0, 191, 255), (50, 50, 50)],  # Hot pink, gold, cyan, black
        # Campbell's Soup inspired  
        [(220, 20, 60), (255, 255, 255), (255, 215, 0), (139, 69, 19)],  # Red, white, gold, brown
        # Electric colors
        [(255, 0, 255), (0, 255, 255), (255, 255, 0), (0, 0, 0)],  # Magenta, cyan, yellow, black
        # Mao series inspired
        [(255, 140, 0), (138, 43, 226), (50, 205, 50), (255, 20, 147)],  # Orange, purple, green, pink
    ]
    
    # Select palette based on time for variety (or could use frame position)
    palette_idx = int(t * 0.5) % len(warhol_palettes)
    current_palette = warhol_palettes[palette_idx]

    # === COLOR REMAPPING ===
    # Map posterized colors to Warhol palette based on brightness
    gray = cv2.cvtColor(posterized, cv2.COLOR_RGB2GRAY)
    
    # Create output with remapped colors
    pop_art = np.zeros_like(posterized)
    
    # Define brightness thresholds for color mapping
    thresholds = np.linspace(0, 255, len(current_palette) + 1)
    
    for i in range(len(current_palette)):
        mask = (gray >= thresholds[i]) & (gray < thresholds[i + 1])
        pop_art[mask] = current_palette[i]
    
    # Handle the brightest pixels
    mask = gray >= thresholds[-2]
    pop_art[mask] = current_palette[-1]

    # === BLEND WITH ORIGINAL COLORS ===
    # Use color preservation to blend pop art with original hues
    if color_preservation > 0:
        # Convert both to HSV
        pop_hsv = cv2.cvtColor(pop_art, cv2.COLOR_RGB2HSV).astype(np.float32)
        orig_hsv = cv2.cvtColor(original_colors, cv2.COLOR_RGB2HSV).astype(np.float32)
        
        # Blend hue from original, keep saturation and value from pop art
        blended_hsv = pop_hsv.copy()
        blended_hsv[:, :, 0] = pop_hsv[:, :, 0] * (1 - color_preservation * 0.7) + orig_hsv[:, :, 0] * (color_preservation * 0.7)
        # Boost saturation for pop art effect
        blended_hsv[:, :, 1] = np.clip(blended_hsv[:, :, 1] * 1.3, 0, 255)
        
        pop_art = cv2.cvtColor(blended_hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)

    # === HALFTONE/SCREEN PRINT EFFECT ===
    # Add subtle halftone dots for screen print aesthetic
    scale_x = py5.width / 640
    scale_y = py5.height / 480
    
    # Resize to canvas
    pop_art_display = cv2.resize(pop_art, (py5.width, py5.height))
    
    # Display base posterized image
    img = py5.create_image_from_numpy(pop_art_display, 'RGB')
    py5.image(img, 0, 0)

    # === ADD BOLD OUTLINES ===
    # Warhol often had strong black outlines
    gray_small = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray_small, 80, 160)
    
    # Dilate edges slightly for bolder lines
    kernel = np.ones((2, 2), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    
    # Draw edges
    py5.stroke(0, 0, 0, 180)  # Black outlines
    py5.stroke_weight(2)
    py5.no_fill()
    
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours[:150]:  # Limit for performance
        if len(contour) > 15:
            py5.begin_shape()
            for point in contour[::3]:  # Skip some points for cleaner look
                x = point[0][0] * scale_x
                y = point[0][1] * scale_y
                py5.vertex(x, y)
            py5.end_shape()

    # === OPTIONAL: HALFTONE DOTS OVERLAY ===
    # Add subtle dot pattern for authentic screen print look
    if style_strength > 0.5:
        py5.no_stroke()
        dot_spacing = 12
        for fy in range(0, 480, dot_spacing):
            for fx in range(0, 640, dot_spacing):
                # Dot size based on darkness
                brightness = gray_small[fy, fx]
                dot_size = py5.remap(255 - brightness, 0, 255, 0, dot_spacing * 0.4 * style_strength)
                
                if dot_size > 1:
                    x = fx * scale_x
                    y = fy * scale_y
                    # Use complementary color for dots
                    r, g, b = pop_art[fy, fx]
                    # Darker version of the color
                    py5.fill(r * 0.5, g * 0.5, b * 0.5, 80)
                    py5.ellipse(x, y, dot_size, dot_size)


def draw_ui():
    """Draw info panel."""
    py5.fill(0, 180)
    py5.no_stroke()
    py5.rect(10, 10, 320, 70, 5)

    py5.fill(255)
    py5.text_size(14)
    py5.text(f"Style: {modes[mode]}", 20, 32)

    py5.text_size(11)
    py5.text(f"Strength: {style_strength:.2f} (UP/DOWN)", 20, 55)
    py5.text(f"Color Preserve: {color_preservation:.2f} (LEFT/RIGHT)", 20, 70)


def key_pressed():
    global mode, style_strength, color_preservation

    if py5.key == '1':
        mode = 0
    elif py5.key == '2':
        mode = 1
    elif py5.key == '3':
        mode = 2
    elif py5.key == '4':
        mode = 3
    elif py5.key == '5':
        mode = 4
    elif py5.key == '6':
        mode = 5
    elif py5.key == py5.CODED:
        if py5.key_code == py5.UP:
            style_strength = min(1.0, style_strength + 0.1)
        elif py5.key_code == py5.DOWN:
            style_strength = max(0.1, style_strength - 0.1)
        elif py5.key_code == py5.LEFT:
            color_preservation = max(0.0, color_preservation - 0.1)
        elif py5.key_code == py5.RIGHT:
            color_preservation = min(1.0, color_preservation + 0.1)
    elif py5.key == 's':
        filename = f"ml_art_{modes[mode].replace(' ', '_')}_{py5.millis()}.png"
        py5.save(filename)
        print(f"Saved: {filename}")
    elif py5.key == 'q':
        cleanup()
        py5.exit_sketch()


def cleanup():
    """Release resources."""
    global cap
    if cap is not None:
        cap.release()


import atexit
atexit.register(cleanup)


# -------------------------------------------------
# Machine Learning Art Concepts:
#
# 1. Style Transfer (simplified):
#    - Extract content features
#    - Extract style features (textures, patterns)
#    - Combine using optimization
#
# 2. Classical ML Techniques Used:
#    - Edge detection (Canny, Laplacian)
#    - Contour analysis
#    - Color space manipulation
#    - Multi-scale processing
#
# 3. Neural Network Approaches:
#    - Convolution kernels simulate CNN layers
#    - Feature extraction at multiple scales
#    - Texture synthesis via statistics
#
# For Full Neural Style Transfer:
# - Use PyTorch with VGG19 model
# - Implement Gatys et al. algorithm
# - Or use fast-style-transfer models
#
# Extensions:
# - Load custom style images
# - Implement GAN-based generation
# - Add real-time style interpolation
# - Build style training pipeline
# -------------------------------------------------

py5.run_sketch()
