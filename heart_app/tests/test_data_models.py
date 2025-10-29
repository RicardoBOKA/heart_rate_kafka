"""
Tests pour les modèles de données.
"""

import pytest
from heart_app.core.data_models import HeartData, ScenarioConfig


class TestHeartData:
    """Tests pour la classe HeartData."""
    
    def test_creation(self):
        """Test de création d'un HeartData."""
        data = HeartData(
            timestamp=1.0,
            bpm=60.0,
            rr_interval_ms=1000.0,
            scenario="rest"
        )
        assert data.timestamp == 1.0
        assert data.bpm == 60.0
        assert data.rr_interval_ms == 1000.0
        assert data.scenario == "rest"
    
    def test_to_dict(self):
        """Test de conversion en dictionnaire."""
        data = HeartData(
            timestamp=1.0,
            bpm=60.0,
            rr_interval_ms=1000.0,
            scenario="rest"
        )
        d = data.to_dict()
        assert isinstance(d, dict)
        assert d["bpm"] == 60.0
        assert d["scenario"] == "rest"
    
    def test_str_representation(self):
        """Test de la représentation string."""
        data = HeartData(
            timestamp=1.0,
            bpm=65.5,
            rr_interval_ms=950.0,
            scenario="rest"
        )
        s = str(data)
        assert "rest" in s
        assert "65.5" in s
        assert "950" in s


class TestScenarioConfig:
    """Tests pour la classe ScenarioConfig."""
    
    def test_creation_valid(self):
        """Test de création d'un ScenarioConfig valide."""
        config = ScenarioConfig(
            name="test",
            target_bpm=60.0,
            bpm_variance=5.0,
            target_rr_ms=1000.0,
            rr_variance=100.0
        )
        assert config.name == "test"
        assert config.target_bpm == 60.0
    
    def test_validation_negative_bpm(self):
        """Test que les BPM négatifs sont rejetés."""
        with pytest.raises(ValueError):
            ScenarioConfig(
                name="invalid",
                target_bpm=-10.0,
                bpm_variance=5.0,
                target_rr_ms=1000.0,
                rr_variance=100.0
            )
    
    def test_validation_negative_variance(self):
        """Test que les variances négatives sont rejetées."""
        with pytest.raises(ValueError):
            ScenarioConfig(
                name="invalid",
                target_bpm=60.0,
                bpm_variance=-5.0,
                target_rr_ms=1000.0,
                rr_variance=100.0
            )
    
    def test_str_representation(self):
        """Test de la représentation string."""
        config = ScenarioConfig(
            name="test",
            target_bpm=60.0,
            bpm_variance=5.0,
            target_rr_ms=1000.0,
            rr_variance=100.0
        )
        s = str(config)
        assert "test" in s
        assert "60" in s

