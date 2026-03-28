from typing import Dict


def fuse_risk(rule_score: float, model_score: float, coordination_score: float) -> float:
    return min(1.0, 0.2 * rule_score + 0.4 * model_score + 0.4 * coordination_score)


def build_alert(session_id: str, individual_bot_score: float, coordination_score: float, reasons) -> Dict:
    final_risk = fuse_risk(1.0 if reasons else 0.0, individual_bot_score, coordination_score)
    return {
        "session_id": session_id,
        "individual_bot_score": individual_bot_score,
        "coordination_score": coordination_score,
        "final_risk": final_risk,
        "reasons": list(reasons),
    }
