#!/usr/bin/env python3
"""
Systematic evaluation script for all artworks in gallery/in-progress/
Evaluates against today's style: Fauvism
"""

import os
import json
from pathlib import Path

# Today's evaluating style
EVALUATING_STYLE = "Fauvism"
EVALUATING_DATE = "2026-01-17"

# All artworks to evaluate
ARTWORKS = [
    "2026-01-17-brutalist-architecture-concrete-structure-with",
    "abstract-expressionism-emotional-tempest",
    "algorithmic-art-fractal-consciousness",
    "art-deco-metropolitan-elegance",
    "art-nouveau-floral-reverie",
    "bauhaus-geometric-harmony",
    "byzantine-sacred-mosaic",
    "constructivism-revolutionary-architecture",
    "cyberpunk-neon-rain",
    "digital-art-quantum-garden",
    "elementarism-dynamic-diagonals",
    "fauvism-wild-garden-at-twilight",
    "futurism-velocity-symphony",
    "german-expressionism-urban-anxiety",
    "jugendstil-enchanted-forest",
    "land-art-spiral-desert",
    "outsider-art-inner-cosmos",
    "pointillism-sunday-by-the-river",
    "pop-art-consumer-paradise",
    "rococo-garden-of-enchantment",
    "secessionist-eternal-embrace",
    "situationist-international-urban-drift",
    "steampunk-clockwork-observatory",
    "suprematism-cosmic-architecture",
    "suprematism-cosmic-ascension",
    "surrealism-dreamscape-labyrinth",
    "tenebrism-candlelit-contemplation",
    "ukiyo-e-wave-of-dreams",
    "vaporwave-digital-nostalgia"
]

def get_latest_version(artwork_dir):
    """Get the latest version image file in the artwork directory"""
    versions = []
    for file in os.listdir(artwork_dir):
        if file.endswith('.png') and (file.startswith('v') or 'original' in file):
            versions.append(file)
    
    if not versions:
        return None
    
    # Sort by version number
    versions.sort(reverse=True)
    return versions[0]

def main():
    gallery_path = Path("/home/ubuntu/art-gallery-curator/gallery/in-progress")
    
    evaluation_list = []
    
    for artwork in ARTWORKS:
        artwork_path = gallery_path / artwork
        if not artwork_path.exists():
            print(f"Warning: {artwork} not found")
            continue
        
        latest_version = get_latest_version(artwork_path)
        if not latest_version:
            print(f"Warning: No image found in {artwork}")
            continue
        
        evaluation_list.append({
            "artwork": artwork,
            "path": str(artwork_path),
            "latest_version": latest_version,
            "full_path": str(artwork_path / latest_version)
        })
    
    # Save evaluation list
    output_file = "/home/ubuntu/art-gallery-curator/evaluation_list.json"
    with open(output_file, 'w') as f:
        json.dump({
            "evaluating_style": EVALUATING_STYLE,
            "evaluating_date": EVALUATING_DATE,
            "total_artworks": len(evaluation_list),
            "artworks": evaluation_list
        }, f, indent=2)
    
    print(f"Evaluation list created: {len(evaluation_list)} artworks")
    print(f"Saved to: {output_file}")
    
    # Print list for manual review
    for i, item in enumerate(evaluation_list, 1):
        print(f"{i}. {item['artwork']} - {item['latest_version']}")

if __name__ == "__main__":
    main()
