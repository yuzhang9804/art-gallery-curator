import os
import json

# 列出所有 in-progress 作品文件夹
in_progress_dir = "/home/ubuntu/art-gallery-curator/gallery/in-progress"
folders = [f for f in os.listdir(in_progress_dir) if os.path.isdir(os.path.join(in_progress_dir, f)) and not f.startswith('.')]

# 排除已处理的作品
processed = ["abstract-expressionism-emotional-tempest"]
remaining = [f for f in folders if f not in processed]

print(json.dumps(remaining, indent=2))
print(f"\nTotal remaining: {len(remaining)}")
