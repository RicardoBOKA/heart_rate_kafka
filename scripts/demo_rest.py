#!/usr/bin/env python3
"""
Script de démonstration : Scénario de repos
Simule 30 secondes de données cardiaques au repos.
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from heart_app.sensors import SimulatedHeartSensor
from heart_app.core.engine import HeartSimulationEngine
from heart_app.scenarios import REST_SCENARIO


def main():
    """Exécute la démonstration du scénario de repos."""
    print("=" * 60)
    print("DÉMONSTRATION - SCÉNARIO DE REPOS")
    print("=" * 60)
    print(f"Scénario: {REST_SCENARIO}")
    print(f"Durée: 30 secondes")
    print(f"Fréquence d'échantillonnage: 1 Hz")
    print("=" * 60)
    print()
    
    # Créer le capteur et le moteur
    sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
    engine = HeartSimulationEngine(sensor, sampling_rate=1.0)
    
    # Collecter des statistiques
    bpm_values = []
    rr_values = []
    
    # Streamer les données pendant 30 secondes
    for data in engine.stream(duration=30.0):
        print(data)
        bpm_values.append(data.bpm)
        rr_values.append(data.rr_interval_ms)
    
    # Afficher les statistiques
    print()
    print("=" * 60)
    print("STATISTIQUES")
    print("=" * 60)
    print(f"Nombre d'échantillons: {len(bpm_values)}")
    print(f"BPM moyen: {sum(bpm_values)/len(bpm_values):.1f}")
    print(f"BPM min: {min(bpm_values):.1f}")
    print(f"BPM max: {max(bpm_values):.1f}")
    print(f"RR moyen: {sum(rr_values)/len(rr_values):.0f} ms")
    print("=" * 60)


if __name__ == "__main__":
    main()

