from pathlib import Path

artworks_updated = [
    ("byzantine-sacred-mosaic", "v6-tonalism-fusion.png"),
    ("rococo-garden-of-enchantment", "v6-tonalism-fusion.png"),
    ("steampunk-clockwork-observatory", "v8-tonalism-fusion.png")
]

IN_PROGRESS_DIR = Path("/home/ubuntu/art-gallery-curator/gallery/in-progress")

for artwork_name, new_version in artworks_updated:
    changelog_path = IN_PROGRESS_DIR / artwork_name / "CHANGELOG.md"
    
    if changelog_path.exists():
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the last evaluation entry and add generation note
        generation_note = f"""
**新版本生成**: {new_version}（基于 v1-original.png 融合 Tonalism 风格）

---

"""
        
        # Insert after the first evaluation entry
        parts = content.split('---', 2)
        if len(parts) >= 2:
            new_content = parts[0] + '---' + parts[1] + '---' + generation_note + (parts[2] if len(parts) > 2 else '')
            
            with open(changelog_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✓ Updated {artwork_name} CHANGELOG with {new_version}")

print("\nFusion version CHANGELOGs updated")
