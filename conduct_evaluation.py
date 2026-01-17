#!/usr/bin/env python3.11
"""
Strict Art Evaluation System
Evaluates artworks with extremely high standards
"""

import json
import os
from pathlib import Path

# Load evaluation list
with open('/home/ubuntu/art-gallery-curator/evaluation_list.json', 'r') as f:
    data = json.load(f)

DOMINANT_STYLE = data['dominant_style']
DOMINANT_STYLE_DESC = data['dominant_style_desc']
artworks = data['artworks']

print(f"=== STRICT ART EVALUATION ===")
print(f"Dominant Style: {DOMINANT_STYLE}")
print(f"Description: {DOMINANT_STYLE_DESC}")
print(f"Total Artworks: {len(artworks)}")
print(f"\nEvaluation Criteria:")
print(f"  - Criterion A (Style Alignment): How well does this artwork embody {DOMINANT_STYLE}?")
print(f"  - Criterion B (Universal Aesthetics): Composition, color, creativity, emotional expression")
print(f"  - Pass Threshold: Either A or B >= 9.5/10.0")
print(f"  - Perfect Status: 10 consecutive passes")
print(f"\n{'='*80}\n")

# Prepare evaluation results
results = []

for idx, artwork in enumerate(artworks, 1):
    print(f"[{idx}/{len(artworks)}] Evaluating: {artwork['name']}")
    print(f"  Style: {artwork['style']}")
    print(f"  Image: {artwork['image']}")
    print(f"  Consecutive Passes: {artwork['consecutive_passes']}")
    
    # Store for batch evaluation
    results.append({
        'artwork': artwork,
        'index': idx
    })

# Save results for manual evaluation
output_file = '/home/ubuntu/art-gallery-curator/evaluation_results.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({
        'dominant_style': DOMINANT_STYLE,
        'dominant_style_desc': DOMINANT_STYLE_DESC,
        'results': results
    }, f, indent=2, ensure_ascii=False)

print(f"\nEvaluation data prepared: {output_file}")
print(f"Ready for visual assessment of {len(results)} artworks")
