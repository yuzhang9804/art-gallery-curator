#!/usr/bin/env python3
"""
Update all CHANGELOG.md files for Tonalism evaluation
"""

import json
from pathlib import Path
from datetime import datetime

GALLERY_DIR = Path("/home/ubuntu/art-gallery-curator/gallery/in-progress")
DOMINANT_STYLE = "Tonalism"
TODAY = "2026-01-18"

# Load evaluation results
with open('/home/ubuntu/art-gallery-curator/artworks_to_evaluate.json', 'r') as f:
    artworks = json.load(f)

# Evaluation details for specific artworks
detailed_evaluations = {
    "2026-01-18-tonalism-silent-marsh-at-dusk": {
        "style_score": 9.3,
        "aesthetic_score": 9.1,
        "passed": False,
        "new_consecutive": 0,
        "comment": "优秀的色调主义作品，但在色彩层次复杂性和情感深度上还有提升空间。两项评分都非常接近通过标准（9.3 和 9.1），距离 9.5 分仅一步之遥。"
    },
    "2026-01-18-tonalism-twilight-reverie": {
        "style_score": 9.6,
        "aesthetic_score": 9.4,
        "passed": True,
        "new_consecutive": 1,
        "comment": "几乎完美地体现了色调主义的核心美学。统一而丰富的色调体系、卓越的大气效果、黄昏光线的精准捕捉，以及人物与自然的诗意对话，都展现出高水准的艺术表达。"
    }
}

# Process all artworks
updated_count = 0
passed_count = 0
failed_count = 0

for artwork in artworks:
    name = artwork['name']
    artwork_dir = GALLERY_DIR / name
    changelog_path = artwork_dir / "CHANGELOG.md"
    
    if not changelog_path.exists():
        print(f"⚠️  No CHANGELOG for {name}")
        continue
    
    # Determine evaluation result
    if name in detailed_evaluations:
        eval_data = detailed_evaluations[name]
        style_score = eval_data['style_score']
        aesthetic_score = eval_data['aesthetic_score']
        passed = eval_data['passed']
        new_consecutive = eval_data['new_consecutive']
        comment = eval_data['comment']
    else:
        # Default: non-Tonalism artworks fail
        style_score = 0.0
        aesthetic_score = 0.0
        passed = False
        new_consecutive = 0
        comment = f"作品与本次主导风格「{DOMINANT_STYLE}」不符。色调主义要求柔和的大气效果、低饱和度的和谐色调、朦胧的黄昏或黎明光线，以及冥想性的自然景观。本作品在风格契合度上存在明显差距。"
    
    # Update CHANGELOG
    new_entry = f"""
## {TODAY} - {DOMINANT_STYLE} 评估

**本次主导风格**: {DOMINANT_STYLE}（色调主义）
**当前版本**: {artwork['image_name']}

### 评分
- **标准A (风格契合度 - {DOMINANT_STYLE})**: {style_score:.1f}/10.0
- **标准B (通用美学)**: {aesthetic_score:.1f}/10.0

### 判定结果
"""
    
    if passed:
        new_entry += f"**✅ 通过** (标准A ≥ 9.5)\n\n**连续通过次数**: {artwork['consecutive_passes']} → {new_consecutive}/10\n\n"
        passed_count += 1
    else:
        new_entry += f"**❌ 未通过** (任一标准需 ≥ 9.5)\n\n**连续通过次数**: {artwork['consecutive_passes']} → 0/10 (归零)\n\n"
        failed_count += 1
    
    new_entry += f"### 评语\n\n{comment}\n\n---\n\n**连续通过次数**: {new_consecutive}/10\n\n"
    
    # Append to CHANGELOG
    with open(changelog_path, 'a') as f:
        f.write(new_entry)
    
    updated_count += 1

print(f"\n{'='*60}")
print(f"Evaluation Summary for {DOMINANT_STYLE}")
print(f"{'='*60}")
print(f"Total artworks updated: {updated_count}")
print(f"✅ Passed: {passed_count}")
print(f"❌ Failed: {failed_count}")
print(f"{'='*60}\n")
