#!/usr/bin/env python3
"""
Evaluation script for Tonalism style assessment
"""

import os
import json
from pathlib import Path

# Today's dominant style
DOMINANT_STYLE = "Tonalism"

# Base directory
GALLERY_DIR = Path("/home/ubuntu/art-gallery-curator/gallery/in-progress")

# Get all artwork directories
artworks = sorted([d for d in GALLERY_DIR.iterdir() if d.is_dir()])

print(f"Total artworks to evaluate: {len(artworks)}")
print(f"Dominant style for today: {DOMINANT_STYLE}")
print("=" * 80)

for artwork_dir in artworks:
    print(f"\nArtwork: {artwork_dir.name}")
    
    # Check if v1-original.png exists
    original_img = artwork_dir / "v1-original.png"
    if not original_img.exists():
        print(f"  ⚠️  No v1-original.png found, skipping...")
        continue
    
    # Check CHANGELOG.md
    changelog = artwork_dir / "CHANGELOG.md"
    if changelog.exists():
        content = changelog.read_text()
        print(f"  📄 CHANGELOG exists")
    else:
        print(f"  ⚠️  No CHANGELOG.md found")
    
    print(f"  🖼️  Image: {original_img.name}")
