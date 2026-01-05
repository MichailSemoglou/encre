#!/usr/bin/env python3
"""
Data Bridge for Renoir to Processing.py Integration

This module provides utilities for exporting various types of data
from renoir analysis for use in Processing.py visualizations.

Exports include:
- Artist metadata and statistics
- Movement/style information
- Temporal evolution data
- Color harmony analysis
- Artist similarity matrices
"""

import json
from pathlib import Path
from datetime import datetime

try:
    from renoir import ArtistAnalyzer
    from renoir.color import ColorExtractor, ColorAnalyzer, ColorNamer
    RENOIR_AVAILABLE = True
except ImportError:
    RENOIR_AVAILABLE = False


def export_artist_statistics(artist_id, output_path):
    """
    Export comprehensive artist statistics for visualization.

    Args:
        artist_id: WikiArt artist identifier
        output_path: Path to save JSON file

    Returns:
        dict with artist statistics
    """
    if not RENOIR_AVAILABLE:
        raise ImportError("renoir package required")

    analyzer = ArtistAnalyzer()
    works = analyzer.extract_artist_works(artist_id)

    if not works:
        raise ValueError(f"No works found for artist: {artist_id}")

    # Analyze genres and styles
    genres = analyzer.analyze_genres(works)
    styles = analyzer.analyze_styles(works)

    # Extract color statistics from sample works
    extractor = ColorExtractor()
    color_analyzer = ColorAnalyzer()

    color_stats = []
    for work in works[:20]:  # Sample 20 works
        colors = extractor.extract_dominant_colors(work['image'], n_colors=5)
        stats = color_analyzer.analyze_palette_statistics(colors)
        temp = color_analyzer.analyze_color_temperature_distribution(colors)

        color_stats.append({
            'title': work.get('title', 'Untitled'),
            'mean_saturation': stats['mean_saturation'],
            'mean_brightness': stats['mean_value'],
            'warm_ratio': temp['warm_percentage'] / 100,
            'cool_ratio': temp['cool_percentage'] / 100,
            'diversity': color_analyzer.calculate_color_diversity(colors)
        })

    # Aggregate statistics
    if color_stats:
        avg_saturation = sum(s['mean_saturation'] for s in color_stats) / len(color_stats)
        avg_brightness = sum(s['mean_brightness'] for s in color_stats) / len(color_stats)
        avg_warm = sum(s['warm_ratio'] for s in color_stats) / len(color_stats)
        avg_diversity = sum(s['diversity'] for s in color_stats) / len(color_stats)
    else:
        avg_saturation = avg_brightness = avg_warm = avg_diversity = 0

    data = {
        'artist_id': artist_id,
        'artist_name': artist_id.replace('-', ' ').title(),
        'total_works': len(works),
        'genres': genres,
        'styles': styles,
        'color_statistics': {
            'average_saturation': avg_saturation,
            'average_brightness': avg_brightness,
            'warm_cool_ratio': avg_warm,
            'average_diversity': avg_diversity
        },
        'work_details': color_stats,
        'exported_at': datetime.now().isoformat()
    }

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Artist statistics exported to: {output_path}")
    return data


def export_movement_comparison(movement_artists, output_path):
    """
    Export comparison data for artists within a movement.

    Args:
        movement_artists: dict mapping movement name to list of artist IDs
        output_path: Path to save JSON file

    Example:
        export_movement_comparison({
            'Impressionism': ['claude-monet', 'pierre-auguste-renoir'],
            'Expressionism': ['edvard-munch', 'ernst-ludwig-kirchner']
        }, 'movements.json')
    """
    if not RENOIR_AVAILABLE:
        raise ImportError("renoir package required")

    analyzer = ArtistAnalyzer()
    extractor = ColorExtractor()
    color_analyzer = ColorAnalyzer()

    movements_data = {}

    for movement, artists in movement_artists.items():
        movement_data = {
            'name': movement,
            'artists': []
        }

        for artist_id in artists:
            print(f"Processing {artist_id}...")
            try:
                works = analyzer.extract_artist_works(artist_id, limit=10)
                if not works:
                    continue

                # Get representative palette
                all_colors = []
                for work in works[:5]:
                    colors = extractor.extract_dominant_colors(work['image'], n_colors=5)
                    all_colors.extend(colors)

                # Analyze colors
                if all_colors:
                    stats = color_analyzer.analyze_palette_statistics(all_colors[:20])
                    temp = color_analyzer.analyze_color_temperature_distribution(all_colors[:20])

                    artist_data = {
                        'id': artist_id,
                        'name': artist_id.replace('-', ' ').title(),
                        'works_count': len(works),
                        'avg_saturation': stats['mean_saturation'],
                        'avg_brightness': stats['mean_value'],
                        'warm_ratio': temp['warm_percentage'] / 100,
                        'palette': [list(c) for c in all_colors[:5]]
                    }
                    movement_data['artists'].append(artist_data)

            except Exception as e:
                print(f"  Error processing {artist_id}: {e}")

        movements_data[movement] = movement_data

    with open(output_path, 'w') as f:
        json.dump(movements_data, f, indent=2)

    print(f"Movement comparison exported to: {output_path}")
    return movements_data


