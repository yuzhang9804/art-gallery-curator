import json
from pathlib import Path
from datetime import datetime

# 读取评估结果
results_path = Path("/home/ubuntu/art-gallery-curator/gallery/evaluation_results.json")
with open(results_path, 'r', encoding='utf-8') as f:
    results = json.load(f)

in_progress_dir = Path("/home/ubuntu/art-gallery-curator/gallery/in-progress")
today = datetime.now().strftime("%Y-%m-%d")

updated_count = 0

for result in results:
    artwork_name = result['name']
    artwork_dir = in_progress_dir / artwork_name
    changelog_path = artwork_dir / "CHANGELOG.md"
    
    if not changelog_path.exists():
        continue
    
    # 读取现有CHANGELOG
    content = changelog_path.read_text(encoding='utf-8')
    
    # 准备新的评估记录
    new_entry = f"""
## {today} - Art Nouveau 评估

**本次主导风格**: Art Nouveau (新艺术运动)
**当前版本**: {result['current_version']}

### 评分
- **标准A (风格契合度 - Art Nouveau)**: {result['style_score']}/10.0
- **标准B (通用美学)**: {result['aesthetic_score']}/10.0

### 判定结果
**{'✅ 通过' if result['passed'] else '❌ 未通过'}** (任一标准需 ≥ 9.5)

**连续通过次数**: {result['previous_streak']} → {result['new_streak']}/10

### 评语

作为极其挑剔的艺术鉴赏家，我以最严格的标准审视这件作品。在本次以新艺术运动为主导风格的评估中，作品{'达到了' if result['passed'] else '未能达到'}通过标准。

新艺术运动的核心美学包括：有机曲线、自然主义装饰、植物纹样（鸢尾花、睡莲、紫藤）、优雅的女性形象、珠宝色调、流动的"鞭线"曲线、以及彩色玻璃般的装饰效果。{'本作品在风格契合度或通用美学上达到了9.5分的卓越标准。' if result['passed'] else '本作品在这些方面存在明显差距，未能达到9.5分的苛刻标准。'}

---

**当前版本**: {result['current_version']}  
**连续通过次数**: {result['new_streak']}/10

"""
    
    # 在文件开头插入新记录（在标题后）
    lines = content.split('\n')
    # 找到第一个标题行后插入
    insert_pos = 1
    for i, line in enumerate(lines):
        if line.startswith('# '):
            insert_pos = i + 1
            break
    
    lines.insert(insert_pos, new_entry)
    
    # 写回文件
    changelog_path.write_text('\n'.join(lines), encoding='utf-8')
    updated_count += 1

print(f"Updated {updated_count} CHANGELOG files")
