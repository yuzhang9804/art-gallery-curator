import json
from pathlib import Path

# Load artwork list
with open("/home/ubuntu/art-gallery-curator/artworks_to_evaluate.json", "r") as f:
    data = json.load(f)

artworks = data["artworks"]

# Evaluation results
results = []

for artwork_name in artworks:
    artwork_dir = Path(f"/home/ubuntu/art-gallery-curator/gallery/in-progress/{artwork_name}")
    changelog_path = artwork_dir / "CHANGELOG.md"
    
    # Read current consecutive passes from CHANGELOG
    consecutive_passes = 0
    if changelog_path.exists():
        with open(changelog_path, "r") as f:
            content = f.read()
            # Try to find consecutive passes count
            if "连续通过次数" in content:
                # Extract the last occurrence
                lines = content.split("\n")
                for line in reversed(lines):
                    if "连续通过次数" in line and "/" in line:
                        try:
                            parts = line.split(":")[-1].strip()
                            if "/" in parts:
                                consecutive_passes = int(parts.split("/")[0].strip())
                                break
                        except:
                            pass
    
    results.append({
        "name": artwork_name,
        "current_consecutive_passes": consecutive_passes
    })

# Save results
with open("/home/ubuntu/art-gallery-curator/current_status.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Processed {len(results)} artworks")
print(f"\nArtworks with consecutive passes > 0:")
for r in results:
    if r["current_consecutive_passes"] > 0:
        print(f"  - {r['name']}: {r['current_consecutive_passes']}/10")
