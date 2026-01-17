import os
import json

# Main style for this evaluation session
MAIN_STYLE = "Secessionist Art"
MAIN_STYLE_CN = "维也纳分离派"

# All artworks to evaluate
artworks = [
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
    "futurism-velocity-symphony",
    "german-expressionism-urban-anxiety",
    "jugendstil-enchanted-forest",
    "land-art-spiral-desert",
    "outsider-art-inner-cosmos",
    "pointillism-sunday-by-the-river",
    "pop-art-consumer-paradise",
    "rococo-garden-of-enchantment",
    "secessionist-eternal-embrace",
    "situationist-international-urban-drift",
    "steampunk-clockwork-observatory",
    "suprematism-cosmic-architecture",
    "suprematism-cosmic-ascension",
    "surrealism-dreamscape-labyrinth",
    "tenebrism-candlelit-contemplation",
    "ukiyo-e-wave-of-dreams",
    "vaporwave-digital-nostalgia"
]

base_path = "/home/ubuntu/art-gallery-curator/gallery/in-progress"

# Extract current consecutive passes from CHANGELOG
results = []
for artwork in artworks:
    changelog_path = os.path.join(base_path, artwork, "CHANGELOG.md")
    if os.path.exists(changelog_path):
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Find consecutive passes count
            if "连续通过次数:" in content or "连续通过次数：" in content:
                lines = content.split('\n')
                for line in lines:
                    if "连续通过次数" in line and "/" in line:
                        try:
                            parts = line.split(':')[-1].split('：')[-1].strip()
                            current_passes = int(parts.split('/')[0].strip())
                            results.append({
                                'artwork': artwork,
                                'current_passes': current_passes,
                                'changelog_path': changelog_path
                            })
                            break
                        except:
                            pass

print(json.dumps(results, indent=2, ensure_ascii=False))
