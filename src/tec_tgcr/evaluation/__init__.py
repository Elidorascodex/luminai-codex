"""
TEC TGCR Evaluation Framework

Provides metrics and evaluation tools for resonance score (R), coherence, and fragmentation assessment.
Based on Resonance Arcana architecture and Integrated Information Theory (Φ).
"""

from .metrics import ResonanceScore, CoherenceMetrics
from .evaluator import Evaluator

__all__ = ["ResonanceScore", "CoherenceMetrics", "Evaluator"]