def export_temporal_data(artist_id, output_path):
    """
    Export temporal color evolution data for an artist.

    Args:
        artist_id: WikiArt artist identifier
        output_path: Path to save JSON file
    """
    if not RENOIR_AVAILABLE:
        raise ImportError("renoir package required")

    analyzer = ArtistAnalyzer()
    extractor = ColorExtractor()
    color_analyzer = ColorAnalyzer()

    works = analyzer.extract_artist_works(artist_id)

    if not works:
        raise ValueError(f"No works found for artist: {artist_id}")

    # Group by year/decade
    temporal_data = []

    for work in works:
        year = work.get('date')
        if not year or year == 0:
            continue

        try:
            colors = extractor.extract_dominant_colors(work['image'], n_colors=5)
            stats = color_analyzer.analyze_palette_statistics(colors)
            temp = color_analyzer.analyze_color_temperature_distribution(colors)

            temporal_data.append({
                'year': int(year),
                'title': work.get('title', 'Untitled'),
                'saturation': stats['mean_saturation'],
                'brightness': stats['mean_value'],
                'warm_ratio': temp['warm_percentage'] / 100,
                'diversity': color_analyzer.calculate_color_diversity(colors),
                'palette': [list(c) for c in colors]
            })
        except Exception as e:
            continue

    # Sort by year
    temporal_data.sort(key=lambda x: x['year'])

    data = {
        'artist_id': artist_id,
        'artist_name': artist_id.replace('-', ' ').title(),
        'timeline': temporal_data,
        'year_range': {
            'start': temporal_data[0]['year'] if temporal_data else None,
            'end': temporal_data[-1]['year'] if temporal_data else None
        },
        'exported_at': datetime.now().isoformat()
    }

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Temporal data exported to: {output_path}")
    return data


def export_harmony_analysis(artist_id, output_path):
    """
    Export color harmony analysis for Processing visualization.

    Args:
        artist_id: WikiArt artist identifier
        output_path: Path to save JSON file
    """
    if not RENOIR_AVAILABLE:
        raise ImportError("renoir package required")

    analyzer = ArtistAnalyzer()
    extractor = ColorExtractor()
    color_analyzer = ColorAnalyzer()

    works = analyzer.extract_artist_works(artist_id, limit=20)

    if not works:
        raise ValueError(f"No works found for artist: {artist_id}")

    harmony_data = []

    for work in works:
        try:
            colors = extractor.extract_dominant_colors(work['image'], n_colors=6)
            harmony = color_analyzer.analyze_color_harmony(colors)

            harmony_data.append({
                'title': work.get('title', 'Untitled'),
                'palette': [list(c) for c in colors],
                'harmony_score': harmony['harmony_score'],
                'dominant_harmony': harmony['dominant_harmony'],
                'harmonies': harmony['harmonies']
            })
        except Exception as e:
            continue

    # Aggregate harmony preferences
    harmony_counts = {}
    for item in harmony_data:
        h = item['dominant_harmony']
        harmony_counts[h] = harmony_counts.get(h, 0) + 1

    data = {
        'artist_id': artist_id,
        'artist_name': artist_id.replace('-', ' ').title(),
        'works_analyzed': len(harmony_data),
        'harmony_preferences': harmony_counts,
        'average_harmony_score': sum(h['harmony_score'] for h in harmony_data) / len(harmony_data) if harmony_data else 0,
        'work_harmonies': harmony_data,
        'exported_at': datetime.now().isoformat()
    }

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Harmony analysis exported to: {output_path}")
    return data


def create_processing_palette_file(colors, output_path, name="palette"):
    """
    Create a simple palette file optimized for Processing.py loading.

    Args:
        colors: List of RGB tuples
        output_path: Path to save file
        name: Name identifier for the palette
    """
    data = {
        'name': name,
        'colors': [list(c) for c in colors],
        'hex': ['#{:02x}{:02x}{:02x}'.format(c[0], c[1], c[2]) for c in colors]
    }

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Palette saved to: {output_path}")
    return data


# Processing.py helper code template
PROCESSING_LOADER_TEMPLATE = '''
# Processing.py Palette Loader
# Copy this into your Processing sketch

import json

def loadPalette(filename):
    """Load a palette from JSON file."""
    with open(filename) as f:
        data = json.load(f)
    return [color(c[0], c[1], c[2]) for c in data['colors']]

def loadNamedPalette(filename):
    """Load palette with color names."""
    with open(filename) as f:
        data = json.load(f)
    palette = []
    for c in data.get('named_colors', data.get('colors', [])):
        if isinstance(c, dict):
            palette.append({
                'color': color(c['rgb'][0], c['rgb'][1], c['rgb'][2]),
                'name': c.get('name', 'Unknown'),
                'hex': c.get('hex', '')
            })
        else:
            palette.append({
                'color': color(c[0], c[1], c[2]),
                'name': 'Unknown',
                'hex': ''
            })
    return palette

# Usage in setup():
# palette = loadPalette('data/monet.json')
# fill(palette[0])
# ellipse(width/2, height/2, 100, 100)
'''


def generate_processing_loader(output_path):
    """Generate the Processing.py loader helper code."""
    with open(output_path, 'w') as f:
        f.write(PROCESSING_LOADER_TEMPLATE)
    print(f"Processing loader template saved to: {output_path}")


if __name__ == '__main__':
    print("Data Bridge Utilities for Renoir → Processing.py")
    print("=" * 50)
    print("\nAvailable functions:")
    print("  - export_artist_statistics(artist_id, output_path)")
    print("  - export_movement_comparison(movement_artists, output_path)")
    print("  - export_temporal_data(artist_id, output_path)")
    print("  - export_harmony_analysis(artist_id, output_path)")
    print("  - create_processing_palette_file(colors, output_path)")
    print("  - generate_processing_loader(output_path)")
    print("\nExample:")
    print("  from data_bridge import export_artist_statistics")
    print("  export_artist_statistics('claude-monet', '../assets/monet_stats.json')")
