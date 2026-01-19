#!/usr/bin/env python3.11
"""
Update CHANGELOG.md files for all artworks based on evaluation results
"""

import json
from pathlib import Path
from datetime import datetime

# Paths
GALLERY_ROOT = Path("/home/ubuntu/art-gallery-curator/gallery")
IN_PROGRESS = GALLERY_ROOT / "in-progress"
EVALUATION_RESULTS = GALLERY_ROOT / "evaluation_results.json"

# Today's evaluation info
TODAY_DATE = "2026-01-19"
DOMINANT_STYLE = "Tachisme"

def update_changelog(artwork_folder, result):
    """Update or create CHANGELOG.md for an artwork"""
    
    changelog_path = artwork_folder / "CHANGELOG.md"
    
    # Read existing CHANGELOG if it exists
    if changelog_path.exists():
        existing_content = changelog_path.read_text(encoding='utf-8')
    else:
        existing_content = ""
    
    # Determine if this is a new CHANGELOG
    is_new = not changelog_path.exists() or len(existing_content.strip()) < 50
    
    # Extract artwork title from GALLERY.md if available
    gallery_md = artwork_folder / "GALLERY.md"
    title = result['title']
    style = result['style']
    
    if gallery_md.exists():
        gallery_content = gallery_md.read_text(encoding='utf-8')
        lines = gallery_content.split('\n')
        if lines:
            title = lines[0].replace('#', '').strip()
    
    # Build new evaluation entry
    status_symbol = "✓ PASS" if result['passed'] else "✗ FAIL"
    
    new_entry = f"""
### {TODAY_DATE} - Evaluation ({DOMINANT_STYLE})
- **Dominant Style**: {DOMINANT_STYLE}
- **Style Alignment**: {result['style_alignment']:.1f}/10.0
- **Universal Aesthetics**: {result['universal_aesthetics']:.1f}/10.0
- **Result**: {status_symbol}
- **Consecutive Passes**: {result['current_consecutive']} → {result['new_consecutive']}

**Evaluation Notes:**
"""
    
    if result['passed']:
        new_entry += f"本次评估通过。作品在风格契合度或通用美学方面达到了9.5分以上的高标准。连续通过次数增加至{result['new_consecutive']}次。"
    else:
        new_entry += f"本次评估未通过。在以{DOMINANT_STYLE}为主导风格的评判标准下,作品未能在任一维度达到9.5分的通过标准。连续通过次数归零。"
    
    new_entry += "\n\n---\n"
    
    # Create or update CHANGELOG
    if is_new:
        # Create new CHANGELOG
        changelog_content = f"""# CHANGELOG - {title}

## Artwork Information
- **Title**: {title}
- **Style**: {style}
- **Status**: In Progress

## Evaluation History
{new_entry}
## 连续通过次数: {result['new_consecutive']}/10

**完美判定规则**: 只有连续10次风格鉴定都被判定为「通过」的作品,才能进入永久收藏(Perfect Gallery)。
"""
    else:
        # Update existing CHANGELOG
        # Find the position to insert new entry (after "## Evaluation History")
        if "## Evaluation History" in existing_content:
            parts = existing_content.split("## Evaluation History")
            header = parts[0] + "## Evaluation History"
            
            # Find the consecutive passes section
            if "## 连续通过次数:" in existing_content:
                history_and_footer = parts[1].split("## 连续通过次数:")
                history = history_and_footer[0]
                footer_template = "## 连续通过次数:" + history_and_footer[1].split('\n', 1)[1] if len(history_and_footer[1].split('\n', 1)) > 1 else "\n\n**完美判定规则**: 只有连续10次风格鉴定都被判定为「通过」的作品,才能进入永久收藏(Perfect Gallery)。\n"
            else:
                history = parts[1]
                footer_template = "\n\n**完美判定规则**: 只有连续10次风格鉴定都被判定为「通过」的作品,才能进入永久收藏(Perfect Gallery)。\n"
            
            changelog_content = f"""{header}
{new_entry}{history}
## 连续通过次数: {result['new_consecutive']}/10
{footer_template}"""
        else:
            # Fallback: append to end
            changelog_content = existing_content + f"\n\n{new_entry}\n## 连续通过次数: {result['new_consecutive']}/10\n"
    
    # Write updated CHANGELOG
    changelog_path.write_text(changelog_content, encoding='utf-8')
    print(f"Updated: {artwork_folder.name}")

def main():
    """Main update loop"""
    
    # Load evaluation results
    with open(EVALUATION_RESULTS, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    print(f"=== Updating CHANGELOGs for {len(results)} artworks ===\n")
    
    for result in results:
        folder_name = result['folder']
        artwork_folder = IN_PROGRESS / folder_name
        
        if artwork_folder.exists():
            update_changelog(artwork_folder, result)
        else:
            print(f"Warning: Folder not found: {folder_name}")
    
    print(f"\n=== All CHANGELOGs updated ===")

if __name__ == "__main__":
    main()
