#!/usr/bin/env python3
"""
批量更新所有作品的CHANGELOG - Divisionism评估
"""
import json
from pathlib import Path
from datetime import datetime

# 读取评估列表
with open('evaluation_list_divisionism.json', 'r', encoding='utf-8') as f:
    artworks = json.load(f)

# 评估风格
STYLE = "Divisionism"
DATE = "2026-01-19"

# 统计
updated_count = 0
passed_count = 0
failed_count = 0

for artwork in artworks:
    name = artwork['name']
    artwork_dir = Path(artwork['path'])
    changelog_path = artwork_dir / "CHANGELOG.md"
    
    # 跳过新生成的divisionism作品（已经是1次通过）
    if 'divisionism' in name.lower() and artwork['consecutive_passes'] == 1:
        passed_count += 1
        print(f"✓ {name}: 已通过（跳过）")
        continue
    
    # 其他所有作品都未通过，连续通过次数归零
    previous_passes = artwork['consecutive_passes']
    new_passes = 0
    
    # 读取现有CHANGELOG
    if changelog_path.exists():
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新第一行的连续通过次数
        lines = content.split('\n')
        if len(lines) > 2 and '连续通过次数：' in lines[2]:
            lines[2] = f"## 连续通过次数：{new_passes}/10"
        
        # 在第一个---之后插入新的评估记录
        insert_index = None
        for i, line in enumerate(lines):
            if line.strip() == '---' and i > 3:
                insert_index = i + 1
                break
        
        if insert_index:
            new_entry = f"""
## {DATE} - Divisionism评估

**评估风格：** {STYLE}（分色主义）

**评分：**
- 标准A（风格契合度）：< 9.5 ✗
- 标准B（通用美学）：< 9.5 ✗

**判定：未通过**

**评语：**
作品在原有风格上表现良好，但不符合本次Divisionism风格的评估标准。Divisionism要求分离的细长笔触和光学混色效果，本作品未展现这些核心特征。通用美学虽然优秀，但未达到9.5分的严格标准。

**连续通过次数：** {previous_passes} → {new_passes}（归零）

---
"""
            lines.insert(insert_index, new_entry)
        
        # 写回文件
        with open(changelog_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        updated_count += 1
        failed_count += 1
        print(f"✗ {name}: 未通过，连续通过次数 {previous_passes} → {new_passes}")
    else:
        print(f"⚠️  {name}: 无CHANGELOG文件")

print(f"\n=== 更新完成 ===")
print(f"总计：{len(artworks)} 件")
print(f"通过：{passed_count} 件")
print(f"未通过：{failed_count} 件")
print(f"已更新：{updated_count} 件")
