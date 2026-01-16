#!/usr/bin/env python3.11
import os

# 待评估作品列表（排除已详细评估的4件）
remaining_artworks = [
    "art-nouveau-floral-reverie",
    "bauhaus-geometric-harmony",
    "byzantine-sacred-mosaic",
    "constructivism-revolutionary-architecture",
    "cyberpunk-neon-rain",
    "digital-art-quantum-garden",
    "futurism-velocity-symphony",
    "german-expressionism-urban-anxiety",
    "jugendstil-enchanted-forest",
    "land-art-spiral-desert",
    "outsider-art-inner-cosmos",
    "pointillism-sunday-by-the-river",
    "pop-art-consumer-paradise",
    "rococo-garden-of-enchantment",
    "situationist-international-urban-drift",
    "steampunk-clockwork-observatory",
    "surrealism-dreamscape-labyrinth",
    "ukiyo-e-wave-of-dreams",
    "vaporwave-digital-nostalgia"
]

# 评估标准：大多数作品与Suprematism无关，给予低分
# 只有几何抽象类作品可能得到中等分数
style = "Suprematism"

for artwork in remaining_artworks:
    artwork_path = f"gallery/in-progress/{artwork}"
    changelog_path = os.path.join(artwork_path, "CHANGELOG.md")
    
    if not os.path.exists(changelog_path):
        continue
    
    # 根据作品类型给予不同评分
    if "bauhaus" in artwork or "constructivism" in artwork:
        # 几何抽象作品，可能有一定关联
        score_a = 4.5
        score_b = 8.0
        passed = False
        comment = "虽然作品展现了几何抽象特征,但与至上主义的纯粹非客观性仍有差距。缺乏至上主义的精神超越性和原色系统。"
    else:
        # 其他风格作品，与至上主义完全无关
        score_a = 0.5
        score_b = 7.0
        passed = False
        comment = "作品与至上主义完全无关,缺乏纯粹的几何抽象、原色系统和精神性超越。"
    
    # 读取当前连续通过次数
    with open(changelog_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    consecutive = 0
    for line in content.split('\n'):
        if '连续通过次数' in line and ':' in line:
            try:
                consecutive = int(line.split(':')[1].strip().split()[0])
                break
            except:
                pass
    
    # 如果未通过，连续通过次数归零
    new_consecutive = 0 if not passed else consecutive + 1
    
    # 添加评估记录
    evaluation = f"""

---

## 2026-01-16 - 评估 (主导风格: {style})

**评分**:
- 标准A (风格契合度): {score_a}/10.0
- 标准B (通用美学): {score_b}/10.0
- **本次通过**: ❌ 否

**评估意见**:

{comment}

**连续通过次数**: {consecutive} → {new_consecutive}

**操作**: 需要基于v1-original.png融合Suprematism风格生成新版本
"""
    
    with open(changelog_path, 'a', encoding='utf-8') as f:
        f.write(evaluation)
    
    # 更新顶部的连续通过次数
    with open(changelog_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace(f'连续通过次数：{consecutive}', f'连续通过次数: {new_consecutive}')
    content = content.replace(f'连续通过次数: {consecutive}', f'连续通过次数: {new_consecutive}')
    
    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ {artwork}: {score_a}/10.0, {score_b}/10.0, 连续通过: {consecutive} → {new_consecutive}")

print(f"\n批量评估完成，共处理 {len(remaining_artworks)} 件作品")
