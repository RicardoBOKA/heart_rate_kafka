#!/usr/bin/env python3
"""
Script de vérification rapide - Test sans dépendances externes.
Vérifie que les imports et la structure de base fonctionnent.
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def check_imports():
    """Vérifie que tous les imports fonctionnent."""
    print("Vérification des imports...")
    
    try:
        from heart_app.core.data_models import HeartData, ScenarioConfig
        print("  ✓ data_models")
    except Exception as e:
        print(f"  ✗ data_models: {e}")
        return False
    
    try:
        from heart_app.core.sensor import ISensor
        print("  ✓ sensor")
    except Exception as e:
        print(f"  ✗ sensor: {e}")
        return False
    
    try:
        from heart_app.scenarios import REST_SCENARIO, SLEEP_SCENARIO, EXERCISE_SCENARIO
        print("  ✓ scenarios")
    except Exception as e:
        print(f"  ✗ scenarios: {e}")
        return False
    
    try:
        from heart_app.sensors import SimulatedHeartSensor
        print("  ✓ simulated_sensor")
    except Exception as e:
        print(f"  ✗ simulated_sensor: {e}")
        return False
    
    try:
        from heart_app.core.engine import HeartSimulationEngine
        print("  ✓ engine")
    except Exception as e:
        print(f"  ✗ engine: {e}")
        return False
    
    try:
        from heart_app.utils.transitions import smooth_transition, interpolate
        print("  ✓ transitions")
    except Exception as e:
        print(f"  ✗ transitions: {e}")
        return False
    
    return True


def check_basic_functionality():
    """Vérifie que la fonctionnalité de base marche."""
    print("\nVérification de la fonctionnalité de base...")
    
    try:
        from heart_app.sensors import SimulatedHeartSensor
        from heart_app.core.engine import HeartSimulationEngine
        from heart_app.scenarios import REST_SCENARIO
        
        # Créer un capteur et moteur
        sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
        engine = HeartSimulationEngine(sensor, sampling_rate=1.0)
        print("  ✓ Création du capteur et moteur")
        
        # Lire un échantillon
        data = engine.get_sample()
        print(f"  ✓ Lecture d'un échantillon: {data}")
        
        # Vérifier les valeurs
        if data.bpm > 0 and data.rr_interval_ms > 0:
            print("  ✓ Valeurs cohérentes")
        else:
            print("  ✗ Valeurs incorrectes")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ✗ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Fonction principale."""
    print("=" * 60)
    print("VÉRIFICATION RAPIDE DU MOTEUR DE SIMULATION")
    print("=" * 60)
    print()
    
    # Vérifier les imports
    imports_ok = check_imports()
    
    if not imports_ok:
        print("\n❌ Échec de la vérification des imports")
        print("\nAssurez-vous d'avoir installé les dépendances:")
        print("  pip install -r requirements.txt")
        return 1
    
    # Vérifier la fonctionnalité
    functionality_ok = check_basic_functionality()
    
    if not functionality_ok:
        print("\n❌ Échec de la vérification fonctionnelle")
        return 1
    
    print("\n" + "=" * 60)
    print("✅ TOUTES LES VÉRIFICATIONS ONT RÉUSSI!")
    print("=" * 60)
    print("\nVous pouvez maintenant:")
    print("  1. Exécuter les tests: pytest heart_app/tests/ -v")
    print("  2. Essayer les démos: python scripts/demo_rest.py")
    print("  3. Utiliser le CLI: python -m heart_app --help")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

