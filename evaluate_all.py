#!/usr/bin/env python3.11
import os
import glob

MAIN_STYLE = "Secessionist Art"
MAIN_STYLE_CN = "维也纳分离派"
DATE = "2026-01-17"

base_path = "/home/ubuntu/art-gallery-curator/gallery/in-progress"

# Evaluation data for each artwork (based on strict criteria)
# Format: (style_A_score, aesthetics_B_score, passes, comment)
evaluations = {
    "algorithmic-art-fractal-consciousness": (0.5, 7.5, False, "算法艺术作品与分离派装饰美学完全无关，缺乏金色装饰和几何有机融合"),
    "art-deco-metropolitan-elegance": (6.5, 9.0, False, "装饰艺术的几何简洁与分离派的有机装饰存在本质差异，缺乏金箔和花卉元素"),
    "art-nouveau-floral-reverie": (7.5, 9.2, False, "新艺术运动与分离派有共通之处，但缺乏分离派标志性的金色装饰和几何图案融合"),
    "bauhaus-geometric-harmony": (3.0, 8.5, False, "包豪斯的功能主义与分离派的装饰性完全对立，缺乏任何装饰元素"),
    "byzantine-sacred-mosaic": (8.0, 9.0, False, "拜占庭马赛克与分离派有共同的金色和神圣感，但缺乏新艺术运动的有机曲线"),
    "constructivism-revolutionary-architecture": (1.0, 7.8, False, "构成主义的革命性与分离派的装饰性完全相反"),
    "cyberpunk-neon-rain": (0.5, 8.5, False, "赛博朋克科幻美学与1900年代装饰艺术毫无关联"),
    "digital-art-quantum-garden": (2.0, 8.0, False, "数字艺术的科技感与分离派的手工装饰性无关"),
    "elementarism-dynamic-diagonals": (3.5, 8.0, False, "元素主义的对角线构图与分离派的装饰性差异巨大"),
    "futurism-velocity-symphony": (1.5, 8.2, False, "未来主义的速度感与分离派的静态装饰性完全对立"),
    "german-expressionism-urban-anxiety": (4.0, 8.5, False, "德国表现主义的扭曲焦虑与分离派的优雅装饰性差异明显"),
    "jugendstil-enchanted-forest": (9.0, 9.3, False, "青年风格与分离派极为接近但缺乏金色装饰，未达9.5分阈值"),
    "land-art-spiral-desert": (0.5, 8.8, False, "大地艺术与室内装饰性分离派完全无关"),
    "outsider-art-inner-cosmos": (0.5, 7.5, False, "局外人艺术的原始性与分离派的精致装饰性完全对立"),
    "pointillism-sunday-by-the-river": (2.0, 9.0, False, "点彩派的光学科学与分离派的装饰性无关"),
    "pop-art-consumer-paradise": (1.0, 8.0, False, "波普艺术的消费文化与分离派的精英装饰性完全不同"),
    "rococo-garden-of-enchantment": (5.5, 9.0, False, "洛可可的装饰性与分离派有相似之处，但时代和风格语言差异明显"),
    "secessionist-eternal-embrace": (9.7, 9.6, True, "完美呈现分离派风格，金色装饰、几何与有机融合、拜占庭影响俱佳"),
    "situationist-international-urban-drift": (0.5, 7.5, False, "情境主义的政治批判与分离派的装饰美学完全无关"),
    "steampunk-clockwork-observatory": (4.0, 9.0, False, "蒸汽朋克的工业美学与分离派的新艺术装饰性差异明显"),
    "suprematism-cosmic-architecture": (2.0, 8.0, False, "至上主义的几何纯粹与分离派的装饰性完全对立"),
    "suprematism-cosmic-ascension": (2.0, 8.0, False, "至上主义的抽象与分离派的装饰性完全对立"),
    "surrealism-dreamscape-labyrinth": (3.0, 8.8, False, "超现实主义的潜意识与分离派的装饰理性差异明显"),
    "tenebrism-candlelit-contemplation": (2.5, 8.5, False, "明暗对照法的戏剧性与分离派的平面装饰性完全不同"),
    "ukiyo-e-wave-of-dreams": (4.0, 9.2, False, "浮世绘的平面性与分离派有相似之处，但文化和装饰语言差异巨大"),
    "vaporwave-digital-nostalgia": (1.0, 7.8, False, "蒸汽波的数字怀旧与分离派的手工装饰性无关"),
}

# Generate evaluation entries
for artwork, (score_a, score_b, passes, comment) in evaluations.items():
    changelog_path = os.path.join(base_path, artwork, "CHANGELOG.md")
    
    if not os.path.exists(changelog_path):
        print(f"SKIP: {artwork} (no CHANGELOG)")
        continue
    
    # Read current consecutive passes
    with open(changelog_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract current consecutive passes
    current_passes = 0
    for line in content.split('\n'):
        if "连续通过次数" in line and "/" in line:
            try:
                parts = line.split(':')[-1].split('：')[-1].strip()
                current_passes = int(parts.split('/')[0].strip())
                break
            except:
                pass
    
    # Calculate new consecutive passes
    if passes:
        new_passes = current_passes + 1
    else:
        new_passes = 0
    
    # Generate evaluation entry
    status_emoji = "✓" if passes else "❌"
    
    evaluation_text = f"""
---

## {DATE} - 评估（主导风格：{MAIN_STYLE_CN} {MAIN_STYLE}）

**评分**:
- 标准A (风格契合度): {score_a}/10.0
- 标准B (通用美学): {score_b}/10.0
- **本次通过**: {status_emoji} {'是' if passes else '否'}

**评估意见**:

{comment}

**连续通过次数**: {current_passes} → {new_passes}/10

"""
    
    # Append to CHANGELOG
    with open(changelog_path, 'a', encoding='utf-8') as f:
        f.write(evaluation_text)
    
    print(f"{'PASS' if passes else 'FAIL'}: {artwork} ({current_passes} → {new_passes})")

print("\n=== Evaluation Summary ===")
print(f"Total artworks: {len(evaluations)}")
print(f"Passed: {sum(1 for _, _, p, _ in evaluations.values() if p)}")
print(f"Failed: {sum(1 for _, _, p, _ in evaluations.values() if not p)}")
