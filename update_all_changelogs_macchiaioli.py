#!/usr/bin/env python3
"""
Batch update all CHANGELOG files with Macchiaioli evaluation results
"""

import json
import os
from pathlib import Path

# Load evaluation results
with open('/home/ubuntu/art-gallery-curator/macchiaioli_evaluation_results.json', 'r', encoding='utf-8') as f:
    evaluations = json.load(f)

gallery_path = Path('/home/ubuntu/art-gallery-curator/gallery/in-progress')

for artwork_name, eval_data in evaluations.items():
    artwork_path = gallery_path / artwork_name
    changelog_path = artwork_path / 'CHANGELOG.md'
    
    if not changelog_path.exists():
        print(f"⚠️  CHANGELOG not found for {artwork_name}")
        continue
    
    # Prepare evaluation entry
    status_icon = "✅" if eval_data['passed'] else "❌"
    
    eval_entry = f"""
## 2026-01-17 - Macchiaioli 评估

**本次主导风格**: Macchiaioli (斑点画派)

### 评分

- **标准A (风格契合度 - Macchiaioli)**: {eval_data['style_fit']}/10.0
- **标准B (通用美学)**: {eval_data['aesthetics']}/10.0

### 判定结果

**{status_icon} {'通过' if eval_data['passed'] else '未通过'}** (任一标准需 ≥ 9.5)

**连续通过次数**: {eval_data['consecutive']}/10

### 评语

{eval_data['comment']}

---

**连续通过次数**: {eval_data['consecutive']}/10
"""
    
    # Append to CHANGELOG
    with open(changelog_path, 'a', encoding='utf-8') as f:
        f.write(eval_entry)
    
    print(f"✓ Updated {artwork_name}")

print("\n✅ All CHANGELOGs updated successfully!")
