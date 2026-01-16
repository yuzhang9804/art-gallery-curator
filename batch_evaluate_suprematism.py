import os
import json

# 主导风格
STYLE = "Suprematism"

# 获取所有in-progress作品
in_progress_dir = "gallery/in-progress"
artworks = [d for d in os.listdir(in_progress_dir) if os.path.isdir(os.path.join(in_progress_dir, d)) and d != "."]

results = []

for artwork in artworks:
    artwork_path = os.path.join(in_progress_dir, artwork)
    
    # 获取最新版本图片
    png_files = [f for f in os.listdir(artwork_path) if f.endswith('.png')]
    if not png_files:
        continue
    
    # 按修改时间排序
    png_files.sort(key=lambda x: os.path.getmtime(os.path.join(artwork_path, x)), reverse=True)
    latest_version = png_files[0]
    
    # 读取CHANGELOG获取当前连续通过次数
    changelog_path = os.path.join(artwork_path, "CHANGELOG.md")
    consecutive_passes = 0
    if os.path.exists(changelog_path):
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 查找连续通过次数
            for line in content.split('\n'):
                if '连续通过次数' in line and ':' in line:
                    try:
                        num_str = line.split(':')[1].strip()
                        consecutive_passes = int(num_str.split()[0])
                        break
                    except:
                        pass
    
    results.append({
        "name": artwork,
        "latest_version": latest_version,
        "path": os.path.join(artwork_path, latest_version),
        "consecutive_passes": consecutive_passes
    })

# 输出结果
print(json.dumps(results, indent=2, ensure_ascii=False))
