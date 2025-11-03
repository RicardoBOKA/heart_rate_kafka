#!/usr/bin/env python3
"""
Script de production de données cardiaques simulées vers Kafka.

Ce script génère en continu des données cardiaques simulées (scénario REST)
et les envoie vers Kafka via KafkaOutput. Il tourne indéfiniment jusqu'à
interruption manuelle (Ctrl+C).

Variables d'environnement requises:
    KAFKA_BOOTSTRAP_SERVERS: Adresse du broker Kafka (défaut: localhost:9092)
                            Exemples:
                            - localhost:9092
                            - kafka1:29092
                            - 192.168.1.100:9092

Usage:
    # Avec configuration par défaut (localhost:9092)
    python scripts/producers/producer_fake_data.py
    
    # Avec serveur Kafka custom
    export KAFKA_BOOTSTRAP_SERVERS="kafka1:29092"
    python scripts/producers/producer_fake_data.py
    
    # Arrêter le script: Ctrl+C
"""

import sys
import os
import logging
import time

# Ajouter le répertoire racine au path pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from heart_app.sensors import SimulatedHeartSensor
from heart_app.core.engine import HeartSimulationEngine
from heart_app.scenarios import REST_SCENARIO
from heart_app.outputs import KafkaOutput


# ============================================================================
# CONFIGURATION DU SCRIPT (paramètres en dur pour simplicité)
# ============================================================================

SCENARIO = REST_SCENARIO       # Scénario de repos (BPM ~70)
SAMPLING_RATE = 1.0            # 1 Hz = 1 mesure par seconde
TOPIC = "fake-heart-data-test" # Topic Kafka cible

# ============================================================================
# CONFIGURATION DU LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


def main():
    """
    Fonction principale du producer.
    
    Initialise le capteur simulé, le moteur de simulation et le output Kafka,
    puis streame les données en continu jusqu'à interruption manuelle.
    """
    
    # Affichage de l'en-tête
    print("=" * 70)
    print("🫀 PRODUCER KAFKA - DONNÉES CARDIAQUES SIMULÉES")
    print("=" * 70)
    print(f"Scénario      : {SCENARIO.name} (BPM cible: {SCENARIO.target_bpm})")
    print(f"Fréquence     : {SAMPLING_RATE} Hz")
    print(f"Topic Kafka   : {TOPIC}")
    print(f"Durée         : Infinie (Ctrl+C pour arrêter)")
    
    # Afficher la configuration Kafka depuis les variables d'environnement
    kafka_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    print(f"Kafka Broker  : {kafka_servers}")
    print("=" * 70)
    print()
    
    # Initialisation du capteur et du moteur
    logger.info("Initialisation du capteur simulé...")
    sensor = SimulatedHeartSensor(initial_scenario=SCENARIO)
    engine = HeartSimulationEngine(sensor, sampling_rate=SAMPLING_RATE)
    logger.info("Capteur simulé initialisé avec succès")
    
    # Variables pour les statistiques
    start_time = time.time()
    messages_sent = 0
    
    try:
        # Utiliser le context manager pour garantir la fermeture propre
        with KafkaOutput(topic=TOPIC) as kafka_output:
            logger.info("Producer Kafka prêt - Début du streaming...")
            print("✅ Streaming démarré - Appuyez sur Ctrl+C pour arrêter\n")
            
            # Boucle infinie de production de données
            for data in engine.stream(duration=None):  # duration=None = infini
                # Envoyer vers Kafka
                success = kafka_output.send(data)
                
                if success:
                    messages_sent += 1
                    # Affichage compact toutes les 10 secondes
                    if messages_sent % 10 == 0:
                        elapsed = time.time() - start_time
                        rate = messages_sent / elapsed if elapsed > 0 else 0
                        print(
                            f"📊 Messages envoyés: {messages_sent} | "
                            f"Temps écoulé: {elapsed:.0f}s | "
                            f"Taux: {rate:.2f} msg/s | "
                            f"BPM actuel: {data.bpm:.1f}"
                        )
                else:
                    logger.warning("Échec de l'envoi d'un message à Kafka")
    
    except KeyboardInterrupt:
        # Interruption manuelle par l'utilisateur (Ctrl+C)
        print("\n")
        print("=" * 70)
        print("⚠️  INTERRUPTION MANUELLE (Ctrl+C)")
        print("=" * 70)
    
    except Exception as e:
        # Erreur inattendue
        logger.error(f"Erreur fatale: {e}", exc_info=True)
        print("\n")
        print("=" * 70)
        print("❌ ERREUR FATALE")
        print("=" * 70)
        print(f"Erreur: {e}")
        print("Consultez les logs pour plus de détails.")
        print("=" * 70)
        return 1
    
    finally:
        # Affichage des statistiques finales
        elapsed = time.time() - start_time
        print()
        print("=" * 70)
        print("📊 STATISTIQUES FINALES")
        print("=" * 70)
        print(f"Messages envoyés  : {messages_sent}")
        print(f"Durée totale      : {elapsed:.2f} secondes")
        
        if elapsed > 0:
            avg_rate = messages_sent / elapsed
            print(f"Taux moyen        : {avg_rate:.2f} messages/seconde")
        
        print("=" * 70)
        logger.info("Producer arrêté proprement")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

