"""
Interface abstraite pour les destinations de sortie des données cardiaques.

Ce module définit l'interface IOutput qui doit être implémentée par toutes
les destinations de données (Kafka, fichiers, bases de données, APIs, etc.).
Cette abstraction permet une architecture extensible et découplée.
"""

from abc import ABC, abstractmethod
from typing import Any


class IOutput(ABC):
    """
    Interface pour les destinations de sortie des données cardiaques.
    
    Toute nouvelle destination (Kafka, fichier, DB, API) doit implémenter
    cette interface pour garantir la compatibilité avec le système.
    
    Cette interface suit le même pattern que ISensor, créant une symétrie
    architecturale : ISensor pour les sources, IOutput pour les destinations.
    """
    
    @abstractmethod
    def send(self, data: Any) -> bool:
        """
        Envoie des données vers la destination.
        
        Args:
            data: Données à envoyer (typiquement HeartData)
            
        Returns:
            bool: True si l'envoi a réussi, False sinon
            
        Raises:
            Exception: En cas d'erreur critique empêchant l'envoi
        """
        pass
    
    @abstractmethod
    def close(self) -> None:
        """
        Ferme proprement la connexion/ressource.
        
        Cette méthode doit être appelée pour libérer les ressources,
        fermer les connexions réseau, flusher les buffers, etc.
        """
        pass
    
    def __enter__(self):
        """
        Support du context manager (with statement).
        
        Permet d'utiliser:
            with KafkaOutput() as output:
                output.send(data)
        
        Returns:
            self: L'instance de l'output
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Fermeture automatique avec le context manager.
        
        Garantit que close() est appelé même en cas d'exception.
        """
        self.close()
        return False  # Ne supprime pas les exceptions

