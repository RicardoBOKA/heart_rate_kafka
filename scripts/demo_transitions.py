#!/usr/bin/env python3
"""
Script de démonstration : Transitions entre différents scénarios
Montre le passage progressif entre repos, sommeil et effort.
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from heart_app.sensors import SimulatedHeartSensor
from heart_app.core.engine import HeartSimulationEngine
from heart_app.scenarios import REST_SCENARIO, SLEEP_SCENARIO, EXERCISE_SCENARIO


def print_phase_header(phase_name: str, scenario):
    """Affiche l'en-tête d'une phase."""
    print(f"\n{'='*60}")
    print(f"PHASE: {phase_name}")
    print(f"Scénario: {scenario.name.upper()} (cible: {scenario.target_bpm} BPM)")
    print("="*60)


def main():
    """Exécute la démonstration de transitions multiples."""
    print("=" * 60)
    print("DÉMONSTRATION - TRANSITIONS ENTRE SCÉNARIOS")
    print("=" * 60)
    print("Cette démo montre les transitions progressives entre:")
    print("  Repos → Sommeil → Repos → Effort → Repos")
    print("\nDurée de chaque phase: 15 secondes")
    print("Notez comment le BPM change progressivement, pas instantanément.")
    print("=" * 60)
    
    # Créer le capteur et le moteur
    sensor = SimulatedHeartSensor(
        initial_scenario=REST_SCENARIO,
        max_bpm_change_per_second=4.0  # Transition douce
    )
    engine = HeartSimulationEngine(sensor, sampling_rate=1.0)
    
    # Définir la séquence de scénarios
    scenarios = [
        ("Repos initial", REST_SCENARIO, 15.0),
        ("Endormissement", SLEEP_SCENARIO, 15.0),
        ("Réveil", REST_SCENARIO, 15.0),
        ("Début d'activité", EXERCISE_SCENARIO, 15.0),
        ("Retour au calme", REST_SCENARIO, 15.0),
    ]
    
    all_data = []
    
    # Exécuter chaque phase
    for phase_name, scenario, duration in scenarios:
        print_phase_header(phase_name, scenario)
        engine.change_scenario(scenario)
        
        phase_data = []
        for data in engine.stream(duration=duration):
            print(data)
            phase_data.append(data)
            all_data.append(data)
        
        # Résumé de la phase
        bpm_values = [d.bpm for d in phase_data]
        print(f"\nRésumé phase: BPM {min(bpm_values):.1f} - {max(bpm_values):.1f} "
              f"(moyenne: {sum(bpm_values)/len(bpm_values):.1f})")
    
    # Statistiques globales
    print("\n" + "=" * 60)
    print("STATISTIQUES GLOBALES")
    print("=" * 60)
    print(f"Nombre total d'échantillons: {len(all_data)}")
    
    bpm_all = [d.bpm for d in all_data]
    print(f"BPM global: min={min(bpm_all):.1f}, max={max(bpm_all):.1f}, "
          f"moyenne={sum(bpm_all)/len(bpm_all):.1f}")
    
    # Analyser les transitions
    print("\nObservations sur les transitions:")
    print("- Le BPM change progressivement, pas instantanément")
    print("- La variabilité RR change selon le scénario")
    print("- Les transitions respectent les limites physiologiques")
    print("=" * 60)


if __name__ == "__main__":
    main()

