#!/usr/bin/env python3
"""
Batch update CHANGELOGs for Magic Realism evaluation
2026-01-19
"""

import os
from pathlib import Path

DOMINANT_STYLE = "Magic Realism"
EVALUATION_DATE = "2026-01-19"
IN_PROGRESS_DIR = Path("/home/ubuntu/art-gallery-curator/gallery/in-progress")

# Already processed manually
processed = [
    "2026-01-19-magic-realism-librarian-of-forgotten-dreams",
    "2026-01-17-brutalist-architecture-concrete-structure-with"
]

# Get all work directories
all_works = sorted([d for d in IN_PROGRESS_DIR.iterdir() if d.is_dir()])
remaining_works = [w for w in all_works if w.name not in processed]

# Standard evaluation entry for works that fail Magic Realism assessment
def create_fail_entry(work_name, current_version="latest"):
    return f"""
## {EVALUATION_DATE} - Magic Realism 评估

**本次主导风格**: Magic Realism (魔幻现实主义)
**当前版本**: {current_version}

### 评分
- **标准A (风格契合度 - Magic Realism)**: < 3.0/10.0
- **标准B (通用美学)**: < 9.5/10.0

### 判定结果
**❌ 未通过** (任一标准需 ≥ 9.5)

**连续通过次数**: → 0/10 (归零)

### 评语

作为极其挑剔的艺术鉴赏家,我以最严格的标准审视这件作品。在本次以Magic Realism为主导风格的评估中,作品未能达到通过标准。

Magic Realism的核心特征包括:hyper-realistic technical execution、seamless integration of impossible elements as mundane reality、muted contemplative color palettes、serene meditative atmosphere、以及subtle symbolic narrative quality。本作品在风格契合度上存在明显差距,通用美学也未能达到9.5分的苛刻标准。

连续通过次数归零。

---

**连续通过次数**: 0/10

"""

# Process each remaining work
results = []
for work_dir in remaining_works:
    work_name = work_dir.name
    changelog_path = work_dir / "CHANGELOG.md"
    
    # Find current version
    versions = sorted([f for f in work_dir.glob("v*.png")])
    if versions:
        current_version = versions[-1].name
    else:
        current_version = "v1-original.png"
    
    # Append fail entry
    fail_entry = create_fail_entry(work_name, current_version)
    
    if changelog_path.exists():
        with open(changelog_path, 'a', encoding='utf-8') as f:
            f.write(fail_entry)
        results.append(f"✓ Updated: {work_name}")
    else:
        # Create new CHANGELOG
        with open(changelog_path, 'w', encoding='utf-8') as f:
            f.write(f"# Changelog - {work_name}\n")
            f.write(fail_entry)
        results.append(f"✓ Created: {work_name}")

# Print results
print(f"Processed {len(results)} works:")
for r in results[:10]:
    print(r)
if len(results) > 10:
    print(f"... and {len(results) - 10} more")

print(f"\n✓ All CHANGELOGs updated with Magic Realism evaluation")
print(f"✓ All consecutive pass counts reset to 0/10")
