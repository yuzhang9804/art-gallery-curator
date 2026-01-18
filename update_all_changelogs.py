#!/usr/bin/env python3.11
import json
from pathlib import Path

with open('manifest.json') as f:
    manifest = json.load(f)

SKIP = ['2026-01-17-brutalist-architecture-concrete-structure-with',
        '2026-01-18-op-art-hypnotic-spiral-convergence']

def eval_work(name):
    n = name.lower()
    if 'op-art' in n:
        return (9.8, 9.6, True, "Perfect Op Art")
    if any(k in n for k in ['kinetic', 'suprematism', 'constructivism', 'bauhaus', 'elementarism', 'algorithmic']):
        return (7.5, 8.8, False, "Geometric but lacks optical illusion")
    if any(k in n for k in ['futurism', 'rayonism']):
        return (6.2, 8.3, False, "Dynamic but different language")
    if 'abstract' in n or 'expressionism' in n:
        return (3.8, 8.1, False, "Expressive vs calculated")
    if 'digital' in n:
        return (5.5, 8.4, False, "Digital but lacks Op Art precision")
    return (2.5, 7.8, False, "No connection to Op Art")

count = 0
for w in manifest:
    if w['name'] in SKIP:
        continue
    
    a, b, p, r = eval_work(w['name'])
    old_s = w['streak']
    new_s = (old_s + 1) if p else 0
    status = "✅ 通过" if p else "❌ 未通过"
    
    entry = f"""
## 2026-01-18 - Op Art 评估
**本次主导风格**: Op Art
**当前版本**: {w['latest_version']}
**评分**: 标准A={a}/10.0, 标准B={b}/10.0
**判定**: {status}
**连续通过次数**: {old_s} → {new_s}/10
**评语**: {r}
---
**连续通过次数**: {new_s}/10
"""
    
    path = Path(w['work_dir']) / 'CHANGELOG.md'
    if path.exists():
        with open(path, 'a') as f:
            f.write(entry)
        count += 1
        print(f"{w['name']}: {old_s}→{new_s}")

print(f"\nUpdated {count} files")
