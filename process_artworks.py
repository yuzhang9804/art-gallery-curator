#!/usr/bin/env python3.11
"""
Process artworks based on evaluation results
"""

import json
from pathlib import Path
from datetime import datetime

# Load evaluation results
GALLERY_ROOT = Path("/home/ubuntu/art-gallery-curator/gallery")
results_file = GALLERY_ROOT / "evaluation_results.json"

with open(results_file, 'r', encoding='utf-8') as f:
    evaluation_results = json.load(f)

# Process each artwork
for result in evaluation_results:
    folder_name = result['folder']
    artwork_dir = GALLERY_ROOT / "in-progress" / folder_name
    
    if not artwork_dir.exists():
        continue
    
    # Create or update CHANGELOG.md
    changelog_path = artwork_dir / "CHANGELOG.md"
    
    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Create changelog entry
    changelog_entry = f"""# Changelog - {result['title']}

## {current_date} - Neo-Expressionism Evaluation

**评估风格**: Neo-Expressionism (新表现主义)

**评分结果**:
- 风格契合度 (Style Alignment): {result['style_alignment']:.1f}/10.0
- 通用美学 (Universal Aesthetics): {result['universal_aesthetics']:.1f}/10.0

**本次判定**: {'✓ 通过' if result['passed'] else '✗ 未通过'}

**连续通过次数**: {result['current_consecutive']} → {result['new_consecutive']}

---

"""
    
    # Read existing changelog if exists
    existing_content = ""
    if changelog_path.exists():
        existing_content = changelog_path.read_text(encoding='utf-8')
        # Remove old header if exists
        if existing_content.startswith("# Changelog"):
            lines = existing_content.split('\n')
            # Find first "---" separator
            for i, line in enumerate(lines):
                if line.strip() == "---" and i > 0:
                    existing_content = '\n'.join(lines[i+1:])
                    break
    
    # Write updated changelog
    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(changelog_entry)
        if existing_content.strip():
            f.write(existing_content)
    
    # Create GALLERY.md if it doesn't exist
    gallery_path = artwork_dir / "GALLERY.md"
    if not gallery_path.exists():
        # Find v1-original.png
        v1_path = artwork_dir / "v1-original.png"
        if v1_path.exists():
            gallery_content = f"""# {result['title']}

![{result['title']}](v1-original.png)

**Style**: {result['style']}

**Status**: In Progress

**Consecutive Passes**: {result['new_consecutive']}/10

---

*Last updated: {current_date}*
"""
            with open(gallery_path, 'w', encoding='utf-8') as f:
                f.write(gallery_content)
    
    print(f"Processed: {folder_name}")

print(f"\nAll artworks processed. CHANGELOGs updated.")

# Output list of artworks that need new versions
failed_artworks = [r for r in evaluation_results if not r['passed']]
print(f"\nArtworks needing new versions: {len(failed_artworks)}")

# Save list for reference
failed_list_path = GALLERY_ROOT / "artworks_need_regeneration.json"
with open(failed_list_path, 'w', encoding='utf-8') as f:
    json.dump(failed_artworks, f, indent=2, ensure_ascii=False)

print(f"List saved to: {failed_list_path}")
