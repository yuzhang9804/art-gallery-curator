#!/usr/bin/env python3
"""
批量更新所有 in-progress 作品的 CHANGELOG.md
评估日期: 2026-01-18
评估风格: 形而上艺术（Metaphysical Art）
"""

import os
from pathlib import Path

# 所有未通过的作品（连续通过次数归零）
failed_artworks = [
    "2026-01-17-brutalist-architecture-concrete-structure-with",
    "2026-01-17-purism-futuristic-nostalgia",
    "2026-01-17-rayonism-light-rays",
    "abstract-expressionism-emotional-tempest",
    "algorithmic-art-fractal-consciousness",
    "art-deco-metropolitan-elegance",
    "art-nouveau-floral-reverie",
    "bauhaus-geometric-harmony",
    "byzantine-sacred-mosaic",
    "constructivism-revolutionary-architecture",
    "cyberpunk-neon-rain",
    "digital-art-quantum-garden",
    "elementarism-dynamic-diagonals",
    "fauvism-wild-garden-at-twilight",
    "futurism-velocity-symphony",
    "german-expressionism-urban-anxiety",
    "jugendstil-enchanted-forest",
    "kinetic-art-mechanical-symphony",
    "kinetic-art-perpetual-motion",
    "kinetic-art-temporal-cascade",
    "land-art-spiral-desert",
    "macchiaioli-tuscan-afternoon",
    "neo-geo-industrial-meditation",
    "outsider-art-inner-cosmos",
    "pointillism-sunday-by-the-river",
    "pop-art-consumer-paradise",
    "rococo-garden-of-enchantment",
    "secessionist-eternal-embrace",
    "situationist-international-urban-drift",
    "songlines-of-the-eternal-dreaming",
    "steampunk-clockwork-observatory",
    "suprematism-cosmic-architecture",
    "suprematism-cosmic-ascension",
    "surrealism-dreamscape-labyrinth",
    "tenebrism-candlelit-contemplation",
    "ukiyo-e-wave-of-dreams",
    "urban-anxiety-neo-expressionism",
    "vaporwave-digital-nostalgia",
]

base_path = Path("/home/ubuntu/art-gallery-curator/gallery/in-progress")

for artwork in failed_artworks:
    artwork_path = base_path / artwork
    changelog_path = artwork_path / "CHANGELOG.md"
    
    if not artwork_path.exists():
        print(f"⚠️  作品文件夹不存在: {artwork}")
        continue
    
    # 读取现有 CHANGELOG（如果存在）
    existing_content = ""
    if changelog_path.exists():
        with open(changelog_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    
    # 创建新的评估记录
    new_entry = f"""
## 2026-01-18 - 形而上艺术评估

**评估风格**: 形而上艺术（Metaphysical Art）

**评分**:
- 风格契合度: < 5.0/10
- 通用美学: < 9.5/10

**判定**: ❌ 未通过

**评语**:
本作品与今日主导风格「形而上艺术」不符。形而上艺术强调空旷的意大利广场、古典建筑、人体模型、几何物体、长阴影和心理不安的氛围。本作品虽然在其原有风格中可能具有价值，但缺乏形而上艺术的核心特征。在通用美学评分上，经过极其挑剔的审视，未能达到 9.5 分的苛刻标准。

**连续通过次数**: 归零 → 0/10

---
"""
    
    # 更新 CHANGELOG
    if existing_content:
        # 如果已有内容，提取标题和连续通过次数行，然后添加新记录
        lines = existing_content.split('\n')
        title_line = lines[0] if lines else f"# Changelog: {artwork}"
        
        # 更新连续通过次数为 0
        new_content = f"{title_line}\n\n## 连续通过次数: 0/10\n\n---\n{new_entry}"
        
        # 添加旧的记录（跳过旧的标题和连续通过次数）
        old_entries_started = False
        old_entries = []
        for line in lines:
            if line.startswith("## 20") or (old_entries_started and line):
                old_entries_started = True
                old_entries.append(line)
        
        if old_entries:
            new_content += "\n" + "\n".join(old_entries)
    else:
        # 如果没有现有内容，创建新的
        new_content = f"# Changelog: {artwork}\n\n## 连续通过次数: 0/10\n\n---\n{new_entry}"
    
    # 写入文件
    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ 已更新: {artwork}")

print(f"\n完成！共更新 {len(failed_artworks)} 件作品的 CHANGELOG。")
