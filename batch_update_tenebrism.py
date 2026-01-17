#!/usr/bin/env python3
import os
from datetime import datetime

# 评估数据 - 基于Tenebrism主导风格
evaluations = {
    "abstract-expressionism-emotional-tempest": {"A": 0.5, "B": 8.2, "pass": False, "streak": 0},
    "algorithmic-art-fractal-consciousness": {"A": 0.5, "B": 9.3, "pass": False, "streak": 0},
    "art-deco-metropolitan-elegance": {"A": 1.0, "B": 9.7, "pass": True, "streak": "+1"},
    "art-nouveau-floral-reverie": {"A": 2.0, "B": 9.6, "pass": True, "streak": "+1"},
    "bauhaus-geometric-harmony": {"A": 0.5, "B": 9.0, "pass": False, "streak": 0},
    "byzantine-sacred-mosaic": {"A": 3.5, "B": 9.4, "pass": False, "streak": 0},
    "constructivism-revolutionary-architecture": {"A": 0.5, "B": 8.8, "pass": False, "streak": 0},
    "cyberpunk-neon-rain": {"A": 1.5, "B": 9.5, "pass": True, "streak": "+1"},
    "digital-art-quantum-garden": {"A": 1.0, "B": 9.4, "pass": False, "streak": 0},
    "elementarism-dynamic-diagonals": {"A": 0.5, "B": 8.7, "pass": False, "streak": 0},
    "futurism-velocity-symphony": {"A": 0.5, "B": 9.2, "pass": False, "streak": 0},
    "german-expressionism-urban-anxiety": {"A": 4.0, "B": 9.3, "pass": False, "streak": 0},
    "jugendstil-enchanted-forest": {"A": 2.5, "B": 9.6, "pass": True, "streak": "+1"},
    "land-art-spiral-desert": {"A": 1.0, "B": 9.1, "pass": False, "streak": 0},
    "outsider-art-inner-cosmos": {"A": 1.5, "B": 8.5, "pass": False, "streak": 0},
    "pointillism-sunday-by-the-river": {"A": 1.5, "B": 9.5, "pass": True, "streak": "+1"},
    "pop-art-consumer-paradise": {"A": 0.5, "B": 8.9, "pass": False, "streak": 0},
    "rococo-garden-of-enchantment": {"A": 2.0, "B": 9.7, "pass": True, "streak": "+1"},
    "situationist-international-urban-drift": {"A": 1.0, "B": 8.6, "pass": False, "streak": 0},
    "steampunk-clockwork-observatory": {"A": 2.5, "B": 9.5, "pass": True, "streak": "+1"},
    "suprematism-cosmic-architecture": {"A": 0.5, "B": 8.5, "pass": False, "streak": 0},
    "suprematism-cosmic-ascension": {"A": 0.5, "B": 8.7, "pass": False, "streak": 0},
    "surrealism-dreamscape-labyrinth": {"A": 5.0, "B": 9.6, "pass": True, "streak": "+1"},
    "ukiyo-e-wave-of-dreams": {"A": 1.5, "B": 9.8, "pass": True, "streak": "+1"},
    "vaporwave-digital-nostalgia": {"A": 1.0, "B": 9.0, "pass": False, "streak": 0},
    "tenebrism-candlelit-contemplation": {"A": 9.8, "B": 9.9, "pass": True, "streak": 1}
}

base_path = "/home/ubuntu/art-gallery-curator/gallery/in-progress"

for artwork, data in evaluations.items():
    changelog_path = os.path.join(base_path, artwork, "CHANGELOG.md")
    
    if not os.path.exists(changelog_path):
        print(f"跳过 {artwork} - CHANGELOG不存在")
        continue
    
    # 读取现有内容
    with open(changelog_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取当前连续通过次数
    import re
    match = re.search(r'连续通过次数[：:]\s*(\d+)', content)
    current_streak = int(match.group(1)) if match else 0
    
    # 计算新的连续通过次数
    if data["pass"]:
        new_streak = current_streak + 1
    else:
        new_streak = 0
    
    # 准备新的评估记录
    new_entry = f"""
---

## 2026-01-16 - 评估 (主导风格: Tenebrism)

**评分**:
- 标准A (风格契合度): {data['A']}/10.0
- 标准B (通用美学): {data['B']}/10.0
- **本次通过**: {'✅ 是' if data['pass'] else '❌ 否'}

**连续通过次数**: {current_streak} → {new_streak}

"""
    
    # 更新文件 - 在第一个 ## 之前插入
    lines = content.split('\n')
    insert_pos = 0
    for i, line in enumerate(lines):
        if line.startswith('## ') and i > 0:
            insert_pos = i
            break
    
    if insert_pos > 0:
        # 更新顶部的连续通过次数
        new_lines = []
        for i, line in enumerate(lines):
            if '连续通过次数' in line and i < 10:
                new_lines.append(f"## 连续通过次数: {new_streak}/10")
            else:
                new_lines.append(line)
        
        lines = new_lines
        lines.insert(insert_pos, new_entry)
        
        with open(changelog_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"✓ {artwork}: {current_streak} → {new_streak}")
    else:
        print(f"⚠ {artwork}: 无法找到插入位置")

print("\n批量更新完成")
