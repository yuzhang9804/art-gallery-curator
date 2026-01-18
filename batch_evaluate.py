import os
import json
from pathlib import Path

# 主导风格
DOMINANT_STYLE = "German Expressionism"

# 获取所有 in-progress 作品
in_progress_dir = Path("/home/ubuntu/art-gallery-curator/gallery/in-progress")
artworks = [d for d in in_progress_dir.iterdir() if d.is_dir()]

results = []

for artwork_dir in artworks:
    artwork_name = artwork_dir.name
    changelog_path = artwork_dir / "CHANGELOG.md"
    
    # 读取 CHANGELOG 获取当前连续通过次数
    current_streak = 0
    if changelog_path.exists():
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 查找最近的连续通过次数
            if "连续通过次数**: 1/10" in content or "连续通过次数**: 1 " in content:
                current_streak = 1
            elif "连续通过次数**: 0" in content or "连续通过次数**: → 0" in content:
                current_streak = 0
    
    # 检查是否有 v1-original.png
    v1_original = artwork_dir / "v1-original.png"
    has_original = v1_original.exists()
    
    results.append({
        "name": artwork_name,
        "current_streak": current_streak,
        "has_original": has_original,
        "path": str(artwork_dir)
    })

# 保存结果
output_path = "/home/ubuntu/art-gallery-curator/artworks_to_evaluate.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Found {len(results)} artworks")
print(f"Results saved to {output_path}")
