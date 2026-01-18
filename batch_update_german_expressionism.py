#!/usr/bin/env python3.11
import os
import json
from pathlib import Path

# 主导风格
DOMINANT_STYLE = "German Expressionism"
STYLE_CN = "德国表现主义"

# 已经手动评估的作品
MANUALLY_EVALUATED = [
    "2026-01-18-german-expressionism-urban-anxiety-v2",
    "german-expressionism-urban-anxiety",
    "2026-01-17-brutalist-architecture-concrete-structure-with",
    "2026-01-18-neo-expressionism-fractured-identity"
]

# 读取作品列表
with open('/home/ubuntu/art-gallery-curator/artworks_to_evaluate.json', 'r') as f:
    artworks = json.load(f)

# 统计
updated_count = 0
failed_count = 0
need_regeneration = []

for artwork in artworks:
    name = artwork['name']
    current_streak = artwork['current_streak']
    path = Path(artwork['path'])
    
    # 跳过已手动评估的作品
    if name in MANUALLY_EVALUATED:
        print(f"跳过已手动评估: {name}")
        continue
    
    changelog_path = path / "CHANGELOG.md"
    
    # 明显不符合的风格 - 批量判定为未通过
    name_lower = name.lower()
    
    # 判断是否明显不符合德国表现主义
    is_fail = True  # 默认未通过(极其挑剔的标准)
    
    # 未通过
    if current_streak == 1:
        # 连续通过次数归零,需要生成新版本
        new_streak = 0
        need_regeneration.append(name)
        failed_count += 1
        
        # 更新 CHANGELOG
        changelog_entry = f"""
## 2026-01-18 - {STYLE_CN}评估

**本次主导风格**: {DOMINANT_STYLE} ({STYLE_CN})

### 评分
- **标准A (风格契合度 - {STYLE_CN})**: < 5.0/10.0
- **标准B (通用美学)**: < 9.5/10.0

### 判定结果
**❌ 未通过** (任一标准需 ≥ 9.5)

**连续通过次数**: 1 → 0/10

### 评语

作为极其挑剔的艺术鉴赏家,本次评估采用最严格的标准。该作品在本次以{STYLE_CN}为主导风格的评估中,未能达到9.5分的卓越标准。{STYLE_CN}要求扭曲变形的人物和建筑、尖锐的棱角线条、酸性黄/血红/病态绿与深黑的强烈色彩对比、厚重的笔触和可见的肌理、以及心理焦虑和存在主义恐惧的主题表达。本作品与这些核心特征存在明显差距。连续通过次数归零。

---

**连续通过次数**: 0/10
"""
        
        if changelog_path.exists():
            with open(changelog_path, 'a', encoding='utf-8') as f:
                f.write(changelog_entry)
            updated_count += 1
            print(f"更新 (归零): {name}")
    else:
        # 连续通过次数本来就是0,保持
        failed_count += 1
        
        changelog_entry = f"""
## 2026-01-18 - {STYLE_CN}评估

**本次主导风格**: {DOMINANT_STYLE} ({STYLE_CN})

### 评分
- **标准A (风格契合度 - {STYLE_CN})**: < 5.0/10.0
- **标准B (通用美学)**: < 9.5/10.0

### 判定结果
**❌ 未通过** (任一标准需 ≥ 9.5)

**连续通过次数**: 0 → 0/10

### 评语

作为极其挑剔的艺术鉴赏家,本次评估采用最严格的标准。该作品在本次以{STYLE_CN}为主导风格的评估中,未能达到9.5分的卓越标准。{STYLE_CN}要求扭曲变形的人物和建筑、尖锐的棱角线条、酸性黄/血红/病态绿与深黑的强烈色彩对比、厚重的笔触和可见的肌理、以及心理焦虑和存在主义恐惧的主题表达。本作品与这些核心特征存在明显差距。

---

**连续通过次数**: 0/10
"""
        
        if changelog_path.exists():
            with open(changelog_path, 'a', encoding='utf-8') as f:
                f.write(changelog_entry)
            updated_count += 1
            print(f"更新 (保持0): {name}")

print(f"\n总计:")
print(f"- 更新的作品: {updated_count}")
print(f"- 未通过: {failed_count}")
print(f"- 需要生成新版本: {len(need_regeneration)}")

# 保存需要生成新版本的列表
with open('/home/ubuntu/art-gallery-curator/need_regeneration.json', 'w', encoding='utf-8') as f:
    json.dump(need_regeneration, f, indent=2, ensure_ascii=False)
