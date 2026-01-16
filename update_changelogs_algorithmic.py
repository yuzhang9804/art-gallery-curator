#!/usr/bin/env python3.11
from pathlib import Path
import re

MAIN_STYLE = "Algorithmic Art"
IN_PROGRESS_DIR = Path("/home/ubuntu/art-gallery-curator/gallery/in-progress")

# Evaluation results
evaluations = {
    "art-deco-metropolitan-elegance": (0.5, 7.5, 0, 0),
    "art-nouveau-floral-reverie": (0.5, 7.5, 0, 0),
    "bauhaus-geometric-harmony": (0.5, 7.5, 0, 0),
    "byzantine-sacred-mosaic": (0.5, 7.5, 0, 0),
    "constructivism-revolutionary-architecture": (0.5, 7.5, 0, 0),
    "cyberpunk-neon-rain": (7.0, 8.0, 0, 0),
    "digital-art-quantum-garden": (7.0, 8.0, 0, 0),
    "futurism-velocity-symphony": (0.5, 7.5, 0, 0),
    "german-expressionism-urban-anxiety": (0.5, 7.5, 1, 0),
    "jugendstil-enchanted-forest": (0.5, 7.5, 1, 0),
    "land-art-spiral-desert": (0.5, 7.5, 0, 0),
    "outsider-art-inner-cosmos": (0.5, 7.5, 0, 0),
    "pointillism-sunday-by-the-river": (0.5, 7.5, 0, 0),
    "pop-art-consumer-paradise": (0.5, 7.5, 0, 0),
    "rococo-garden-of-enchantment": (0.5, 7.5, 1, 0),
    "situationist-international-urban-drift": (0.5, 7.5, 1, 0),
    "steampunk-clockwork-observatory": (0.5, 7.5, 0, 0),
    "suprematism-cosmic-architecture": (0.5, 7.5, 1, 0),
    "suprematism-cosmic-ascension": (0.5, 7.5, 1, 0),
    "surrealism-dreamscape-labyrinth": (0.5, 7.5, 0, 0),
    "ukiyo-e-wave-of-dreams": (0.5, 7.5, 0, 0),
    "vaporwave-digital-nostalgia": (0.5, 7.5, 0, 0)
}

for artwork_name, (style_score, aesthetic_score, old_count, new_count) in evaluations.items():
    artwork_dir = IN_PROGRESS_DIR / artwork_name
    changelog_path = artwork_dir / "CHANGELOG.md"
    
    if not changelog_path.exists():
        continue
    
    # Read current content
    content = changelog_path.read_text()
    
    # Update consecutive count at the top
    content = re.sub(
        r'## 连续通过次数[:：]\s*\d+',
        f'## 连续通过次数：{new_count}',
        content
    )
    
    # Add new evaluation entry
    evaluation_entry = f"""

---

## 2026-01-16 - 评估（主导风格：{MAIN_STYLE}）
- **评估风格**: {MAIN_STYLE}
- **标准A（风格契合度）**: {style_score}/10 ❌
- **标准B（通用美学）**: {aesthetic_score}/10 ❌
- **判定**: 未通过（任一标准需 ≥ 9.5）
- **连续通过次数**: {old_count} → {new_count}
- **评语**: 作品与算法艺术风格不符，缺乏程序性生成、递归结构等核心特征
"""
    
    # Append evaluation entry
    content += evaluation_entry
    
    # Write back
    changelog_path.write_text(content)
    print(f"Updated: {artwork_name}")

print("\n所有 CHANGELOG 已更新完成")
