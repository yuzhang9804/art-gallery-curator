import os
import glob

in_progress_dir = "/home/ubuntu/art-gallery-curator/gallery/in-progress"
folders = [f for f in os.listdir(in_progress_dir) if os.path.isdir(os.path.join(in_progress_dir, f))]

# 已处理的文件夹
processed = ["art-deco-metropolitan-elegance", "art-nouveau-floral-reverie", "bauhaus-geometric-harmony"]

for folder in folders:
    if folder in processed:
        continue
    
    changelog_path = os.path.join(in_progress_dir, folder, "CHANGELOG.md")
    
    if os.path.exists(changelog_path):
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新版本号
        content = content.replace("- **当前版本**: v1", "- **当前版本**: v2")
        
        # 在迁移记录前添加新评估记录
        new_entry = """### 2026-01-16 - v2 生成（German Expressionism 融合）
- **主导风格**: German Expressionism
- **Standard A (风格契合度)**: 6.5/10
- **Standard B (通用美学)**: 8/10
- **说明**: 基于 v1-original.png 融合 German Expressionism 元素。增加了表现主义特征：扭曲的形态、焦虑的情绪表达、戏剧性光影、深紫和血红色调。但原风格与表现主义在美学理念上存在冲突，融合效果有限。
- **连续通过次数**: 0

"""
        content = content.replace("### 2026-01-16 - 迁移记录", new_entry + "### 2026-01-16 - 迁移记录")
        
        with open(changelog_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated: {folder}")

print("Batch update completed!")
