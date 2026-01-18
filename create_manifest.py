#!/usr/bin/env python3.11
import os
import re
import json
from pathlib import Path

IN_PROGRESS_DIR = Path("/home/ubuntu/art-gallery-curator/gallery/in-progress")

def get_latest_version(work_dir):
    png_files = list(work_dir.glob("*.png"))
    if not png_files:
        return None
    
    def version_key(path):
        match = re.search(r'v(\d+)', path.stem)
        return int(match.group(1)) if match else 0
    
    return sorted(png_files, key=version_key, reverse=True)[0]

def get_current_streak(work_dir):
    changelog = work_dir / "CHANGELOG.md"
    if not changelog.exists():
        return 0
    content = changelog.read_text()
    matches = re.findall(r'连续通过次数[：:]\s*(\d+)/10', content)
    return int(matches[-1]) if matches else 0

works = sorted([d for d in IN_PROGRESS_DIR.iterdir() if d.is_dir()])
manifest = []

for work_dir in works:
    latest = get_latest_version(work_dir)
    if latest:
        manifest.append({
            'name': work_dir.name,
            'latest_version': latest.name,
            'latest_path': str(latest),
            'v1_path': str(work_dir / 'v1-original.png'),
            'work_dir': str(work_dir),
            'streak': get_current_streak(work_dir)
        })

with open('/home/ubuntu/art-gallery-curator/manifest.json', 'w') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"Created manifest: {len(manifest)} works")
