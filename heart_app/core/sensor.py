"""
Interface abstraite pour les capteurs cardiaques.
"""

from abc import ABC, abstractmethod
from typing import Optional
from .data_models import HeartData, ScenarioConfig


class ISensor(ABC):
    """
    Interface abstraite pour tous les capteurs cardiaques.
    
    Cette interface permet de créer différentes implémentations :
    - Capteurs simulés (pour tests et développement)
    - Capteurs réels (connexion matériel)
    - Capteurs hybrides (mixte simulation + données réelles)
    """
    
    @abstractmethod
    def read(self) -> HeartData:
        """
        Lit une mesure cardiaque du capteur.
        
        Returns:
            HeartData: Données cardiaques mesurées
            
        Raises:
            Exception: Si la lecture échoue
        """
        pass
    
    @abstractmethod
    def set_scenario(self, scenario: ScenarioConfig) -> None:
        """
        Change le scénario actif du capteur.
        
        Args:
            scenario: Nouvelle configuration de scénario
        """
        pass
    
    @abstractmethod
    def reset(self) -> None:
        """
        Réinitialise l'état interne du capteur.
        """
        pass
    
    def get_current_scenario(self) -> Optional[ScenarioConfig]:
        """
        Retourne le scénario actuellement actif.
        
        Returns:
            ScenarioConfig ou None si aucun scénario n'est défini
        """
        return None

