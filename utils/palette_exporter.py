#!/usr/bin/env python3
"""
Palette Exporter for Processing.py Integration

This utility exports color palettes from renoir analysis
into JSON format that can be easily loaded in Processing.py sketches.

Usage:
    python palette_exporter.py --artist claude-monet --output monet.json
    python palette_exporter.py --artist vincent-van-gogh --colors 8 --output vangogh.json
"""

import json
import argparse
from pathlib import Path

try:
    from renoir import ArtistAnalyzer
    from renoir.color import ColorExtractor, ColorNamer
    RENOIR_AVAILABLE = True
except ImportError:
    RENOIR_AVAILABLE = False
    print("Warning: renoir package not installed. Install with: pip install renoir-wikiart")


def extract_artist_palette(artist_id, n_colors=5, n_works=10):
    """
    Extract a representative color palette from an artist's works.

    Args:
        artist_id: WikiArt artist identifier (e.g., 'claude-monet')
        n_colors: Number of colors to extract per work
        n_works: Number of works to sample

    Returns:
        dict with palette data
    """
    if not RENOIR_AVAILABLE:
        raise ImportError("renoir package required. Install with: pip install renoir-wikiart")

    analyzer = ArtistAnalyzer()
    extractor = ColorExtractor()
    namer = ColorNamer(vocabulary="artist")

    # Get artist works
    works = analyzer.extract_artist_works(artist_id, limit=n_works)

    if not works:
        raise ValueError(f"No works found for artist: {artist_id}")

    # Collect all colors
    all_colors = []
    work_palettes = []

    for work in works:
        colors = extractor.extract_dominant_colors(work['image'], n_colors=n_colors)
        work_palette = {
            'title': work.get('title', 'Untitled'),
            'colors': [list(c) for c in colors]
        }
        work_palettes.append(work_palette)
        all_colors.extend(colors)

    # Extract overall dominant palette
    if len(all_colors) > n_colors:
        # Re-cluster all colors to get representative palette
        from sklearn.cluster import KMeans
        import numpy as np

        kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
        kmeans.fit(all_colors)
        dominant_colors = kmeans.cluster_centers_.astype(int).tolist()
    else:
        dominant_colors = [list(c) for c in all_colors[:n_colors]]

    # Add color names
    named_colors = []
    for rgb in dominant_colors:
        name_data = namer.name(tuple(rgb), return_metadata=True)
        named_colors.append({
            'rgb': rgb,
            'hex': name_data['hex'],
            'name': name_data['name'],
            'family': name_data['family']
        })

    return {
        'artist': artist_id,
        'artist_display': artist_id.replace('-', ' ').title(),
        'n_works_sampled': len(works),
        'colors': dominant_colors,
        'named_colors': named_colors,
        'work_palettes': work_palettes
    }


def export_palette_json(palette_data, output_path):
    """Export palette data to JSON file."""
    with open(output_path, 'w') as f:
        json.dump(palette_data, f, indent=2)
    print(f"Palette exported to: {output_path}")


def export_multiple_artists(artists, output_dir, n_colors=5, n_works=10):
    """
    Export palettes for multiple artists.

    Args:
        artists: List of artist IDs
        output_dir: Directory to save JSON files
        n_colors: Colors per palette
        n_works: Works to sample per artist
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    results = {}

    for artist_id in artists:
        print(f"Extracting palette for {artist_id}...")
        try:
            palette = extract_artist_palette(artist_id, n_colors, n_works)
            output_path = output_dir / f"{artist_id.replace('-', '_')}.json"
            export_palette_json(palette, output_path)
            results[artist_id] = 'success'
        except Exception as e:
            print(f"  Error: {e}")
            results[artist_id] = f'error: {e}'

    return results


# Pre-defined artist collections for common use cases
IMPRESSIONISTS = [
    'claude-monet',
    'pierre-auguste-renoir',
    'edgar-degas',
    'camille-pissarro',
    'alfred-sisley'
]

POST_IMPRESSIONISTS = [
    'vincent-van-gogh',
    'paul-cezanne',
    'paul-gauguin',
    'georges-seurat'
]

EXPRESSIONISTS = [
    'edvard-munch',
    'ernst-ludwig-kirchner',
    'wassily-kandinsky',
    'franz-marc'
]

ABSTRACT = [
    'wassily-kandinsky',
    'piet-mondrian',
    'kazimir-malevich',
    'mark-rothko'
]


def main():
    parser = argparse.ArgumentParser(
        description='Export artist palettes from renoir for Processing.py'
    )
    parser.add_argument(
        '--artist', '-a',
        help='Artist ID (e.g., claude-monet)'
    )
    parser.add_argument(
        '--group', '-g',
        choices=['impressionists', 'post-impressionists', 'expressionists', 'abstract'],
        help='Export a predefined group of artists'
    )
    parser.add_argument(
        '--output', '-o',
        default='palette.json',
        help='Output file or directory path'
    )
    parser.add_argument(
        '--colors', '-c',
        type=int,
        default=5,
        help='Number of colors to extract (default: 5)'
    )
    parser.add_argument(
        '--works', '-w',
        type=int,
        default=10,
        help='Number of works to sample (default: 10)'
    )

    args = parser.parse_args()

    if args.group:
        groups = {
            'impressionists': IMPRESSIONISTS,
            'post-impressionists': POST_IMPRESSIONISTS,
            'expressionists': EXPRESSIONISTS,
            'abstract': ABSTRACT
        }
        artists = groups[args.group]
        export_multiple_artists(artists, args.output, args.colors, args.works)
    elif args.artist:
        palette = extract_artist_palette(args.artist, args.colors, args.works)
        export_palette_json(palette, args.output)
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python palette_exporter.py --artist claude-monet --output ../assets/palettes/monet.json")
        print("  python palette_exporter.py --group impressionists --output ../assets/palettes/")


if __name__ == '__main__':
    main()
