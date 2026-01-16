import os
import json

in_progress_dir = "/home/ubuntu/art-gallery-curator/gallery/in-progress"
folders = sorted([f for f in os.listdir(in_progress_dir) if os.path.isdir(os.path.join(in_progress_dir, f)) and f != ".gitkeep"])

# 已处理的作品
processed = ["abstract-expressionism-emotional-tempest"]

remaining = [f for f in folders if f not in processed]

print(json.dumps(remaining, indent=2))
print(f"\n总计剩余: {len(remaining)} 个作品")
