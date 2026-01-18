#!/usr/bin/env python3
"""
Quick evaluation script for all artworks
"""

import json
from pathlib import Path

# Load artworks list
with open('/home/ubuntu/art-gallery-curator/artworks_to_evaluate.json', 'r') as f:
    artworks = json.load(f)

DOMINANT_STYLE = "Tonalism"

# Evaluation results
results = []

for artwork in artworks:
    name = artwork['name']
    image_name = artwork['image_name']
    consecutive_passes = artwork['consecutive_passes']
    
    # Determine if artwork style matches Tonalism
    is_tonalism = 'tonalism' in name.lower()
    
    # Quick evaluation logic
    if is_tonalism:
        # Tonalism artworks have high chance of passing
        result = {
            "name": name,
            "image": image_name,
            "style_match": "High",
            "consecutive_passes_before": consecutive_passes,
            "action": "Detailed evaluation needed"
        }
    else:
        # Non-Tonalism artworks likely won't pass
        result = {
            "name": name,
            "image": image_name,
            "style_match": "Low",
            "consecutive_passes_before": consecutive_passes,
            "action": "Reset to 0, generate fusion version"
        }
    
    results.append(result)

# Count statistics
tonalism_count = sum(1 for r in results if r['style_match'] == 'High')
non_tonalism_count = sum(1 for r in results if r['style_match'] == 'Low')

print(f"Total artworks: {len(results)}")
print(f"Tonalism artworks: {tonalism_count}")
print(f"Non-Tonalism artworks: {non_tonalism_count}")

# Save results
output_path = Path("/home/ubuntu/art-gallery-curator/quick_eval_results.json")
with open(output_path, 'w') as f:
    json.dump({
        "dominant_style": DOMINANT_STYLE,
        "statistics": {
            "total": len(results),
            "tonalism": tonalism_count,
            "non_tonalism": non_tonalism_count
        },
        "results": results
    }, f, indent=2, ensure_ascii=False)

print(f"\nResults saved to: {output_path}")
