"""
Scénarios cardiaques pré-configurés avec valeurs physiologiques réalistes.
"""

from heart_app.core.data_models import ScenarioConfig


# Scénario de repos - Personne éveillée au calme
REST_SCENARIO = ScenarioConfig(
    name="rest",
    target_bpm=60.0,
    bpm_variance=5.0,
    target_rr_ms=1000.0,
    rr_variance=100.0,
    description="État de repos, personne calme et éveillée"
)

# Scénario de sommeil - Personne endormie
SLEEP_SCENARIO = ScenarioConfig(
    name="sleep",
    target_bpm=52.0,
    bpm_variance=4.0,
    target_rr_ms=1150.0,
    rr_variance=150.0,
    description="État de sommeil profond"
)

# Scénario d'effort - Activité physique modérée à intense
EXERCISE_SCENARIO = ScenarioConfig(
    name="exercise",
    target_bpm=120.0,
    bpm_variance=10.0,
    target_rr_ms=500.0,
    rr_variance=50.0,
    description="Effort physique modéré à intense"
)


def create_custom_exercise(intensity_bpm: float) -> ScenarioConfig:
    """
    Crée un scénario d'effort personnalisé avec un BPM cible spécifique.
    
    Args:
        intensity_bpm: Fréquence cardiaque cible pour l'effort
        
    Returns:
        ScenarioConfig configuré pour l'effort demandé
    """
    # Calcul automatique du RR correspondant
    target_rr = 60000.0 / intensity_bpm
    # Variance proportionnelle à l'intensité
    bpm_variance = max(5.0, intensity_bpm * 0.08)
    rr_variance = max(30.0, target_rr * 0.1)
    
    return ScenarioConfig(
        name=f"exercise_{int(intensity_bpm)}",
        target_bpm=intensity_bpm,
        bpm_variance=bpm_variance,
        target_rr_ms=target_rr,
        rr_variance=rr_variance,
        description=f"Effort personnalisé à {intensity_bpm} BPM"
    )

