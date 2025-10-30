#!/usr/bin/env python3
"""
Script de démonstration : Flux continu avec scénarios aléatoires
Génère un flux infini de données cardiaques avec des transitions aléatoires
entre différents scénarios, tout en restant principalement en mode repos.
"""

import sys
import os
import random
import signal
import time
from typing import List, Tuple

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from heart_app.sensors import SimulatedHeartSensor
from heart_app.core.engine import HeartSimulationEngine
from heart_app.scenarios import REST_SCENARIO, SLEEP_SCENARIO, EXERCISE_SCENARIO
from heart_app.core.data_models import ScenarioConfig


class RandomScenarioStream:
    """Gestionnaire de flux continu avec scénarios aléatoires."""
    
    def __init__(self, sampling_rate: float = 1.0):
        """
        Initialise le gestionnaire de flux.
        
        Args:
            sampling_rate: Fréquence d'échantillonnage en Hz
        """
        self.sampling_rate = sampling_rate
        self.sensor = SimulatedHeartSensor(
            initial_scenario=REST_SCENARIO,
            max_bpm_change_per_second=4.0
        )
        self.engine = HeartSimulationEngine(self.sensor, sampling_rate=sampling_rate)
        
        # Scénarios alternatifs (non-REST)
        self.alternative_scenarios = [
            (SLEEP_SCENARIO, "SOMMEIL", 20.0, 40.0),  # (scénario, nom, durée_min, durée_max)
            (EXERCISE_SCENARIO, "EFFORT", 15.0, 30.0),
        ]
        
        # Configuration du scénario par défaut
        self.default_scenario = REST_SCENARIO
        self.current_scenario_name = "REPOS"
        
        # Statistiques
        self.total_samples = 0
        self.bpm_values: List[float] = []
        self.rr_values: List[float] = []
        self.scenario_switches = 0
        self.start_time = None
        
        # Flag d'arrêt
        self.should_stop = False
        
    def _schedule_next_scenario_switch(self) -> Tuple[ScenarioConfig, str, float]:
        """
        Planifie le prochain changement de scénario.
        
        Returns:
            Tuple (scénario, nom, durée en secondes)
        """
        # Décider si on passe à un scénario alternatif ou si on reste en repos
        # Probabilité: 70% repos prolongé, 30% scénario alternatif
        if random.random() < 0.7:
            # Rester en repos pour une durée aléatoire (60-180 secondes)
            duration = random.uniform(3.0, 5.0)
            return self.default_scenario, "REPOS", duration
        else:
            # Choisir un scénario alternatif
            scenario, name, min_duration, max_duration = random.choice(self.alternative_scenarios)
            duration = random.uniform(min_duration, max_duration)
            return scenario, name, duration
    
    def _handle_signal(self, signum, frame):
        """Gère les signaux d'arrêt propre (SIGINT, SIGTERM)."""
        self.should_stop = True
    
    def stream(self):
        """
        Lance le flux continu de données avec transitions aléatoires.
        Tourne indéfiniment jusqu'à interruption (Ctrl+C ou SIGTERM).
        """
        # Enregistrer les gestionnaires de signaux
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)
        
        # Message de début
        print("=" * 80)
        print("FLUX CONTINU DE DONNÉES CARDIAQUES - SCÉNARIOS ALÉATOIRES")
        print("=" * 80)
        print(f"Scénario principal: {self.default_scenario.name.upper()}")
        print(f"Scénarios alternatifs: {', '.join(name for _, name, _, _ in self.alternative_scenarios)}")
        print(f"Fréquence d'échantillonnage: {self.sampling_rate} Hz")
        print("Appuyez sur Ctrl+C pour arrêter proprement")
        print("=" * 80)
        print()
        
        self.start_time = time.time()
        
        # Planifier le premier changement de scénario
        next_scenario, next_name, time_until_switch = self._schedule_next_scenario_switch()
        next_switch_time = time.time() + time_until_switch
        
        try:
            while not self.should_stop:
                # Vérifier si c'est le moment de changer de scénario
                current_time = time.time()
                if current_time >= next_switch_time:
                    # Changer de scénario silencieusement
                    self.engine.change_scenario(next_scenario)
                    self.current_scenario_name = next_name
                    self.scenario_switches += 1
                    
                    # Planifier le prochain changement
                    next_scenario, next_name, time_until_switch = self._schedule_next_scenario_switch()
                    next_switch_time = current_time + time_until_switch
                
                # Obtenir et afficher un échantillon
                data = self.engine.get_sample()
                print(data)
                
                # Collecter les statistiques
                self.total_samples += 1
                self.bpm_values.append(data.bpm)
                self.rr_values.append(data.rr_interval_ms)
                
                # Attendre le prochain échantillon
                time.sleep(1.0 / self.sampling_rate)
        
        except Exception as e:
            print(f"\n⚠️  Erreur inattendue: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
        
        finally:
            self._print_statistics()
    
    def _print_statistics(self):
        """Affiche les statistiques de fin."""
        if self.total_samples == 0:
            print("\nAucune donnée collectée.")
            return
        
        duration = time.time() - self.start_time if self.start_time else 0
        
        print()
        print("=" * 80)
        print("STATISTIQUES DE FIN")
        print("=" * 80)
        print(f"Durée totale: {duration:.1f} secondes ({duration/60:.1f} minutes)")
        print(f"Nombre d'échantillons: {self.total_samples}")
        print(f"Nombre de changements de scénario: {self.scenario_switches}")
        print()
        print(f"BPM moyen: {sum(self.bpm_values)/len(self.bpm_values):.1f}")
        print(f"BPM min: {min(self.bpm_values):.1f}")
        print(f"BPM max: {max(self.bpm_values):.1f}")
        print()
        print(f"RR moyen: {sum(self.rr_values)/len(self.rr_values):.0f} ms")
        print(f"RR min: {min(self.rr_values):.0f} ms")
        print(f"RR max: {max(self.rr_values):.0f} ms")
        
        # Calculer l'écart-type du RR (variabilité)
        rr_mean = sum(self.rr_values) / len(self.rr_values)
        rr_variance = sum((x - rr_mean) ** 2 for x in self.rr_values) / len(self.rr_values)
        rr_std = rr_variance ** 0.5
        print(f"Variabilité RR (écart-type): {rr_std:.0f} ms")
        print("=" * 80)


def main():
    """Fonction principale."""
    # Créer et lancer le flux
    stream = RandomScenarioStream(sampling_rate=1.0)
    stream.stream()


if __name__ == "__main__":
    main()

