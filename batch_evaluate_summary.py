#!/usr/bin/env python3
"""
Quick batch evaluation summary for remaining artworks
Focus on identifying which artworks are most likely to pass Vorticism criteria
"""

import json
from pathlib import Path

# Artworks already evaluated in detail
EVALUATED = [
    "2026-01-17-brutalist-architecture-concrete-structure-with",
    "2026-01-17-purism-futuristic-nostalgia",
    "2026-01-17-rayonism-light-rays",
    "2026-01-19-vorticism-industrial-vortex"
]

# Load complete artwork list
with open("/home/ubuntu/art-gallery-curator/all_artworks_complete.json") as f:
    data = json.load(f)

remaining = [art for art in data["artworks"] if art["name"] not in EVALUATED]

print(f"Remaining artworks to evaluate: {len(remaining)}\n")

# Categorize by likely Vorticism alignment based on style names
high_potential = []
medium_potential = []
low_potential = []

for art in remaining:
    name = art["name"].lower()
    
    # High potential: mechanical, industrial, angular styles
    if any(keyword in name for keyword in ["futurism", "constructivism", "bauhaus", "suprematism", 
                                            "elementarism", "kinetic", "cyberpunk", "steampunk",
                                            "algorithmic", "digital", "neo-geo"]):
        high_potential.append(art)
    
    # Low potential: organic, decorative, atmospheric styles
    elif any(keyword in name for keyword in ["art-nouveau", "rococo", "byzantine", "ukiyo-e",
                                               "fauvism", "tonalism", "impressionism", "pointillism",
                                               "ethereal", "garden", "enchanted", "twilight"]):
        low_potential.append(art)
    
    # Medium: everything else
    else:
        medium_potential.append(art)

print("=== HIGH POTENTIAL FOR VORTICISM ALIGNMENT ===")
for art in high_potential:
    print(f"  - {art['name']}")

print(f"\n=== MEDIUM POTENTIAL ({len(medium_potential)}) ===")
for art in medium_potential[:10]:
    print(f"  - {art['name']}")
if len(medium_potential) > 10:
    print(f"  ... and {len(medium_potential) - 10} more")

print(f"\n=== LOW POTENTIAL ({len(low_potential)}) ===")
for art in low_potential[:10]:
    print(f"  - {art['name']}")
if len(low_potential) > 10:
    print(f"  ... and {len(low_potential) - 10} more")

# Save categorization
output = {
    "evaluated_count": len(EVALUATED),
    "remaining_count": len(remaining),
    "high_potential": [art["name"] for art in high_potential],
    "medium_potential": [art["name"] for art in medium_potential],
    "low_potential": [art["name"] for art in low_potential]
}

with open("/home/ubuntu/art-gallery-curator/evaluation_categorization.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\n✓ Categorization saved to evaluation_categorization.json")
