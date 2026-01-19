#!/usr/bin/env python3
"""Get complete list of all artworks with their latest versions"""

import os
import json
from pathlib import Path

GALLERY_DIR = Path("/home/ubuntu/art-gallery-curator/gallery/in-progress")

def get_latest_version(artwork_dir):
    """Get the latest version image file"""
    versions = []
    for file in os.listdir(artwork_dir):
        if file.endswith('.png'):
            versions.append(file)
    
    if not versions:
        return None
    
    # Sort to get latest version
    versions.sort(reverse=True)
    return versions[0]

def main():
    artworks = []
    
    for item in sorted(GALLERY_DIR.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            latest = get_latest_version(item)
            if latest:
                artworks.append({
                    "name": item.name,
                    "path": str(item),
                    "latest_version": latest,
                    "full_path": str(item / latest)
                })
    
    print(f"Total artworks: {len(artworks)}\n")
    for i, art in enumerate(artworks, 1):
        print(f"{i}. {art['name']} - {art['latest_version']}")
    
    # Save to JSON
    output = {
        "date": "2026-01-19",
        "style": "Vorticism",
        "total": len(artworks),
        "artworks": artworks
    }
    
    output_file = Path("/home/ubuntu/art-gallery-curator/all_artworks_complete.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved to: {output_file}")

if __name__ == "__main__":
    main()
