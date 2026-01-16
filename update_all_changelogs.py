import os
import json

# 读取评估结果
with open('/home/ubuntu/art-gallery-curator/jugendstil_evaluation.json', 'r', encoding='utf-8') as f:
    evaluations = json.load(f)

base_path = '/home/ubuntu/art-gallery-curator/gallery/in-progress'

for artwork, data in evaluations.items():
    changelog_path = os.path.join(base_path, artwork, 'CHANGELOG.md')
    
    if not os.path.exists(changelog_path):
        print(f"Warning: {changelog_path} not found, skipping...")
        continue
    
    # 读取现有内容
    with open(changelog_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新连续通过次数
    if '## 连续通过次数：' in content:
        content = content.replace(
            f'## 连续通过次数：{content.split("## 连续通过次数：")[1].split()[0]}',
            f'## 连续通过次数：{data["consecutive"]}'
        )
    
    # 追加新评估记录
    new_entry = f'''
## 2026-01-16 - 评估 (主导风格: Jugendstil)

**评分**:
- 标准A (风格契合度): {data["style_score"]}/10.0
- 标准B (通用美学): {data["aesthetic_score"]}/10.0
- **本次通过**: {'✅ 是' if data["passed"] else '❌ 否'}

**评估意见**:

{data["comment"]}

**连续通过次数**: {data["consecutive"]}/10

'''
    
    if not data["passed"]:
        # 获取下一个版本号
        version_num = len([line for line in content.split('\n') if 'v' in line and '-jugendstil-fusion.png' in line or 'v' in line and 'fusion.png' in line]) + 1
        new_entry += f'''---

## 版本历史更新
- v{version_num}-jugendstil-fusion.png: 融合 Jugendstil 风格 (2026-01-16)
'''
    
    # 写回文件
    with open(changelog_path, 'a', encoding='utf-8') as f:
        f.write(new_entry)
    
    print(f"Updated: {artwork} - Pass: {data['passed']}, Consecutive: {data['consecutive']}")

print("\nAll CHANGELOGs updated!")
