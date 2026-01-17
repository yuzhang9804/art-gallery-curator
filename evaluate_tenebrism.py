import os
import json

# 评估数据
evaluations = {
    "abstract-expressionism-emotional-tempest": {
        "current_streak": 0,
        "style_score": 0.5,
        "aesthetic_score": 8.2,
        "passed": False,
        "comment": "这是一件纯粹的抽象表现主义作品，与 Tenebrism（明暗对照法）完全无关。缺乏单一光源、极端明暗对比、具象主题等核心特征。通用美学方面，虽有情感爆发力，但缺乏视觉焦点，色彩混乱，构图张力不够精妙，情感表达直白而缺乏层次。",
        "action": "generate_new_version"
    }
}

# 保存评估结果
with open('/home/ubuntu/art-gallery-curator/tenebrism_evaluation.json', 'w', encoding='utf-8') as f:
    json.dump(evaluations, f, ensure_ascii=False, indent=2)

print("评估数据已保存")
