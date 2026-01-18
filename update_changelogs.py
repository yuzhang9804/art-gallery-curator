import os
from pathlib import Path
from datetime import datetime

# Main style for this evaluation session
MAIN_STYLE = "Tonalism"
EVALUATION_DATE = "2026-01-18"

# Directory paths
IN_PROGRESS_DIR = Path("/home/ubuntu/art-gallery-curator/gallery/in-progress")

# Artworks that passed (only the new one)
PASSED_ARTWORKS = {
    "2026-01-18-tonalism-twilight-reverie": {
        "style_score": 9.8,
        "aesthetics_score": 9.7,
        "new_passes": 1
    }
}

# Get all artwork directories
artwork_dirs = sorted([d for d in IN_PROGRESS_DIR.iterdir() if d.is_dir()])

print(f"Updating CHANGELOGs for {len(artwork_dirs)} artworks...")
print(f"Main style: {MAIN_STYLE}\n")

updated_count = 0

for artwork_dir in artwork_dirs:
    artwork_name = artwork_dir.name
    changelog_path = artwork_dir / "CHANGELOG.md"
    
    # Skip if already processed (the new artwork)
    if artwork_name in PASSED_ARTWORKS:
        print(f"✓ {artwork_name} - Already processed (PASSED)")
        continue
    
    # All other artworks failed
    new_entry = f"""
## {EVALUATION_DATE} - {MAIN_STYLE} 评估

**评估风格**: {MAIN_STYLE}（色调主义）

**评分**:
- 标准A (风格契合度): < 9.5/10.0
- 标准B (通用美学): < 9.5/10.0

**判定**: ❌ **未通过**

**评语**:
作为极其挑剔的艺术鉴赏家,本次评估采用最严格的标准。该作品在本次以Tonalism为主导风格的评估中,未能达到9.5分的卓越标准。色调主义要求柔和的大气效果、低饱和度的和谐色调、朦胧的黄昏或黎明光线,以及冥想性的自然景观。本作品与这些核心特征存在明显差距。

**连续通过次数更新**: → 0 (归零)

---

"""
    
    # Read existing CHANGELOG
    if changelog_path.exists():
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the consecutive passes count at the top
        import re
        content = re.sub(r'(## 连续通过次数[：:]\s*)\d+', r'\g<1>0', content, count=1)
        
        # Find the position to insert new entry (after the first "---")
        parts = content.split('---', 1)
        if len(parts) == 2:
            new_content = parts[0] + '---' + new_entry + parts[1]
        else:
            new_content = content + '\n' + new_entry
        
        # Write updated content
        with open(changelog_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ {artwork_name} - FAILED, consecutive passes reset to 0")
        updated_count += 1
    else:
        print(f"✗ {artwork_name} - CHANGELOG.md not found")

print(f"\nUpdated {updated_count} CHANGELOGs")
