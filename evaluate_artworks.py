import os
import json
from pathlib import Path

# Main style for this evaluation session
MAIN_STYLE = "Tonalism"

# Directory paths
IN_PROGRESS_DIR = Path("/home/ubuntu/art-gallery-curator/gallery/in-progress")

# Get all artwork directories
artwork_dirs = sorted([d for d in IN_PROGRESS_DIR.iterdir() if d.is_dir()])

print(f"Total artworks to evaluate: {len(artwork_dirs)}")
print(f"Main style: {MAIN_STYLE}\n")

# Store evaluation results
evaluations = []

for artwork_dir in artwork_dirs:
    artwork_name = artwork_dir.name
    
    # Find latest version
    png_files = sorted(artwork_dir.glob("*.png"), key=lambda x: x.stat().st_mtime, reverse=True)
    if not png_files:
        continue
    
    latest_version = png_files[0].name
    
    # Read CHANGELOG to get current consecutive passes
    changelog_path = artwork_dir / "CHANGELOG.md"
    current_passes = 0
    if changelog_path.exists():
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for "连续通过次数：" pattern
            import re
            matches = re.findall(r'连续通过次数[：:]\s*(\d+)', content)
            if matches:
                current_passes = int(matches[0])
    
    evaluations.append({
        'name': artwork_name,
        'latest_version': latest_version,
        'current_passes': current_passes,
        'path': str(artwork_dir)
    })

# Output evaluation list
output_file = Path("/home/ubuntu/art-gallery-curator/artworks_to_evaluate.json")
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(evaluations, f, indent=2, ensure_ascii=False)

print(f"Evaluation list saved to: {output_file}")
print(f"\nArtworks summary:")
for i, ev in enumerate(evaluations, 1):
    print(f"{i}. {ev['name']} - {ev['latest_version']} (passes: {ev['current_passes']}/10)")
