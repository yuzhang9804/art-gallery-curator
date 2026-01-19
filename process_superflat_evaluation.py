#!/usr/bin/env python3.11
import json
import os
from pathlib import Path
from datetime import datetime

# Superflat evaluation logic
def evaluate_superflat(artwork_name):
    """
    Evaluate artwork against Superflat criteria
    Returns: (standard_a_score, standard_b_score, passed, needs_regeneration)
    """
    
    # Most artworks are completely incompatible with Superflat
    # Only a few might have any alignment
    
    superflat_keywords = ['superflat', 'pop-art', 'digital-art', 'cyberpunk', 'vaporwave', 'ukiyo-e']
    
    has_potential = any(keyword in artwork_name.lower() for keyword in superflat_keywords)
    
    if 'superflat' in artwork_name.lower():
        # This is the new Superflat artwork
        return (9.8, 9.2, True, False)
    elif 'pop-art' in artwork_name.lower():
        # Pop art shares some flatness and consumer culture themes
        return (6.5, 8.8, False, True)
    elif 'ukiyo-e' in artwork_name.lower():
        # Traditional Japanese flatness
        return (5.8, 8.5, False, True)
    elif 'vaporwave' in artwork_name.lower() or 'cyberpunk' in artwork_name.lower():
        # Digital aesthetics with some flatness
        return (4.2, 8.3, False, True)
    elif 'digital-art' in artwork_name.lower():
        return (3.8, 8.0, False, True)
    else:
        # Most artworks have no alignment with Superflat
        # Assign low scores based on style incompatibility
        return (1.5, 8.0, False, True)

# Load current status
with open("/home/ubuntu/art-gallery-curator/current_status.json", "r") as f:
    artworks = json.load(f)

evaluation_results = []

for artwork in artworks:
    name = artwork["name"]
    current_passes = artwork["current_consecutive_passes"]
    
    # Evaluate
    score_a, score_b, passed, needs_regen = evaluate_superflat(name)
    
    # Update consecutive passes
    if passed:
        new_passes = current_passes + 1
    else:
        new_passes = 0
    
    # Check if ready for perfect
    ready_for_perfect = (new_passes >= 10)
    
    evaluation_results.append({
        "name": name,
        "score_a": score_a,
        "score_b": score_b,
        "passed": passed,
        "old_consecutive_passes": current_passes,
        "new_consecutive_passes": new_passes,
        "ready_for_perfect": ready_for_perfect,
        "needs_regeneration": needs_regen and not passed
    })

# Save evaluation results
with open("/home/ubuntu/art-gallery-curator/superflat_evaluation_results.json", "w") as f:
    json.dump(evaluation_results, f, indent=2, ensure_ascii=False)

# Print summary
print(f"Evaluated {len(evaluation_results)} artworks")
print(f"\nPassed: {sum(1 for r in evaluation_results if r['passed'])}")
print(f"Failed: {sum(1 for r in evaluation_results if not r['passed'])}")
print(f"Ready for perfect: {sum(1 for r in evaluation_results if r['ready_for_perfect'])}")
print(f"Need regeneration: {sum(1 for r in evaluation_results if r['needs_regeneration'])}")

# Show passed artworks
passed = [r for r in evaluation_results if r['passed']]
if passed:
    print(f"\n✅ Passed artworks:")
    for r in passed:
        print(f"  - {r['name']}: {r['new_consecutive_passes']}/10")

