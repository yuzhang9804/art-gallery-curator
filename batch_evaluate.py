#!/usr/bin/env python3
import json
import random
from pathlib import Path

# 读取评估列表
with open('evaluation_list_divisionism.json', 'r', encoding='utf-8') as f:
    artworks = json.load(f)

# 今日风格：Divisionism
today_style = "Divisionism"

# 评估结果
results = []

for artwork in artworks:
    name = artwork['name']
    consecutive_passes = artwork['consecutive_passes']
    
    # 模拟评分（实际需要人工评估）
    # 这里只是创建数据结构
    result = {
        "name": name,
        "image_path": artwork['image'],
        "previous_consecutive_passes": consecutive_passes,
        "style_score": None,  # 待填写
        "aesthetic_score": None,  # 待填写
        "passed": None,  # 待判定
        "new_consecutive_passes": None,  # 待计算
        "action": None  # 待确定
    }
    results.append(result)

# 保存评估模板
with open('evaluation_template_divisionism.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"已创建评估模板，共 {len(results)} 件作品")
print("文件：evaluation_template_divisionism.json")
