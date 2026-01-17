import os
from datetime import datetime

# List of all failed artworks that need CHANGELOG updates
artworks = [
    "abstract-expressionism-emotional-tempest",
    "algorithmic-art-fractal-consciousness",
    "art-deco-metropolitan-elegance",
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
    "suprematism-cosmic-architecture",
    "suprematism-cosmic-ascension",
    "surrealism-dreamscape-labyrinth",
    "ukiyo-e-wave-of-dreams",
    "vaporwave-digital-nostalgia"
]

base_path = "gallery/in-progress"

for artwork in artworks:
    changelog_path = os.path.join(base_path, artwork, "CHANGELOG.md")
    
    # Read existing CHANGELOG if it exists
    if os.path.exists(changelog_path):
        with open(changelog_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    else:
        existing_content = f"# Changelog: {artwork.replace('-', ' ').title()}\n\n"
    
    # Prepare new entry
    new_entry = f"""## 连续通过次数: 0/10

---

## 2026-01-16 | Evaluation with Elementarism

**主导风格**: Elementarism

**评估结果**: ❌ **未通过**

**馆长评语**:

本次评估以元素主义（Elementarism）为主导风格。该作品虽然在其原有风格上有一定的艺术价值，但与元素主义的核心理念——对角线构图、几何纯粹性和动态平衡——相去甚远。因此在风格契合度上得分极低，未能达到通过标准（任一标准 ≥ 9.5）。

**连续通过次数**: 已归零 → 0

**新版本**: 已生成融合 Elementarism 风格的新版本

---

"""
    
    # Update CHANGELOG
    # Remove old "连续通过次数" line if exists
    lines = existing_content.split('\n')
    new_lines = []
    skip_count_line = False
    for line in lines:
        if line.startswith('## 连续通过次数:'):
            skip_count_line = True
            continue
        if skip_count_line and line.strip() == '':
            skip_count_line = False
            continue
        new_lines.append(line)
    
    # Reconstruct content
    if new_lines[0].startswith('# Changelog:'):
        final_content = new_lines[0] + '\n\n' + new_entry + '\n'.join(new_lines[2:])
    else:
        final_content = new_entry + '\n'.join(new_lines)
    
    # Write updated CHANGELOG
    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"Updated: {artwork}")

print("\nAll CHANGELOGs updated successfully!")
