# Heart App - Moteur de Simulation Cardiaque

Application Python modulaire et orientée objet pour la simulation de données cardiaques réalistes.

## Vue d'ensemble

Heart App est un moteur de simulation qui génère des données cardiaques (BPM et HRV) selon différents scénarios physiologiques (repos, sommeil, effort). L'architecture est conçue pour être facilement extensible avec de nouveaux capteurs, métriques et scénarios.

## Architecture

### Structure du projet

```
heart_app/
├── core/               # Composants centraux
│   ├── data_models.py  # HeartData, ScenarioConfig
│   ├── sensor.py       # Interface ISensor
│   └── engine.py       # HeartSimulationEngine
├── sensors/            # Implémentations de capteurs
│   └── simulated_sensor.py
├── scenarios/          # Scénarios pré-configurés
│   └── cardiac_scenarios.py
├── utils/              # Utilitaires
│   └── transitions.py
└── tests/              # Tests pytest
```

### Concepts clés

#### 1. Interface ISensor
Interface abstraite permettant d'intégrer différents types de capteurs :
- Capteurs simulés (pour développement/tests)
- Capteurs réels (futurs)
- Capteurs hybrides

#### 2. ScenarioConfig
Configuration d'un scénario cardiaque avec :
- BPM cible et variance
- Intervalles RR cibles et variance
- Métadonnées descriptives

#### 3. HeartSimulationEngine
Orchestrateur principal gérant :
- Lecture des données via le capteur
- Streaming continu avec fréquence configurable
- Changements de scénarios avec transitions progressives

## Métriques simulées

### BPM (Battements par minute)
- **Repos** : ~60 BPM (55-70)
- **Sommeil** : ~52 BPM (45-60)
- **Effort** : ~120 BPM (90-150, configurable)

### HRV (Variabilité via intervalles RR)
- **Repos** : ~1000 ms ±100 ms
- **Sommeil** : ~1150 ms ±150 ms (variabilité accrue)
- **Effort** : ~500 ms ±50 ms (variabilité réduite)

## Caractéristiques

### Transitions progressives
Les changements de scénario sont progressifs et réalistes :
- Limite de changement : ~3-5 BPM/seconde
- Interpolation douce
- Respect des contraintes physiologiques

### Variabilité réaliste
- Oscillations lentes et naturelles
- Bruit gaussien court-terme
- Variabilité proportionnelle au scénario

## Utilisation

### CLI principal

```bash
# Exécuter via le module
python -m heart_app --scenario rest --duration 30

# Scénario d'effort personnalisé
python -m heart_app --scenario exercise --intensity 140 --duration 60

# Mode silencieux avec statistiques
python -m heart_app --scenario sleep --duration 20 --quiet --stats
```

### Dans le code

```python
from heart_app.sensors import SimulatedHeartSensor
from heart_app.core.engine import HeartSimulationEngine
from heart_app.scenarios import REST_SCENARIO

# Créer le capteur et le moteur
sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)
engine = HeartSimulationEngine(sensor, sampling_rate=1.0)

# Lecture unique
data = engine.get_sample()
print(f"BPM: {data.bpm}, RR: {data.rr_interval_ms}")

# Streaming continu
for data in engine.stream(duration=10.0):
    print(data)
```

### Scripts de démonstration

```bash
# Démonstration repos (30s)
python scripts/demo_rest.py

# Démonstration sommeil (30s)
python scripts/demo_sleep.py

# Démonstration effort avec récupération
python scripts/demo_exercise.py

# Démonstration transitions multiples
python scripts/demo_transitions.py
```

## Tests

Exécuter tous les tests avec pytest :

```bash
# Tous les tests
pytest heart_app/tests/

# Tests spécifiques
pytest heart_app/tests/test_sensor.py

# Avec couverture
pytest --cov=heart_app heart_app/tests/

# Mode verbeux
pytest -v heart_app/tests/
```

## Extension du système

### Ajouter un nouveau scénario

```python
from heart_app.core.data_models import ScenarioConfig

CUSTOM_SCENARIO = ScenarioConfig(
    name="custom",
    target_bpm=80.0,
    bpm_variance=6.0,
    target_rr_ms=750.0,
    rr_variance=80.0,
    description="Mon scénario personnalisé"
)
```

### Implémenter un capteur réel

```python
from heart_app.core.sensor import ISensor
from heart_app.core.data_models import HeartData

class RealHeartSensor(ISensor):
    def read(self) -> HeartData:
        # Lecture depuis matériel réel
        ...
    
    def set_scenario(self, scenario):
        # Configuration du capteur
        ...
    
    def reset(self):
        # Réinitialisation
        ...
```

### Ajouter une nouvelle métrique

1. Étendre `HeartData` dans `data_models.py`
2. Modifier le capteur pour générer la nouvelle métrique
3. Mettre à jour les tests

## Dépendances

- **numpy** : Génération aléatoire et calculs mathématiques
- **pytest** : Framework de tests

## Roadmap

### Prochaines étapes
- [ ] Ajout d'une API REST (FastAPI)
- [ ] Intégration avec Kafka pour streaming
- [ ] Support de capteurs réels
- [ ] Métriques avancées (SpO2, pression artérielle)
- [ ] Persistence des données (base de données)
- [ ] Visualisation en temps réel

## Licence

MIT

