#!/usr/bin/env python3
import os
import json
from pathlib import Path

GALLERY_DIR = Path("/home/ubuntu/art-gallery-curator/gallery/in-progress")
DOMINANT_STYLE = "Tonalism"

artworks = sorted([d for d in GALLERY_DIR.iterdir() if d.is_dir()])

evaluation_data = []

for artwork_dir in artworks:
    artwork_name = artwork_dir.name
    
    # Find the latest version image
    images = list(artwork_dir.glob("*.png"))
    if not images:
        continue
    
    # Sort to find the latest version
    version_images = [img for img in images if img.stem.startswith('v')]
    if version_images:
        # Extract version number and sort
        def get_version_num(path):
            try:
                return int(path.stem.split('-')[0][1:])
            except:
                return 0
        latest_image = sorted(version_images, key=get_version_num, reverse=True)[0]
    else:
        latest_image = images[0]
    
    # Read CHANGELOG to get consecutive passes
    changelog_path = artwork_dir / "CHANGELOG.md"
    consecutive_passes = 0
    if changelog_path.exists():
        content = changelog_path.read_text()
        # Try to find consecutive passes count
        if "连续通过次数" in content:
            lines = content.split('\n')
            for line in lines:
                if "连续通过次数" in line and "/" in line:
                    try:
                        parts = line.split('/')
                        num_part = parts[0].split(':')[-1].strip()
                        consecutive_passes = int(num_part)
                        break
                    except:
                        pass
    
    evaluation_data.append({
        "name": artwork_name,
        "image_path": str(latest_image),
        "image_name": latest_image.name,
        "consecutive_passes": consecutive_passes,
        "changelog_exists": changelog_path.exists()
    })

# Save to JSON
output_path = Path("/home/ubuntu/art-gallery-curator/artworks_to_evaluate.json")
with open(output_path, 'w') as f:
    json.dump(evaluation_data, f, indent=2, ensure_ascii=False)

print(f"Total artworks: {len(evaluation_data)}")
print(f"Saved to: {output_path}")
