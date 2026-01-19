#!/usr/bin/env python3
"""
Update all CHANGELOG.md files based on Vorticism evaluation results
All artworks failed, so all consecutive passes reset to 0
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Load evaluation results
with open("/home/ubuntu/art-gallery-curator/vorticism_evaluation_complete.json") as f:
    evaluation_data = json.load(f)

GALLERY_DIR = Path("/home/ubuntu/art-gallery-curator/gallery/in-progress")
TODAY = "2026-01-19"
STYLE = "Vorticism"

def update_changelog(artwork_name, evaluation):
    """Update or create CHANGELOG.md for an artwork"""
    artwork_dir = GALLERY_DIR / artwork_name
    changelog_path = artwork_dir / "CHANGELOG.md"
    
    if not artwork_dir.exists():
        print(f"Warning: {artwork_name} directory not found")
        return
    
    # Read existing changelog if it exists
    if changelog_path.exists():
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update consecutive passes to 0 in metadata section
        if "**Consecutive Passes**:" in content:
            # Find and replace the consecutive passes line
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "**Consecutive Passes**:" in line or "Consecutive Passes:" in line:
                    lines[i] = "- **Consecutive Passes**: 0"
                    break
            content = '\n'.join(lines)
        else:
            # Add consecutive passes if not present
            if "## Metadata" in content:
                content = content.replace(
                    "## Metadata",
                    f"## Metadata\n- **Consecutive Passes**: 0"
                )
    else:
        # Create new changelog
        content = f"""# Changelog: {artwork_name}

## Metadata
- **Artwork ID**: {artwork_name}
- **Current Status**: In Progress
- **Consecutive Passes**: 0

---
"""
    
    # Append new evaluation entry
    new_entry = f"""
## {TODAY} - Vorticism Evaluation
- **Evaluation Style**: {STYLE}
- **Style Alignment Score**: {evaluation['style_alignment']}/10.0
- **Universal Aesthetics Score**: {evaluation['universal_aesthetics']}/10.0
- **Result**: FAILED (neither standard ≥ 9.5)
- **Consecutive Passes**: Reset to 0
- **Reason**: {evaluation['reason']}
- **Action Required**: Generate new version fusing with Vorticism style
"""
    
    content += new_entry
    
    # Write updated changelog
    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Updated: {artwork_name}")

def main():
    print(f"Updating CHANGELOG.md for all {len(evaluation_data['evaluations'])} artworks...\n")
    
    for evaluation in evaluation_data['evaluations']:
        artwork_name = evaluation['artwork']
        update_changelog(artwork_name, evaluation)
    
    print(f"\n✓ All changelogs updated successfully!")
    print(f"All consecutive passes reset to 0 (all artworks failed Vorticism evaluation)")

if __name__ == "__main__":
    main()
