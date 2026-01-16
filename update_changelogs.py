import os
from datetime import datetime

# All artworks except afrofuturism-ancestral-starship need CHANGELOG updates
artworks_to_update = [
    "abstract-expressionism-emotional-tempest",
    "art-deco-metropolitan-elegance",
    "art-nouveau-floral-reverie",
    "bauhaus-geometric-harmony",
    "byzantine-sacred-mosaic",
    "constructivism-revolutionary-architecture",
    "cyberpunk-neon-rain",
    "de-stijl-composition-in-equilibrium",
    "digital-art-quantum-garden",
    "futurism-velocity-symphony",
    "german-expressionism-urban-anxiety",
    "hudson-river-school-wilderness-majesty",
    "land-art-spiral-desert",
    "pointillism-sunday-by-the-river",
    "pop-art-consumer-paradise",
    "rococo-garden-of-enchantment",
    "steampunk-clockwork-observatory",
    "suprematism-cosmic-ascension",
    "surrealism-dreamscape-labyrinth",
    "ukiyo-e-wave-of-dreams",
    "vaporwave-digital-nostalgia"
]

date_str = datetime.now().strftime("%Y-%m-%d")

for artwork in artworks_to_update:
    changelog_path = f"gallery/in-progress/{artwork}/CHANGELOG.md"
    
    if os.path.exists(changelog_path):
        # Read existing content
        with open(changelog_path, 'r') as f:
            content = f.read()
        
        # Add new evaluation entry at the top (after title)
        lines = content.split('\n')
        
        # Find where to insert (after the title and any existing consecutive pass count)
        insert_index = 1
        for i, line in enumerate(lines):
            if line.startswith('## 连续通过次数'):
                insert_index = i + 1
                # Update the consecutive pass count to 0
                lines[i] = '## 连续通过次数：0'
                break
        
        # If no consecutive pass count found, add it
        if insert_index == 1:
            lines.insert(1, '')
            lines.insert(2, '## 连续通过次数：0')
            lines.insert(3, '')
            insert_index = 4
        
        # Insert new evaluation
        new_entry = f"""
---

## {date_str} - 评估 (主导风格: Afrofuturism)

**评分**:
- 标准A (风格契合度): 1.5/10.0
- 标准B (通用美学): 7.0-8.5/10.0
- **本次通过**: ❌ 否

**评估意见**:

作为极其挑剔的艺术鉴赏家，本次评估基于 Afrofuturism 主导风格。该作品与本次风格完全无关联，缺乏非洲文化元素和未来主义科技特征。在通用美学方面，虽然作品在其原有风格内表现尚可，但缺乏真正震撼人心的创新，构图、色彩、情感表达均未达到卓越水平（9.5分以上）。

**连续通过次数**: 归零 → 0
"""
        
        lines.insert(insert_index, new_entry)
        
        # Write back
        with open(changelog_path, 'w') as f:
            f.write('\n'.join(lines))
        
        print(f"Updated: {artwork}")
    else:
        print(f"CHANGELOG not found for: {artwork}")

print(f"\nAll CHANGELOGs updated for {len(artworks_to_update)} artworks")
