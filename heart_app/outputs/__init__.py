"""
Module outputs - Destinations de sortie pour les données cardiaques.

Ce module fournit une architecture extensible pour envoyer les données
vers différentes destinations (Kafka, fichiers, bases de données, APIs, etc.).

Toutes les destinations implémentent l'interface IOutput, garantissant
une interface uniforme et une extensibilité maximale.

Usage:
    from heart_app.outputs import KafkaOutput
    
    with KafkaOutput() as output:
        output.send(heart_data)
"""

from .base_output import IOutput
from .kafka_output import KafkaOutput

__all__ = [
    'IOutput',
    'KafkaOutput',
]

__version__ = '1.0.0'

