"""
Tests pour le moteur de simulation.
"""

import pytest
from heart_app.core.engine import HeartSimulationEngine
from heart_app.sensors import SimulatedHeartSensor
from heart_app.scenarios import REST_SCENARIO, EXERCISE_SCENARIO


class TestHeartSimulationEngine:
    """Tests pour HeartSimulationEngine."""
    
    def test_creation(self):
        """Test de création du moteur."""
        sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
        engine = HeartSimulationEngine(sensor, sampling_rate=1.0)
        assert engine.get_sampling_rate() == 1.0
    
    def test_get_sample(self):
        """Test de lecture d'un échantillon unique."""
        sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
        engine = HeartSimulationEngine(sensor)
        
        data = engine.get_sample()
        assert data is not None
        assert data.bpm > 0
    
    def test_stream_duration(self):
        """Test du streaming avec durée limitée."""
        sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
        engine = HeartSimulationEngine(sensor, sampling_rate=10.0)  # 10 Hz
        
        samples = list(engine.stream(duration=0.5))
        
        # Devrait avoir environ 5 échantillons (0.5s * 10Hz)
        assert 3 <= len(samples) <= 7  # Tolérance pour timing
    
    def test_stream_callback(self):
        """Test du streaming avec callback."""
        sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
        engine = HeartSimulationEngine(sensor, sampling_rate=10.0)
        
        collected = []
        
        def callback(data):
            collected.append(data)
        
        list(engine.stream(duration=0.3, callback=callback))
        
        assert len(collected) > 0
        assert all(d.bpm > 0 for d in collected)
    
    def test_change_scenario(self):
        """Test du changement de scénario via le moteur."""
        sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
        engine = HeartSimulationEngine(sensor)
        
        engine.change_scenario(EXERCISE_SCENARIO)
        assert engine.get_current_scenario() == EXERCISE_SCENARIO
    
    def test_reset(self):
        """Test de la réinitialisation du moteur."""
        sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
        engine = HeartSimulationEngine(sensor)
        
        engine.get_sample()
        engine.reset()
        
        data = engine.get_sample()
        assert data.timestamp < 1.0
    
    def test_set_sampling_rate(self):
        """Test du changement de fréquence d'échantillonnage."""
        sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
        engine = HeartSimulationEngine(sensor, sampling_rate=1.0)
        
        engine.set_sampling_rate(5.0)
        assert engine.get_sampling_rate() == 5.0
    
    def test_invalid_sampling_rate(self):
        """Test que les fréquences invalides sont rejetées."""
        sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
        engine = HeartSimulationEngine(sensor)
        
        with pytest.raises(ValueError):
            engine.set_sampling_rate(-1.0)
        
        with pytest.raises(ValueError):
            engine.set_sampling_rate(0.0)
    
    def test_stream_timestamps_increasing(self):
        """Test que les timestamps augmentent dans le stream."""
        sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
        engine = HeartSimulationEngine(sensor, sampling_rate=10.0)
        
        samples = list(engine.stream(duration=0.3))
        
        for i in range(len(samples) - 1):
            assert samples[i + 1].timestamp > samples[i].timestamp

