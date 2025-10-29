"""
Tests pour le capteur simulé.
"""

import pytest
import time
from heart_app.sensors import SimulatedHeartSensor
from heart_app.scenarios import REST_SCENARIO, SLEEP_SCENARIO, EXERCISE_SCENARIO


class TestSimulatedHeartSensor:
    """Tests pour SimulatedHeartSensor."""
    
    def test_creation(self):
        """Test de création du capteur."""
        sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
        assert sensor.get_current_scenario() == REST_SCENARIO
    
    def test_read_without_scenario(self):
        """Test que read() échoue sans scénario."""
        sensor = SimulatedHeartSensor()
        with pytest.raises(RuntimeError):
            sensor.read()
    
    def test_read_with_scenario(self):
        """Test de lecture avec un scénario."""
        sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
        data = sensor.read()
        
        assert data is not None
        assert data.bpm > 0
        assert data.rr_interval_ms > 0
        assert data.scenario == "rest"
    
    def test_bpm_in_range(self):
        """Test que le BPM reste dans des plages réalistes."""
        sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
        
        for _ in range(10):
            data = sensor.read()
            # Plage physiologique large mais réaliste
            assert 30 < data.bpm < 220
    
    def test_rr_interval_consistency(self):
        """Test que RR est cohérent avec BPM."""
        sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
        data = sensor.read()
        
        # RR devrait être approximativement 60000 / BPM
        expected_rr = 60000.0 / data.bpm
        # Tolérance large pour la variabilité
        assert abs(data.rr_interval_ms - expected_rr) < 500
    
    def test_scenario_change(self):
        """Test du changement de scénario."""
        sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
        sensor.set_scenario(EXERCISE_SCENARIO)
        assert sensor.get_current_scenario() == EXERCISE_SCENARIO
    
    def test_progressive_transition(self):
        """Test que la transition entre scénarios est progressive."""
        sensor = SimulatedHeartSensor(
            initial_scenario=REST_SCENARIO,
            max_bpm_change_per_second=5.0
        )
        
        # Lire une valeur initiale
        initial_data = sensor.read()
        initial_bpm = sensor.get_current_bpm()
        
        # Changer vers effort
        sensor.set_scenario(EXERCISE_SCENARIO)
        
        # Lire immédiatement après
        time.sleep(0.1)
        new_data = sensor.read()
        
        # Le BPM ne devrait pas avoir sauté directement à la cible
        bpm_diff = abs(new_data.bpm - initial_bpm)
        assert bpm_diff < 20.0  # Pas de saut brutal
    
    def test_reset(self):
        """Test de la réinitialisation."""
        sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
        sensor.read()
        sensor.reset()
        
        # Après reset, le capteur devrait être à l'état initial
        data = sensor.read()
        assert data.timestamp < 1.0  # Proche de 0
    
    def test_metadata_present(self):
        """Test que les métadonnées sont présentes."""
        sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
        data = sensor.read()
        
        assert data.metadata is not None
        assert "is_simulated" in data.metadata
        assert data.metadata["is_simulated"] is True
    
    def test_multiple_reads(self):
        """Test de lectures multiples."""
        sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
        
        readings = []
        for _ in range(5):
            data = sensor.read()
            readings.append(data)
            time.sleep(0.1)
        
        # Vérifier que les timestamps augmentent
        for i in range(len(readings) - 1):
            assert readings[i + 1].timestamp > readings[i].timestamp
    
    def test_different_scenarios_produce_different_ranges(self):
        """Test que différents scénarios produisent des plages différentes."""
        # Repos
        sensor_rest = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
        rest_readings = [sensor_rest.read().bpm for _ in range(20)]
        avg_rest = sum(rest_readings) / len(rest_readings)
        
        # Effort
        sensor_exercise = SimulatedHeartSensor(initial_scenario=EXERCISE_SCENARIO)
        exercise_readings = [sensor_exercise.read().bpm for _ in range(20)]
        avg_exercise = sum(exercise_readings) / len(exercise_readings)
        
        # L'effort devrait avoir un BPM moyen plus élevé
        assert avg_exercise > avg_rest + 20

