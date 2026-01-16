import os
import json
from pathlib import Path

# Main evaluation style
MAIN_STYLE = "Algorithmic Art"
EVALUATION_DATE = "2026-01-16"

# Directory paths
IN_PROGRESS_DIR = Path("/home/ubuntu/art-gallery-curator/gallery/in-progress")

# Get all artwork directories
artworks = [d for d in IN_PROGRESS_DIR.iterdir() if d.is_dir()]

# Already evaluated
evaluated = ["algorithmic-art-fractal-consciousness", "abstract-expressionism-emotional-tempest"]

# Prepare evaluation list
evaluation_list = []

for artwork_dir in sorted(artworks):
    artwork_name = artwork_dir.name
    
    if artwork_name in evaluated:
        continue
    
    # Find latest version
    versions = sorted([f for f in artwork_dir.glob("v*.png")], reverse=True)
    if not versions:
        continue
    
    latest_version = versions[0].name
    
    # Read CHANGELOG to get current consecutive pass count
    changelog_path = artwork_dir / "CHANGELOG.md"
    consecutive_count = 0
    if changelog_path.exists():
        content = changelog_path.read_text()
        for line in content.split('\n'):
            if '连续通过次数' in line or '連續通過次數' in line:
                # Extract number
                import re
                match = re.search(r'[:：]\s*(\d+)', line)
                if match:
                    consecutive_count = int(match.group(1))
                break
    
    evaluation_list.append({
        "name": artwork_name,
        "path": str(artwork_dir),
        "latest_version": latest_version,
        "consecutive_count": consecutive_count
    })

# Output evaluation list
print(json.dumps(evaluation_list, indent=2, ensure_ascii=False))
print(f"\n总计待评估作品数：{len(evaluation_list)}")
