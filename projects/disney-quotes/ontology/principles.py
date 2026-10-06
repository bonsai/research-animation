"""Disney's 12 Principles of Animation — cross-reference to ontology concepts.

Mapping each principle to the ontology concept candidates in the corpus.
These are hypotheses to be validated, not claims that Disney used this vocabulary.
"""

PRINCIPLES = [
    ("SQUEEZE & STRETCH", "squash_and_stretch",
     "物体の柔軟性と動きの生命力を表現。形状を非幾何学的に変形させる。"),
    ("ANTICIPATION", "anticipation",
     "動きの前に予備動作を入れ、視聴者に結果を予測させる。"),
    ("STAGING", "staging",
     "観客の注目を明確な目的へ誘導する構成。"),
    ("STRAIGHT AHEAD & POSE TO POSE", "straight_ahead_pose_to_pose",
     "連続的な描画か、ポーズ間の规划か。生成順序の設計方針。"),
    ("FOLLOW THROUGH & OVERLAPPING ACTION", "follow_through",
     "主要動作後の惯性動作。生成結果の微調整・自然化。"),
    ("SLOW IN & SLOW OUT", "slow_in_out",
     "動きの出始めと終わりを滑らかにする。"),
    ("ARC", "arc",
     "自然な動きは弧を描く。生成軌道の設計。"),
    ("SECONDARY ACTION", "secondary_action",
     "主動作を補完する追加動作。生成結果の装飾・文脈付与。"),
    ("TIMING", "timing",
     "動作の速度と間。生成の制御パラメータ。"),
    ("EXAGGERATION", "exaggeration",
     "現実を超えて意図を明確に。生成強度のスケーリング。"),
    ("Solid Drawing", "solid_drawing",
     "立体感・重量感・バランス。生成物の造形評価。"),
    ("APPEAL", "appeal",
     "観客を惹きつける魅力。キャラクター・生成物の吸引力。"),
]

# concept mapping hypotheses
PRINCIPLE_MAPPINGS = {
    "squash_and_stretch": ["TRANSFORMATION", "POSSIBILITY"],
    "anticipation": ["EXPLORATION", "SEARCH"],
    "staging": ["PERCEPTION", "STORY"],
    "straight_ahead_pose_to_pose": ["SYSTEM", "COORDINATION"],
    "follow_through": ["REFINEMENT", "ITERATION"],
    "slow_in_out": ["TRANSFORMATION"],
    "arc": ["CONTINUITY", "MATERIALIZATION"],
    "secondary_action": ["COLLABORATION", "EMOTION"],
    "timing": ["ITERATION"],
    "exaggeration": ["OPEN_POSSIBILITY", "ENTERTAINMENT"],
    "solid_drawing": ["ENTITY", "CHARACTER"],
    "appeal": ["AUDIENCE", "EVALUATION", "IDENTITY"],
}
