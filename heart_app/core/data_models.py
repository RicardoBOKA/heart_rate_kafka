"""
Modèles de données pour la simulation cardiaque.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class HeartData:
    """
    Représente une mesure cardiaque à un instant donné.
    
    Attributes:
        timestamp: Temps en secondes (epoch ou relatif)
        bpm: Fréquence cardiaque en battements par minute
        rr_interval_ms: Intervalle RR en millisecondes (HRV)
        scenario: Nom du scénario actif (repos, sommeil, effort, etc.)
        metadata: Informations additionnelles optionnelles
    """
    timestamp: float
    bpm: float
    rr_interval_ms: float
    scenario: str
    metadata: Optional[dict] = None
    
    def to_dict(self) -> dict:
        """Convertit les données en dictionnaire."""
        return {
            "timestamp": self.timestamp,
            "bpm": self.bpm,
            "rr_interval_ms": self.rr_interval_ms,
            "scenario": self.scenario,
            "metadata": self.metadata
        }
    
    def __str__(self) -> str:
        """Représentation lisible des données."""
        return (f"[{self.scenario}] "
                f"BPM: {self.bpm:.1f} | "
                f"RR: {self.rr_interval_ms:.0f}ms | "
                f"Time: {self.timestamp:.2f}s")


@dataclass
class ScenarioConfig:
    """
    Configuration d'un scénario cardiaque.
    
    Attributes:
        name: Nom du scénario (repos, sommeil, effort, etc.)
        target_bpm: Fréquence cardiaque cible moyenne
        bpm_variance: Variance acceptable autour du BPM cible
        target_rr_ms: Intervalle RR cible moyen en millisecondes
        rr_variance: Variance acceptable autour du RR cible
        description: Description optionnelle du scénario
    """
    name: str
    target_bpm: float
    bpm_variance: float
    target_rr_ms: float
    rr_variance: float
    description: str = ""
    
    def __post_init__(self):
        """Validation des paramètres."""
        if self.target_bpm <= 0:
            raise ValueError("target_bpm doit être positif")
        if self.bpm_variance < 0:
            raise ValueError("bpm_variance doit être positive ou nulle")
        if self.target_rr_ms <= 0:
            raise ValueError("target_rr_ms doit être positif")
        if self.rr_variance < 0:
            raise ValueError("rr_variance doit être positive ou nulle")
    
    def __str__(self) -> str:
        """Représentation lisible de la configuration."""
        return (f"{self.name}: BPM={self.target_bpm}±{self.bpm_variance}, "
                f"RR={self.target_rr_ms}±{self.rr_variance}ms")

