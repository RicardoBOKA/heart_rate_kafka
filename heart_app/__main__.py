#!/usr/bin/env python3
"""
Point d'entrée principal pour l'application de simulation cardiaque.
Permet d'exécuter via: python -m heart_app
"""

import sys
import argparse
from heart_app.sensors import SimulatedHeartSensor
from heart_app.core.engine import HeartSimulationEngine
from heart_app.scenarios import REST_SCENARIO, SLEEP_SCENARIO, EXERCISE_SCENARIO
from heart_app.scenarios.cardiac_scenarios import create_custom_exercise


def parse_arguments():
    """Parse les arguments de ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Moteur de simulation cardiaque",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m heart_app --scenario rest --duration 30
  python -m heart_app --scenario exercise --intensity 140 --duration 60
  python -m heart_app --scenario sleep --rate 2.0
        """
    )
    
    parser.add_argument(
        "--scenario",
        choices=["rest", "sleep", "exercise"],
        default="rest",
        help="Scénario à simuler (défaut: rest)"
    )
    
    parser.add_argument(
        "--duration",
        type=float,
        default=30.0,
        help="Durée de la simulation en secondes (défaut: 30)"
    )
    
    parser.add_argument(
        "--rate",
        type=float,
        default=1.0,
        help="Fréquence d'échantillonnage en Hz (défaut: 1.0)"
    )
    
    parser.add_argument(
        "--intensity",
        type=float,
        default=None,
        help="BPM cible pour l'effort (défaut: 120, uniquement pour --scenario exercise)"
    )
    
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Mode silencieux, affiche seulement les statistiques finales"
    )
    
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Affiche les statistiques détaillées à la fin"
    )
    
    return parser.parse_args()


def select_scenario(scenario_name: str, intensity: float = None):
    """Sélectionne le scénario approprié."""
    if scenario_name == "rest":
        return REST_SCENARIO
    elif scenario_name == "sleep":
        return SLEEP_SCENARIO
    elif scenario_name == "exercise":
        if intensity is not None:
            return create_custom_exercise(intensity)
        return EXERCISE_SCENARIO
    else:
        raise ValueError(f"Scénario inconnu: {scenario_name}")


def calculate_statistics(data_list):
    """Calcule les statistiques sur les données collectées."""
    if not data_list:
        return {}
    
    bpm_values = [d.bpm for d in data_list]
    rr_values = [d.rr_interval_ms for d in data_list]
    
    # Calcul de l'écart-type pour RR (variabilité)
    rr_mean = sum(rr_values) / len(rr_values)
    rr_variance = sum((x - rr_mean) ** 2 for x in rr_values) / len(rr_values)
    rr_std = rr_variance ** 0.5
    
    return {
        "count": len(data_list),
        "bpm_mean": sum(bpm_values) / len(bpm_values),
        "bpm_min": min(bpm_values),
        "bpm_max": max(bpm_values),
        "rr_mean": rr_mean,
        "rr_std": rr_std,
        "duration": data_list[-1].timestamp - data_list[0].timestamp
    }


def print_statistics(stats, scenario):
    """Affiche les statistiques formatées."""
    print("\n" + "=" * 60)
    print("STATISTIQUES DE LA SIMULATION")
    print("=" * 60)
    print(f"Scénario: {scenario.name}")
    print(f"Échantillons collectés: {stats['count']}")
    print(f"Durée effective: {stats['duration']:.2f} secondes")
    print()
    print("BPM (Battements par minute):")
    print(f"  Moyenne: {stats['bpm_mean']:.1f} BPM")
    print(f"  Minimum: {stats['bpm_min']:.1f} BPM")
    print(f"  Maximum: {stats['bpm_max']:.1f} BPM")
    print(f"  Cible: {scenario.target_bpm:.1f} ±{scenario.bpm_variance:.1f} BPM")
    print()
    print("Intervalles RR (HRV):")
    print(f"  Moyenne: {stats['rr_mean']:.0f} ms")
    print(f"  Écart-type: {stats['rr_std']:.0f} ms")
    print(f"  Cible: {scenario.target_rr_ms:.0f} ±{scenario.rr_variance:.0f} ms")
    print("=" * 60)


def main():
    """Fonction principale."""
    args = parse_arguments()
    
    # Sélectionner le scénario
    try:
        scenario = select_scenario(args.scenario, args.intensity)
    except ValueError as e:
        print(f"Erreur: {e}", file=sys.stderr)
        return 1
    
    # Afficher l'en-tête
    if not args.quiet:
        print("=" * 60)
        print("MOTEUR DE SIMULATION CARDIAQUE")
        print("=" * 60)
        print(f"Scénario: {scenario}")
        print(f"Durée: {args.duration} secondes")
        print(f"Fréquence: {args.rate} Hz")
        print("=" * 60)
        print()
    
    # Créer le capteur et le moteur
    sensor = SimulatedHeartSensor(initial_scenario=scenario)
    engine = HeartSimulationEngine(sensor, sampling_rate=args.rate)
    
    # Collecter les données
    data_collected = []
    
    try:
        for data in engine.stream(duration=args.duration):
            if not args.quiet:
                print(data)
            data_collected.append(data)
    except KeyboardInterrupt:
        print("\n\nInterruption par l'utilisateur (Ctrl+C)")
    
    # Afficher les statistiques si demandé ou en mode quiet
    if args.stats or args.quiet:
        if data_collected:
            stats = calculate_statistics(data_collected)
            print_statistics(stats, scenario)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

