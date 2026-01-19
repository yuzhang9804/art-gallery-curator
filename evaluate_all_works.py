import os
import json
from pathlib import Path

# Get all artwork directories in in-progress
in_progress_dir = Path("/home/ubuntu/art-gallery-curator/gallery/in-progress")
artworks = [d for d in in_progress_dir.iterdir() if d.is_dir()]

print(f"Found {len(artworks)} artworks in in-progress directory")
print("\nArtwork list:")
for i, artwork in enumerate(sorted(artworks), 1):
    print(f"{i}. {artwork.name}")

# Save to JSON for processing
artwork_data = {
    "total": len(artworks),
    "artworks": [str(a.name) for a in sorted(artworks)]
}

with open("/home/ubuntu/art-gallery-curator/artworks_to_evaluate.json", "w") as f:
    json.dump(artwork_data, f, indent=2, ensure_ascii=False)

print(f"\nSaved artwork list to artworks_to_evaluate.json")
