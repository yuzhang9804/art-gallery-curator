#!/usr/bin/env python3.11
import json
from pathlib import Path
from datetime import datetime

# Load evaluation results
with open("/home/ubuntu/art-gallery-curator/superflat_evaluation_results.json", "r") as f:
    results = json.load(f)

today = datetime.now().strftime("%Y-%m-%d")

for result in results:
    artwork_name = result["name"]
    score_a = result["score_a"]
    score_b = result["score_b"]
    passed = result["passed"]
    new_passes = result["new_consecutive_passes"]
    
    artwork_dir = Path(f"/home/ubuntu/art-gallery-curator/gallery/in-progress/{artwork_name}")
    changelog_path = artwork_dir / "CHANGELOG.md"
    
    if not changelog_path.exists():
        continue
    
    # Create evaluation entry
    status_emoji = "✅ 通过" if passed else "❌ 未通过"
    
    evaluation_entry = f"""
## {today} - Superflat 评估

**本次主导风格**: Superflat (超扁平)

### 评分
- **标准A (风格契合度 - Superflat)**: {score_a}/10.0
- **标准B (通用美学)**: {score_b}/10.0

### 判定结果
**{status_emoji}** (任一标准需 ≥ 9.5)

**连续通过次数**: {new_passes}/10

### 评语

作为极其挑剔的艺术鉴赏家，我以最严格的标准审视这件作品。在本次以Superflat为主导风格的评估中，{'作品达到通过标准' if passed else '作品未能达到通过标准'}。

Superflat的核心美学包括：彻底消解三维空间深度、所有元素压缩在同一平面、高饱和度糖果色系、锐利轮廓线、图形化符号、日本传统装饰与流行文化融合、以及对消费主义的批判性反思。{'本作品在这些方面表现出色' if passed else '本作品在这些方面存在明显差距'}，{'达到' if passed else '未能达到'}9.5分的苛刻标准。

---

"""
    
    # Prepend to existing CHANGELOG
    with open(changelog_path, "r") as f:
        existing_content = f.read()
    
    # Remove the first line if it's just "# Changelog"
    if existing_content.startswith("# Changelog"):
        lines = existing_content.split("\n", 1)
        if len(lines) > 1:
            existing_content = lines[1]
    
    new_content = f"# Changelog - {artwork_name}\n{evaluation_entry}{existing_content}"
    
    with open(changelog_path, "w") as f:
        f.write(new_content)

print(f"Updated {len(results)} CHANGELOGs")
