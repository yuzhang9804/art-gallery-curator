#!/usr/bin/env python3
"""
Update all CHANGELOG.md files with Fauvism evaluation results
"""

import json
from pathlib import Path
from datetime import datetime

def update_changelog(artwork_name, evaluation_data):
    """Update or create CHANGELOG.md for an artwork"""
    artwork_path = Path(f"/home/ubuntu/art-gallery-curator/gallery/in-progress/{artwork_name}")
    changelog_path = artwork_path / "CHANGELOG.md"
    
    if not artwork_path.exists():
        print(f"Warning: {artwork_name} directory not found")
        return
    
    standard_a = evaluation_data["standard_a"]
    standard_b = evaluation_data["standard_b"]
    passed = evaluation_data["passed"]
    consecutive_passes = evaluation_data["consecutive_passes"]
    notes = evaluation_data["notes"]
    
    # Create new entry
    new_entry = f"""
## 2026-01-17 - Fauvism 评估

**标准A (风格契合度 - Fauvism)**: {standard_a}/10.0  
**标准B (通用美学)**: {standard_b}/10.0

**评估说明**: {notes}

**判定**: {'✅ 通过' if passed else '❌ 未通过'}  
**连续通过次数**: {consecutive_passes}/10

---
"""
    
    # Read existing changelog if it exists
    if changelog_path.exists():
        with open(changelog_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        
        # Update consecutive passes count in header
        if "连续通过次数:" in existing_content:
            # Replace the count
            lines = existing_content.split('\n')
            for i, line in enumerate(lines):
                if "连续通过次数:" in line:
                    lines[i] = f"## 连续通过次数: {consecutive_passes}/10"
                    break
            existing_content = '\n'.join(lines)
        
        # Add new entry after the header
        parts = existing_content.split('---', 1)
        if len(parts) > 1:
            new_content = parts[0] + '---' + new_entry + parts[1]
        else:
            new_content = existing_content + '\n' + new_entry
    else:
        # Create new changelog
        new_content = f"""# CHANGELOG

## 连续通过次数: {consecutive_passes}/10

---
{new_entry}
"""
    
    # Write updated changelog
    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ Updated: {artwork_name}")

def main():
    # Load evaluation results
    results_file = "/home/ubuntu/art-gallery-curator/evaluation_results_fauvism.json"
    with open(results_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    evaluations = data["evaluations"]
    
    print(f"Updating {len(evaluations)} CHANGELOG files...\n")
    
    for artwork_name, eval_data in evaluations.items():
        update_changelog(artwork_name, eval_data)
    
    print(f"\n✓ All CHANGELOG files updated successfully")

if __name__ == "__main__":
    main()
