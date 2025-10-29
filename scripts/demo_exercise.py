#!/usr/bin/env python3
"""
Script de démonstration : Scénario d'effort avec montée et récupération
Simule une séquence d'effort physique avec transition progressive.
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from heart_app.sensors import SimulatedHeartSensor
from heart_app.core.engine import HeartSimulationEngine
from heart_app.scenarios import REST_SCENARIO, EXERCISE_SCENARIO


def main():
    """Exécute la démonstration d'un cycle effort/récupération."""
    print("=" * 60)
    print("DÉMONSTRATION - EFFORT AVEC RÉCUPÉRATION")
    print("=" * 60)
    print("Séquence:")
    print("  1. Repos (10 secondes)")
    print("  2. Montée en effort (20 secondes)")
    print("  3. Récupération (20 secondes)")
    print("=" * 60)
    print()
    
    # Créer le capteur et le moteur
    sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
    engine = HeartSimulationEngine(sensor, sampling_rate=1.0)
    
    # Phase 1: Repos (10s)
    print("PHASE 1: REPOS")
    print("-" * 60)
    for data in engine.stream(duration=10.0):
        print(data)
    
    # Phase 2: Effort (20s)
    print("\nPHASE 2: MONTÉE EN EFFORT")
    print("-" * 60)
    engine.change_scenario(EXERCISE_SCENARIO)
    bpm_values_exercise = []
    for data in engine.stream(duration=20.0):
        print(data)
        bpm_values_exercise.append(data.bpm)
    
    # Phase 3: Récupération (20s)
    print("\nPHASE 3: RÉCUPÉRATION")
    print("-" * 60)
    engine.change_scenario(REST_SCENARIO)
    bpm_values_recovery = []
    for data in engine.stream(duration=20.0):
        print(data)
        bpm_values_recovery.append(data.bpm)
    
    # Statistiques
    print()
    print("=" * 60)
    print("STATISTIQUES")
    print("=" * 60)
    print(f"BPM max pendant l'effort: {max(bpm_values_exercise):.1f}")
    print(f"BPM moyen pendant l'effort: {sum(bpm_values_exercise)/len(bpm_values_exercise):.1f}")
    print(f"BPM final après récupération: {bpm_values_recovery[-1]:.1f}")
    print(f"Descente BPM pendant récupération: {bpm_values_recovery[0]:.1f} → {bpm_values_recovery[-1]:.1f}")
    print("=" * 60)


if __name__ == "__main__":
    main()

