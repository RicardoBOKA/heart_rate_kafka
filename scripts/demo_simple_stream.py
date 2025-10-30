#!/usr/bin/env python3
"""
Script de démonstration : Flux continu simple (scénario REST)
Génère un flux infini de données cardiaques au repos.
"""

import sys
import os
import signal
import time
from typing import List

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from heart_app.sensors import SimulatedHeartSensor
from heart_app.core.engine import HeartSimulationEngine
from heart_app.scenarios import REST_SCENARIO


class SimpleStream:
    """Gestionnaire de flux continu simple en mode repos."""
    
    def __init__(self, sampling_rate: float = 1.0):
        """
        Initialise le gestionnaire de flux.
        
        Args:
            sampling_rate: Fréquence d'échantillonnage en Hz
        """
        self.sampling_rate = sampling_rate
        self.sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
        self.engine = HeartSimulationEngine(self.sensor, sampling_rate=sampling_rate)
        
        # Statistiques
        self.total_samples = 0
        self.bpm_values: List[float] = []
        self.rr_values: List[float] = []
        self.start_time = None
        
        # Flag d'arrêt
        self.should_stop = False
    
    def _handle_signal(self, signum, frame):
        """Gère les signaux d'arrêt propre (SIGINT, SIGTERM)."""
        self.should_stop = True
    
    def stream(self):
        """
        Lance le flux continu de données.
        Tourne indéfiniment jusqu'à interruption (Ctrl+C ou SIGTERM).
        """
        # Enregistrer les gestionnaires de signaux
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)
        
        # Message de début
        print("=" * 80)
        print("FLUX CONTINU DE DONNÉES CARDIAQUES - SCÉNARIO REPOS")
        print("=" * 80)
        print(f"Scénario: {REST_SCENARIO.name.upper()} (cible: {REST_SCENARIO.target_bpm} BPM)")
        print(f"Fréquence d'échantillonnage: {self.sampling_rate} Hz")
        print("Appuyez sur Ctrl+C pour arrêter proprement")
        print("=" * 80)
        print()
        
        self.start_time = time.time()
        
        try:
            while not self.should_stop:
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
    stream = SimpleStream(sampling_rate=1.0)
    stream.stream()


if __name__ == "__main__":
    main()

