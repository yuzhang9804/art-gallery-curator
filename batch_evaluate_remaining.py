#!/usr/bin/env python3.11
import os
import json

# 已评估的作品
evaluated = [
    "abstract-expressionism-emotional-tempest",
    "art-deco-metropolitan-elegance",
    "suprematism-cosmic-architecture",
    "suprematism-cosmic-ascension"
]

# 获取所有in-progress作品
in_progress_dir = "gallery/in-progress"
all_artworks = [d for d in os.listdir(in_progress_dir) 
                if os.path.isdir(os.path.join(in_progress_dir, d)) and d not in [".gitkeep", ""]]

# 过滤出未评估的作品
remaining = [a for a in all_artworks if a not in evaluated]

print(f"总作品数: {len(all_artworks)}")
print(f"已评估: {len(evaluated)}")
print(f"待评估: {len(remaining)}")
print("\n待评估作品列表:")
for i, artwork in enumerate(remaining, 1):
    artwork_path = os.path.join(in_progress_dir, artwork)
    
    # 获取最新版本
    png_files = [f for f in os.listdir(artwork_path) if f.endswith('.png')]
    if png_files:
        png_files.sort(key=lambda x: os.path.getmtime(os.path.join(artwork_path, x)), reverse=True)
        latest = png_files[0]
        
        # 读取连续通过次数
        changelog_path = os.path.join(artwork_path, "CHANGELOG.md")
        consecutive = 0
        if os.path.exists(changelog_path):
            with open(changelog_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if '连续通过次数' in line and ':' in line:
                        try:
                            consecutive = int(line.split(':')[1].strip().split()[0])
                            break
                        except:
                            pass
        
        print(f"{i}. {artwork}")
        print(f"   最新版本: {latest}")
        print(f"   连续通过次数: {consecutive}")
