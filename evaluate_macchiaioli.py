#!/usr/bin/env python3
"""
Systematic evaluation of all artworks against Macchiaioli style
"""

import os
import json
from pathlib import Path

# Today's dominant style
DOMINANT_STYLE = "Macchiaioli"

# All artworks in in-progress
artworks = [
    "2026-01-17-brutalist-architecture-concrete-structure-with",
    "2026-01-17-purism-futuristic-nostalgia",
    "2026-01-17-rayonism-light-rays",
    "abstract-expressionism-emotional-tempest",
    "algorithmic-art-fractal-consciousness",
    "art-deco-metropolitan-elegance",
    "art-nouveau-floral-reverie",
    "bauhaus-geometric-harmony",
    "byzantine-sacred-mosaic",
    "constructivism-revolutionary-architecture",
    "cyberpunk-neon-rain",
    "digital-art-quantum-garden",
    "elementarism-dynamic-diagonals",
    "fauvism-wild-garden-at-twilight",
    "futurism-velocity-symphony",
    "german-expressionism-urban-anxiety",
    "jugendstil-enchanted-forest",
    "kinetic-art-mechanical-symphony",
    "kinetic-art-perpetual-motion",
    "kinetic-art-temporal-cascade",
    "land-art-spiral-desert",
    "macchiaioli-tuscan-afternoon",
    "neo-geo-industrial-meditation",
    "outsider-art-inner-cosmos",
    "pointillism-sunday-by-the-river",
    "pop-art-consumer-paradise",
    "rococo-garden-of-enchantment",
    "secessionist-eternal-embrace",
    "situationist-international-urban-drift",
    "songlines-of-the-eternal-dreaming",
    "steampunk-clockwork-observatory",
    "suprematism-cosmic-architecture",
    "suprematism-cosmic-ascension",
    "surrealism-dreamscape-labyrinth",
    "tenebrism-candlelit-contemplation",
    "ukiyo-e-wave-of-dreams",
    "urban-anxiety-neo-expressionism",
    "vaporwave-digital-nostalgia"
]

print(f"Total artworks to evaluate: {len(artworks)}")
print(f"Dominant style: {DOMINANT_STYLE}")
print("\nArtworks list:")
for i, artwork in enumerate(artworks, 1):
    print(f"{i}. {artwork}")
