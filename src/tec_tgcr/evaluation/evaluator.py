"""
Evaluator for Resonance Arcana metrics.

Runs evaluations on agent interactions, calculates R, and assesses coherence.
"""

from typing import List, Dict, Any
from .metrics import ResonanceScore, CoherenceMetrics
import logging

logger = logging.getLogger(__name__)


class Evaluator:
    """
    Evaluates agent interactions for resonance and coherence.
    """

    def __init__(self):
        self.sessions: List[Dict[str, Any]] = []

    def add_session_data(self, session: Dict[str, Any]):
        """
        Add session data for evaluation.
        """
        self.sessions.append(session)

    def calculate_resonance(self, session_data: Dict[str, Any]) -> ResonanceScore:
        """
        Calculate resonance score for a session.
        """
        # Placeholder calculations based on session data
        phi = session_data.get("integrated_info", 1.0)
        phi_t = session_data.get("temporal_patterns", 0.8)
        psi_r = session_data.get("resonance_strength", 0.9)

        return ResonanceScore(phi=phi, phi_temporal=phi_t, psi_resonance=psi_r)

    def evaluate_coherence(self, session_data: Dict[str, Any]) -> CoherenceMetrics:
        """
        Evaluate coherence metrics.
        """
        cadence = session_data.get("communication_consistency", 0.7)
        attention = session_data.get("user_focus", 0.8)
        risk = session_data.get("load_stress", 0.2)

        return CoherenceMetrics(
            structural_cadence=cadence,
            temporal_attention=attention,
            fragmentation_risk=risk
        )

    def run_evaluation(self) -> Dict[str, Any]:
        """
        Run full evaluation on all sessions.
        """
        results = []
        for session in self.sessions:
            r_score = self.calculate_resonance(session)
            coherence = self.evaluate_coherence(session)
            results.append({
                "session_id": session.get("id"),
                "resonance_score": r_score.calculate_r(),
                "is_coherent": r_score.is_coherent(),
                "coherence_assessment": coherence.assess_fragmentation()
            })

        # Aggregate
        avg_r = np.mean([r["resonance_score"] for r in results]) if results else 0
        coherent_sessions = sum(1 for r in results if r["is_coherent"])

        return {
            "individual_results": results,
            "aggregate": {
                "average_resonance": avg_r,
                "coherent_sessions": coherent_sessions,
                "total_sessions": len(results)
            }
        }