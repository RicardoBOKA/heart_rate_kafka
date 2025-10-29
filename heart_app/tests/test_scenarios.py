"""
Tests pour les scénarios cardiaques.
"""

import pytest
from heart_app.scenarios import REST_SCENARIO, SLEEP_SCENARIO, EXERCISE_SCENARIO
from heart_app.scenarios.cardiac_scenarios import create_custom_exercise


class TestPredefinedScenarios:
    """Tests pour les scénarios pré-configurés."""
    
    def test_rest_scenario(self):
        """Test du scénario de repos."""
        assert REST_SCENARIO.name == "rest"
        assert 55 <= REST_SCENARIO.target_bpm <= 70
        assert REST_SCENARIO.target_bpm == 60.0
    
    def test_sleep_scenario(self):
        """Test du scénario de sommeil."""
        assert SLEEP_SCENARIO.name == "sleep"
        assert 45 <= SLEEP_SCENARIO.target_bpm <= 60
        assert SLEEP_SCENARIO.target_bpm == 52.0
    
    def test_exercise_scenario(self):
        """Test du scénario d'effort."""
        assert EXERCISE_SCENARIO.name == "exercise"
        assert 90 <= EXERCISE_SCENARIO.target_bpm <= 150
        assert EXERCISE_SCENARIO.target_bpm == 120.0
    
    def test_scenario_rr_intervals(self):
        """Test que les intervalles RR sont cohérents avec les BPM."""
        # RR devrait être plus long pour repos que pour effort
        assert REST_SCENARIO.target_rr_ms > EXERCISE_SCENARIO.target_rr_ms
        assert SLEEP_SCENARIO.target_rr_ms > REST_SCENARIO.target_rr_ms


class TestCustomExercise:
    """Tests pour la création de scénarios d'effort personnalisés."""
    
    def test_create_custom_exercise(self):
        """Test de création d'un effort personnalisé."""
        custom = create_custom_exercise(140.0)
        assert custom.target_bpm == 140.0
        assert "exercise" in custom.name
    
    def test_custom_exercise_rr_calculation(self):
        """Test que le RR est calculé correctement."""
        custom = create_custom_exercise(120.0)
        expected_rr = 60000.0 / 120.0  # 500 ms
        assert abs(custom.target_rr_ms - expected_rr) < 1.0
    
    def test_custom_exercise_different_intensities(self):
        """Test plusieurs intensités d'effort."""
        low = create_custom_exercise(100.0)
        high = create_custom_exercise(160.0)
        
        assert low.target_bpm < high.target_bpm
        assert low.target_rr_ms > high.target_rr_ms

