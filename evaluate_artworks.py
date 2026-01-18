#!/usr/bin/env python3.11
"""
Art Gallery Curator - Artwork Evaluation System
Evaluates artworks against today's dominant style (Neo-Geo) with strict standards
"""

import os
import json
from pathlib import Path
from datetime import datetime

# Today's dominant style for evaluation
DOMINANT_STYLE = "Graffiti Art"
DOMINANT_STYLE_DESC = "Urban street art movement featuring bold spray-painted murals, wildstyle lettering, vibrant colors, and social commentary with raw rebellious energy"

# Evaluation criteria
PASS_THRESHOLD = 9.5  # Either criterion A or B must be >= 9.5
PERFECT_THRESHOLD = 10  # Consecutive passes needed for "perfect" status

def get_latest_version_image(artwork_dir):
    """Get the latest version image from an artwork directory"""
    images = sorted([f for f in os.listdir(artwork_dir) if f.endswith('.png')])
    if not images:
        return None
    # Prefer v*-*.png pattern, fallback to v1-original.png
    versioned = [img for img in images if img.startswith('v')]
    return versioned[-1] if versioned else images[-1]

def read_changelog(artwork_dir):
    """Read CHANGELOG.md and extract consecutive pass count"""
    changelog_path = os.path.join(artwork_dir, 'CHANGELOG.md')
    if not os.path.exists(changelog_path):
        return 0, []
    
    with open(changelog_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract consecutive pass count from the first line
    lines = content.strip().split('\n')
    consecutive_passes = 0
    history = []
    
    for line in lines:
        if line.startswith('**连续通过次数'):
            try:
                consecutive_passes = int(line.split(':')[1].split('/')[0].strip())
            except:
                consecutive_passes = 0
        elif line.startswith('###'):
            history.append(line)
    
    return consecutive_passes, history

def extract_style_from_name(artwork_name):
    """Extract art style from artwork directory name"""
    # Remove date prefix if exists
    name = artwork_name
    if name.startswith('2026-'):
        parts = name.split('-', 3)
        if len(parts) > 3:
            name = parts[3]
    
    # Common style patterns
    style_map = {
        'abstract-expressionism': 'Abstract Expressionism',
        'algorithmic-art': 'Algorithmic Art',
        'art-deco': 'Art Deco',
        'art-nouveau': 'Art Nouveau',
        'bauhaus': 'Bauhaus',
        'brutalist': 'Brutalism',
        'byzantine': 'Byzantine',
        'constructivism': 'Constructivism',
        'cyberpunk': 'Cyberpunk',
        'digital-art': 'Digital Art',
        'elementarism': 'Elementarism',
        'fauvism': 'Fauvism',
        'futurism': 'Futurism',
        'german-expressionism': 'German Expressionism',
        'jugendstil': 'Jugendstil',
        'kinetic-art': 'Kinetic Art',
        'land-art': 'Land Art',
        'neo-geo': 'Neo-Geo',
        'outsider-art': 'Outsider Art',
        'pointillism': 'Pointillism',
        'pop-art': 'Pop Art',
        'purism': 'Purism',
        'rayonism': 'Rayonism',
        'rococo': 'Rococo',
        'secessionist': 'Secessionism',
        'situationist': 'Situationist International',
        'songlines': 'Aboriginal Songlines',
        'steampunk': 'Steampunk',
        'suprematism': 'Suprematism',
        'surrealism': 'Surrealism',
        'tenebrism': 'Tenebrism',
        'ukiyo-e': 'Ukiyo-e',
        'vaporwave': 'Vaporwave',
        'graffiti-art': 'Graffiti Art',
        'graffiti': 'Graffiti Art'
    }
    
    for key, value in style_map.items():
        if key in artwork_name.lower():
            return value
    
    return "Unknown Style"

# List all artworks
in_progress_dir = Path('/home/ubuntu/art-gallery-curator/gallery/in-progress')
artworks = sorted([d for d in os.listdir(in_progress_dir) if os.path.isdir(in_progress_dir / d) and d != '.gitkeep'])

print(f"=== Art Gallery Curator Evaluation ===")
print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
print(f"Dominant Style: {DOMINANT_STYLE}")
print(f"Total Artworks to Evaluate: {len(artworks)}")
print(f"")

# Prepare evaluation list
evaluation_list = []
for artwork_name in artworks:
    artwork_dir = in_progress_dir / artwork_name
    image_file = get_latest_version_image(artwork_dir)
    consecutive_passes, _ = read_changelog(artwork_dir)
    artwork_style = extract_style_from_name(artwork_name)
    
    if image_file:
        evaluation_list.append({
            'name': artwork_name,
            'style': artwork_style,
            'image': str(artwork_dir / image_file),
            'consecutive_passes': consecutive_passes
        })

# Save evaluation list for processing
output_file = '/home/ubuntu/art-gallery-curator/evaluation_list.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({
        'dominant_style': DOMINANT_STYLE,
        'dominant_style_desc': DOMINANT_STYLE_DESC,
        'artworks': evaluation_list
    }, f, indent=2, ensure_ascii=False)

print(f"Evaluation list prepared: {len(evaluation_list)} artworks")
print(f"Output: {output_file}")
