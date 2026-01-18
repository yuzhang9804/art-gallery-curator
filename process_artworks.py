#!/usr/bin/env python3.11
"""
作品处理脚本：根据评估结果更新 CHANGELOG 和生成新版本
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime

# 读取评估结果
with open('/home/ubuntu/art-gallery-curator/detailed_evaluation_results.json', 'r', encoding='utf-8') as f:
    evaluation_data = json.load(f)

results = evaluation_data['results']
dominant_style = evaluation_data['dominant_style']

# 统计信息
actions = {
    'updated_passed': [],  # 通过，更新连续通过次数
    'updated_failed': [],  # 未通过，连续通过次数归零
    'to_generate': [],     # 需要生成新版本的作品
    'to_perfect': []       # 晋升到 perfect 的作品
}

# 处理每个作品
for result in results:
    artwork_name = result['name']
    passed = result['passed']
    consecutive_passes = result['consecutive_passes']
    
    artwork_dir = Path(f"/home/ubuntu/art-gallery-curator/gallery/in-progress/{artwork_name}")
    changelog_path = artwork_dir / "CHANGELOG.md"
    
    if not changelog_path.exists():
        print(f"警告: {artwork_name} 缺少 CHANGELOG.md，跳过")
        continue
    
    # 读取现有 CHANGELOG
    with open(changelog_path, 'r', encoding='utf-8') as f:
        changelog_content = f.read()
    
    # 更新连续通过次数
    if passed:
        new_consecutive = consecutive_passes + 1
        
        # 检查是否达到完美标准（10次）
        if new_consecutive >= 10:
            actions['to_perfect'].append({
                'name': artwork_name,
                'consecutive': new_consecutive
            })
        else:
            actions['updated_passed'].append({
                'name': artwork_name,
                'consecutive': new_consecutive,
                'style_score': result['style_score'],
                'aesthetic_score': result['aesthetic_score']
            })
        
        # 更新 CHANGELOG
        # 更新连续通过次数
        if '连续通过次数：' in changelog_content:
            changelog_content = re.sub(
                r'## 连续通过次数：\d+',
                f'## 连续通过次数：{new_consecutive}',
                changelog_content
            )
        else:
            # 如果没有找到，在文件开头添加
            changelog_content = f"# Changelog: {artwork_name}\n\n## 连续通过次数：{new_consecutive}\n\n" + changelog_content
        
        # 添加新的评估记录
        today = datetime.now().strftime('%Y-%m-%d')
        new_entry = f"\n## {today} - 评估通过\n"
        new_entry += f"- **主导风格**: {dominant_style}\n"
        new_entry += f"- **风格契合度**: {result['style_score']}/10\n"
        new_entry += f"- **通用美学**: {result['aesthetic_score']}/10\n"
        new_entry += f"- **连续通过次数**: {consecutive_passes} → {new_consecutive}\n"
        new_entry += f"- **评语**: {result['comments']}\n"
        
        changelog_content += new_entry
        
    else:
        # 未通过，连续通过次数归零
        new_consecutive = 0
        
        actions['updated_failed'].append({
            'name': artwork_name,
            'previous_consecutive': consecutive_passes,
            'style_score': result['style_score'],
            'aesthetic_score': result['aesthetic_score']
        })
        
        # 如果之前有连续通过次数，需要生成新版本
        if consecutive_passes > 0:
            actions['to_generate'].append({
                'name': artwork_name,
                'style': result['style']
            })
        
        # 更新 CHANGELOG
        if '连续通过次数：' in changelog_content:
            changelog_content = re.sub(
                r'## 连续通过次数：\d+',
                f'## 连续通过次数：0',
                changelog_content
            )
        else:
            changelog_content = f"# Changelog: {artwork_name}\n\n## 连续通过次数：0\n\n" + changelog_content
        
        # 添加新的评估记录
        today = datetime.now().strftime('%Y-%m-%d')
        new_entry = f"\n## {today} - 评估未通过\n"
        new_entry += f"- **主导风格**: {dominant_style}\n"
        new_entry += f"- **风格契合度**: {result['style_score']}/10\n"
        new_entry += f"- **通用美学**: {result['aesthetic_score']}/10\n"
        new_entry += f"- **连续通过次数归零**: {consecutive_passes} → 0\n"
        new_entry += f"- **评语**: {result['comments']}\n"
        
        changelog_content += new_entry
    
    # 写回 CHANGELOG
    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(changelog_content)

# 保存处理结果
output_file = '/home/ubuntu/art-gallery-curator/processing_actions.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(actions, f, ensure_ascii=False, indent=2)

# 打印统计
print(f"=== 作品处理完成 ===")
print(f"通过并更新: {len(actions['updated_passed'])}")
print(f"未通过并归零: {len(actions['updated_failed'])}")
print(f"需要生成新版本: {len(actions['to_generate'])}")
print(f"晋升到 perfect: {len(actions['to_perfect'])}")
print(f"\n详细信息已保存到: {output_file}")
