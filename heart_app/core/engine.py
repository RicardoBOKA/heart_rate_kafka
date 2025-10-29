"""
Moteur principal de simulation cardiaque.
"""

import time
from typing import Generator, Optional

from .sensor import ISensor
from .data_models import HeartData, ScenarioConfig


class HeartSimulationEngine:
    """
    Moteur orchestrant la simulation cardiaque.
    
    Gère :
    - Le capteur actif (simulé ou réel)
    - Les changements de scénarios avec transitions
    - L'échantillonnage et le streaming de données
    """
    
    def __init__(
        self,
        sensor: ISensor,
        sampling_rate: float = 1.0
    ):
        """
        Initialise le moteur de simulation.
        
        Args:
            sensor: Capteur cardiaque à utiliser (ISensor)
            sampling_rate: Fréquence d'échantillonnage en Hz (lectures/seconde)
        """
        self._sensor = sensor
        self._sampling_rate = sampling_rate
        self._sampling_interval = 1.0 / sampling_rate
        
    def get_sample(self) -> HeartData:
        """
        Obtient une seule mesure cardiaque.
        
        Returns:
            HeartData: Une mesure cardiaque unique
        """
        return self._sensor.read()
    
    def stream(
        self,
        duration: Optional[float] = None,
        callback: Optional[callable] = None
    ) -> Generator[HeartData, None, None]:
        """
        Génère un flux continu de mesures cardiaques.
        
        Args:
            duration: Durée du streaming en secondes (None = infini)
            callback: Fonction optionnelle appelée pour chaque mesure
            
        Yields:
            HeartData: Mesures cardiaques successives
            
        Examples:
            >>> for data in engine.stream(duration=10.0):
            ...     print(data)
        """
        start_time = time.time()
        
        while True:
            # Vérifier si la durée est dépassée
            if duration is not None:
                elapsed = time.time() - start_time
                if elapsed >= duration:
                    break
            
            # Lire une mesure
            data = self._sensor.read()
            
            # Appeler le callback si fourni
            if callback is not None:
                callback(data)
            
            # Yield la donnée
            yield data
            
            # Attendre le prochain échantillon
            time.sleep(self._sampling_interval)
    
    def change_scenario(self, scenario: ScenarioConfig) -> None:
        """
        Change le scénario actif du capteur.
        
        La transition sera progressive grâce aux mécanismes internes du capteur.
        
        Args:
            scenario: Nouveau scénario à appliquer
        """
        self._sensor.set_scenario(scenario)
    
    def reset(self) -> None:
        """
        Réinitialise l'état du moteur et du capteur.
        """
        self._sensor.reset()
    
    def get_current_scenario(self) -> Optional[ScenarioConfig]:
        """
        Retourne le scénario actuellement actif.
        
        Returns:
            ScenarioConfig ou None
        """
        return self._sensor.get_current_scenario()
    
    def set_sampling_rate(self, rate: float) -> None:
        """
        Modifie la fréquence d'échantillonnage.
        
        Args:
            rate: Nouvelle fréquence en Hz
        """
        if rate <= 0:
            raise ValueError("Le taux d'échantillonnage doit être positif")
        self._sampling_rate = rate
        self._sampling_interval = 1.0 / rate
    
    def get_sampling_rate(self) -> float:
        """
        Retourne la fréquence d'échantillonnage actuelle.
        
        Returns:
            Fréquence en Hz
        """
        return self._sampling_rate

