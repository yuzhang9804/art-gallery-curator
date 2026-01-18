#!/usr/bin/env python3.11
"""
Art Gallery Curator - Systematic Artwork Evaluation Script
Evaluates all works in in-progress directory against today's dominant style (Op Art)
"""

import os
import re
from pathlib import Path

# Today's dominant style
DOMINANT_STYLE = "Op Art"
EVALUATION_DATE = "2026-01-18"

# Gallery paths
IN_PROGRESS_DIR = Path("/home/ubuntu/art-gallery-curator/gallery/in-progress")
PERFECT_DIR = Path("/home/ubuntu/art-gallery-curator/gallery/perfect")

def read_changelog(work_dir):
    """Read existing CHANGELOG.md to get current streak count"""
    changelog_path = work_dir / "CHANGELOG.md"
    if not changelog_path.exists():
        return 0
    
    content = changelog_path.read_text()
    # Look for the most recent "连续通过次数" line
    matches = re.findall(r'连续通过次数[：:]\s*(\d+)/10', content)
    if matches:
        return int(matches[-1])
    return 0

def get_work_style(work_name):
    """Extract style from work directory name"""
    # Common patterns: date-style-theme or style-theme
    parts = work_name.split('-')
    
    # Skip date parts (YYYY-MM-DD)
    if len(parts) > 0 and parts[0].isdigit() and len(parts[0]) == 4:
        parts = parts[3:]  # Skip YYYY, MM, DD
    
    # Try to identify style from remaining parts
    style_keywords = {
        'op-art': 'Op Art',
        'brutalist': 'Brutalist Architecture',
        'purism': 'Purism',
        'rayonism': 'Rayonism',
        'graffiti': 'Graffiti Art',
        'process-art': 'Process Art',
        'regionalism': 'Regionalism',
        'tonalism': 'Tonalism',
        'abstract-expressionism': 'Abstract Expressionism',
        'algorithmic': 'Algorithmic Art',
        'art-deco': 'Art Deco',
        'art-nouveau': 'Art Nouveau',
        'bauhaus': 'Bauhaus',
        'byzantine': 'Byzantine',
        'constructivism': 'Constructivism',
        'cyberpunk': 'Cyberpunk',
        'digital-art': 'Digital Art',
        'elementarism': 'Elementarism',
        'fauvism': 'Fauvism',
        'futurism': 'Futurism',
        'german-expressionism': 'German Expressionism',
        'jugendstil': 'Jugendstil',
        'kinetic-art': 'Kinetic Art',
        'land-art': 'Land Art',
        'macchiaioli': 'Macchiaioli',
        'metaphysical': 'Metaphysical Art',
        'neo-geo': 'Neo-Geo',
        'outsider-art': 'Outsider Art',
        'pointillism': 'Pointillism',
        'pop-art': 'Pop Art',
        'rococo': 'Rococo',
        'secessionist': 'Secessionist',
        'situationist': 'Situationist International',
        'songlines': 'Indigenous Australian Art',
        'steampunk': 'Steampunk',
        'suprematism': 'Suprematism',
        'surrealism': 'Surrealism',
        'tenebrism': 'Tenebrism',
        'ukiyo-e': 'Ukiyo-e',
        'vaporwave': 'Vaporwave',
    }
    
    work_lower = work_name.lower()
    for keyword, style_name in style_keywords.items():
        if keyword in work_lower:
            return style_name
    
    return "Unknown Style"

def main():
    """Main evaluation workflow"""
    works = sorted([d for d in IN_PROGRESS_DIR.iterdir() if d.is_dir()])
    
    print(f"=== Art Gallery Curator Evaluation ===")
    print(f"Date: {EVALUATION_DATE}")
    print(f"Dominant Style: {DOMINANT_STYLE}")
    print(f"Total works to evaluate: {len(works)}")
    print()
    
    stats = {
        'evaluated': 0,
        'passed': 0,
        'failed': 0,
        'promoted_to_perfect': 0,
        'needs_regeneration': []
    }
    
    for work_dir in works:
        work_name = work_dir.name
        work_style = get_work_style(work_name)
        current_streak = read_changelog(work_dir)
        
        print(f"📁 {work_name}")
        print(f"   Style: {work_style}")
        print(f"   Current streak: {current_streak}/10")
        
        # Store for batch processing
        stats['evaluated'] += 1
        print(f"   ⏳ Queued for evaluation")
        print()
    
    print(f"\n=== Evaluation Queue Summary ===")
    print(f"Total works queued: {stats['evaluated']}")
    print(f"\nAll works have been identified and are ready for detailed evaluation.")

if __name__ == "__main__":
    main()
