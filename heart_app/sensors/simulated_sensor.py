"""
Capteur cardiaque simulé pour tests et développement.
"""

import time
import numpy as np
from typing import Optional

from heart_app.core.sensor import ISensor
from heart_app.core.data_models import HeartData, ScenarioConfig
from heart_app.utils.transitions import smooth_transition


class SimulatedHeartSensor(ISensor):
    """
    Capteur cardiaque simulé avec génération de données réalistes.
    
    Génère des données BPM et HRV (intervalles RR) avec :
    - Oscillations naturelles autour des valeurs cibles
    - Transitions progressives entre scénarios
    - Variabilité réaliste basée sur des distributions normales
    """
    
    def __init__(
        self,
        initial_scenario: Optional[ScenarioConfig] = None,
        max_bpm_change_per_second: float = 4.0,
        sampling_rate: float = 1.0
    ):
        """
        Initialise le capteur simulé.
        
        Args:
            initial_scenario: Scénario de départ (optionnel)
            max_bpm_change_per_second: Vitesse max de changement de BPM (réalisme)
            sampling_rate: Taux d'échantillonnage en Hz (lectures par seconde)
        """
        self._scenario: Optional[ScenarioConfig] = initial_scenario
        self._current_bpm: float = initial_scenario.target_bpm if initial_scenario else 60.0
        self._start_time: float = time.time()
        self._last_read_time: float = self._start_time
        self._max_bpm_change_per_second = max_bpm_change_per_second
        self._sampling_rate = sampling_rate
        
        # Pour ajouter des oscillations lentes et naturelles
        self._oscillation_phase = np.random.uniform(0, 2 * np.pi)
        self._oscillation_frequency = 0.1  # Hz - environ une oscillation tous les 10s
        
    def read(self) -> HeartData:
        """
        Lit une mesure cardiaque simulée.
        
        Returns:
            HeartData avec valeurs générées
            
        Raises:
            RuntimeError: Si aucun scénario n'est défini
        """
        if self._scenario is None:
            raise RuntimeError("Aucun scénario défini. Appelez set_scenario() d'abord.")
        
        current_time = time.time()
        elapsed_since_start = current_time - self._start_time
        time_delta = current_time - self._last_read_time
        self._last_read_time = current_time
        
        # Calcul du BPM avec transition progressive
        target_bpm = self._scenario.target_bpm
        max_change = self._max_bpm_change_per_second * time_delta
        self._current_bpm = smooth_transition(self._current_bpm, target_bpm, max_change)
        
        # Ajout d'oscillations lentes et naturelles
        self._oscillation_phase += 2 * np.pi * self._oscillation_frequency * time_delta
        oscillation = np.sin(self._oscillation_phase) * (self._scenario.bpm_variance * 0.3)
        
        # Ajout de variabilité court-terme (bruit)
        noise = np.random.normal(0, self._scenario.bpm_variance * 0.4)
        
        # BPM final
        bpm = self._current_bpm + oscillation + noise
        bpm = max(30.0, min(220.0, bpm))  # Limites physiologiques
        
        # Calcul du RR basé sur le BPM
        # RR_ms = 60000 / BPM (conversion minute -> millisecondes)
        base_rr = 60000.0 / bpm
        
        # Ajout de variabilité HRV
        rr_noise = np.random.normal(0, self._scenario.rr_variance)
        rr_interval = base_rr + rr_noise
        rr_interval = max(300.0, min(2000.0, rr_interval))  # Limites physiologiques
        
        return HeartData(
            timestamp=elapsed_since_start,
            bpm=bpm,
            rr_interval_ms=rr_interval,
            scenario=self._scenario.name,
            metadata={
                "is_simulated": True,
                "sampling_rate": self._sampling_rate
            }
        )
    
    def set_scenario(self, scenario: ScenarioConfig) -> None:
        """
        Change le scénario actif.
        
        La transition vers le nouveau scénario sera progressive grâce à
        la fonction smooth_transition() utilisée dans read().
        
        Args:
            scenario: Nouveau scénario à appliquer
        """
        self._scenario = scenario
    
    def reset(self) -> None:
        """
        Réinitialise l'état interne du capteur.
        """
        self._start_time = time.time()
        self._last_read_time = self._start_time
        if self._scenario:
            self._current_bpm = self._scenario.target_bpm
        self._oscillation_phase = np.random.uniform(0, 2 * np.pi)
    
    def get_current_scenario(self) -> Optional[ScenarioConfig]:
        """
        Retourne le scénario actuellement actif.
        
        Returns:
            ScenarioConfig actuel ou None
        """
        return self._scenario
    
    def get_current_bpm(self) -> float:
        """
        Retourne le BPM actuel (état interne).
        
        Returns:
            BPM actuel avant ajout de bruit/oscillations
        """
        return self._current_bpm

