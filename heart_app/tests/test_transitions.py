"""
Tests pour les fonctions de transition.
"""

import pytest
from heart_app.utils.transitions import (
    interpolate,
    smooth_transition,
    calculate_transition_progress,
    ease_in_out
)


class TestInterpolate:
    """Tests pour la fonction interpolate."""
    
    def test_interpolate_zero(self):
        """Test interpolation à 0 (valeur actuelle)."""
        result = interpolate(10.0, 20.0, 0.0)
        assert result == 10.0
    
    def test_interpolate_one(self):
        """Test interpolation à 1 (valeur cible)."""
        result = interpolate(10.0, 20.0, 1.0)
        assert result == 20.0
    
    def test_interpolate_half(self):
        """Test interpolation à 0.5 (milieu)."""
        result = interpolate(10.0, 20.0, 0.5)
        assert result == 15.0
    
    def test_interpolate_clipping(self):
        """Test que alpha est clippé entre 0 et 1."""
        result1 = interpolate(10.0, 20.0, -0.5)
        result2 = interpolate(10.0, 20.0, 1.5)
        assert result1 == 10.0
        assert result2 == 20.0


class TestSmoothTransition:
    """Tests pour la fonction smooth_transition."""
    
    def test_transition_upward(self):
        """Test transition vers le haut."""
        result = smooth_transition(60.0, 120.0, 5.0)
        assert result == 65.0  # 60 + 5
    
    def test_transition_downward(self):
        """Test transition vers le bas."""
        result = smooth_transition(120.0, 60.0, 5.0)
        assert result == 115.0  # 120 - 5
    
    def test_transition_small_difference(self):
        """Test que les petites différences atteignent directement la cible."""
        result = smooth_transition(60.0, 62.0, 5.0)
        assert result == 62.0
    
    def test_transition_exact_target(self):
        """Test quand déjà à la cible."""
        result = smooth_transition(60.0, 60.0, 5.0)
        assert result == 60.0
    
    def test_transition_respects_max_change(self):
        """Test que le changement max est respecté."""
        result = smooth_transition(50.0, 100.0, 10.0)
        assert result <= 60.0
        assert result >= 50.0


class TestCalculateTransitionProgress:
    """Tests pour calculate_transition_progress."""
    
    def test_progress_start(self):
        """Test au début de la transition."""
        progress = calculate_transition_progress(0.0, 10.0)
        assert progress == 0.0
    
    def test_progress_middle(self):
        """Test au milieu de la transition."""
        progress = calculate_transition_progress(5.0, 10.0)
        assert progress == 0.5
    
    def test_progress_end(self):
        """Test à la fin de la transition."""
        progress = calculate_transition_progress(10.0, 10.0)
        assert progress == 1.0
    
    def test_progress_over(self):
        """Test après la fin (clipping)."""
        progress = calculate_transition_progress(15.0, 10.0)
        assert progress == 1.0
    
    def test_progress_zero_duration(self):
        """Test avec durée nulle."""
        progress = calculate_transition_progress(5.0, 0.0)
        assert progress == 1.0


class TestEaseInOut:
    """Tests pour la fonction ease_in_out."""
    
    def test_ease_boundaries(self):
        """Test aux bornes 0 et 1."""
        assert ease_in_out(0.0) == 0.0
        assert ease_in_out(1.0) == 1.0
    
    def test_ease_middle(self):
        """Test au milieu (devrait être 0.5)."""
        result = ease_in_out(0.5)
        assert abs(result - 0.5) < 0.01
    
    def test_ease_clipping(self):
        """Test le clipping hors limites."""
        assert ease_in_out(-0.5) == 0.0
        assert ease_in_out(1.5) == 1.0
    
    def test_ease_monotonic(self):
        """Test que la fonction est croissante."""
        values = [ease_in_out(t) for t in [0.0, 0.25, 0.5, 0.75, 1.0]]
        for i in range(len(values) - 1):
            assert values[i] <= values[i + 1]

