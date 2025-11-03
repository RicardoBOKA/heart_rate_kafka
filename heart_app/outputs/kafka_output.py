"""
Implémentation Kafka pour l'envoi de données cardiaques.

Ce module fournit KafkaOutput, une classe qui implémente IOutput
pour envoyer des données vers un topic Kafka.
"""

import json
import logging
import os
from typing import Optional

from kafka import KafkaProducer
from kafka.errors import KafkaError

from .base_output import IOutput


# Configuration du logger
logger = logging.getLogger(__name__)


class KafkaOutput(IOutput):
    """
    Envoie des données cardiaques vers un topic Kafka.
    
    Cette classe implémente IOutput pour permettre l'envoi de données
    vers Kafka de manière simple et robuste. Elle gère automatiquement
    la sérialisation JSON et la gestion des erreurs.
    
    Exemple d'utilisation:
        >>> with KafkaOutput() as output:
        ...     output.send(heart_data)
    
    Variables d'environnement:
        KAFKA_BOOTSTRAP_SERVERS: Adresse du broker Kafka (défaut: localhost:9092)
    """
    
    def __init__(
        self,
        topic: str = "fake-heart-data-test",
        bootstrap_servers: Optional[str] = None
    ):
        """
        Initialise le producer Kafka.
        
        Args:
            topic: Nom du topic Kafka où envoyer les données
            bootstrap_servers: Adresse du broker Kafka (si None, lit depuis env)
        """
        self.topic = topic
        
        # Lire la configuration depuis les variables d'environnement
        if bootstrap_servers is None:
            bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        
        self.bootstrap_servers = bootstrap_servers
        self.message_count = 0
        
        # Configuration du producer Kafka
        producer_config = {
            'bootstrap_servers': bootstrap_servers,
            'value_serializer': lambda v: json.dumps(v).encode('utf-8'),
            'acks': 'all',  # Garantit que tous les replicas ont reçu le message
            'retries': 3,   # Nombre de tentatives en cas d'échec
            'max_in_flight_requests_per_connection': 1,  # Garantit l'ordre des messages
        }
        
        try:
            self.producer = KafkaProducer(**producer_config)
            logger.info(
                f"Kafka producer initialisé - Broker: {bootstrap_servers}, Topic: {topic}"
            )
        except KafkaError as e:
            logger.error(f"Erreur lors de l'initialisation du producer Kafka: {e}")
            raise
    
    def send(self, data) -> bool:
        """
        Envoie une mesure cardiaque vers Kafka.
        
        Extrait uniquement les champs essentiels (timestamp, bpm, rr_interval_ms)
        pour simuler des données réelles de capteur, sans métadonnées de scénario.
        
        Args:
            data: Objet HeartData contenant les mesures cardiaques
            
        Returns:
            bool: True si l'envoi a réussi, False sinon
        """
        try:
            # Format minimaliste : seulement les données brutes du capteur
            message = {
                'timestamp': data.timestamp,
                'bpm': data.bpm,
                'rr_interval_ms': data.rr_interval_ms
            }
            
            # Envoi synchrone pour garantir la livraison
            future = self.producer.send(self.topic, value=message)
            record_metadata = future.get(timeout=10)
            
            self.message_count += 1
            
            logger.debug(
                f"Message envoyé - Topic: {record_metadata.topic}, "
                f"Partition: {record_metadata.partition}, "
                f"Offset: {record_metadata.offset}"
            )
            
            return True
            
        except KafkaError as e:
            logger.error(f"Erreur lors de l'envoi à Kafka: {e}")
            return False
        except Exception as e:
            logger.error(f"Erreur inattendue lors de l'envoi: {e}")
            return False
    
    def close(self) -> None:
        """
        Ferme proprement le producer Kafka.
        
        S'assure que tous les messages en attente sont envoyés avant
        de fermer la connexion.
        """
        if hasattr(self, 'producer'):
            logger.info(
                f"Fermeture du producer Kafka - {self.message_count} messages envoyés"
            )
            try:
                # Flush avec timeout pour éviter de bloquer indéfiniment
                # Envoie tous les messages en attente (timeout: 5 secondes)
                self.producer.flush(timeout=5.0)
            except Exception as e:
                logger.warning(f"Erreur lors du flush (messages peuvent être en attente): {e}")
            
            try:
                self.producer.close(timeout=2.0)
            except Exception as e:
                logger.warning(f"Erreur lors de la fermeture: {e}")
            
            logger.info("Producer Kafka fermé avec succès")
    
    def get_message_count(self) -> int:
        """
        Retourne le nombre de messages envoyés avec succès.
        
        Returns:
            int: Nombre de messages envoyés
        """
        return self.message_count

