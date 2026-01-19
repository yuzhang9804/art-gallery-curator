#!/usr/bin/env python3
"""
Batch evaluation script for Magic Realism style assessment
2026-01-19
"""

import os
import json
from pathlib import Path

# Today's dominant style
DOMINANT_STYLE = "Magic Realism"
EVALUATION_DATE = "2026-01-19"

# Works to evaluate (excluding the first two already processed)
IN_PROGRESS_DIR = Path("/home/ubuntu/art-gallery-curator/gallery/in-progress")

# Get all work directories
all_works = sorted([d for d in IN_PROGRESS_DIR.iterdir() if d.is_dir()])

# Already processed
processed = [
    "2026-01-19-magic-realism-librarian-of-forgotten-dreams",
    "2026-01-17-brutalist-architecture-concrete-structure-with"
]

# Remaining works to process
remaining_works = [w for w in all_works if w.name not in processed]

print(f"Total works in progress: {len(all_works)}")
print(f"Already processed: {len(processed)}")
print(f"Remaining to evaluate: {len(remaining_works)}")
print("\nRemaining works:")
for i, work in enumerate(remaining_works, 1):
    print(f"{i}. {work.name}")

# Create evaluation summary structure
evaluation_summary = {
    "date": EVALUATION_DATE,
    "dominant_style": DOMINANT_STYLE,
    "total_works": len(all_works),
    "processed": len(processed),
    "remaining": len(remaining_works),
    "works": []
}

# For each remaining work, we need to:
# 1. Check if CHANGELOG.md exists
# 2. Read last consecutive pass count
# 3. Evaluate against Magic Realism
# 4. Update CHANGELOG.md
# 5. If fail: generate new version
# 6. If pass and count=10: move to perfect/

for work_dir in remaining_works:
    work_info = {
        "name": work_dir.name,
        "changelog_exists": (work_dir / "CHANGELOG.md").exists(),
        "has_v1_original": (work_dir / "v1-original.png").exists()
    }
    
    # Read CHANGELOG to get current consecutive count
    changelog_path = work_dir / "CHANGELOG.md"
    if changelog_path.exists():
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Try to find last consecutive count
            if "连续通过次数" in content:
                # Extract last occurrence
                lines = content.split('\n')
                for line in reversed(lines):
                    if "连续通过次数" in line or "Consecutive Pass Count" in line:
                        work_info["last_line"] = line
                        break
    
    evaluation_summary["works"].append(work_info)

# Save summary
summary_path = Path("/home/ubuntu/art-gallery-curator/evaluation_summary_2026-01-19.json")
with open(summary_path, 'w', encoding='utf-8') as f:
    json.dump(evaluation_summary, f, indent=2, ensure_ascii=False)

print(f"\nSummary saved to: {summary_path}")
