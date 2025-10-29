# Instructions de configuration rapide

## Installation des dépendances système (Ubuntu/WSL)

Avant de pouvoir exécuter l'application, installez les dépendances système nécessaires :

```bash
sudo apt update
sudo apt install python3-venv python3-pip python3-numpy
```

## Configuration de l'environnement Python

```bash
# Créer l'environnement virtuel
python3 -m venv .venv

# Activer l'environnement
source .venv/bin/activate

# Installer les dépendances Python
pip install -r requirements.txt
```

## Vérification de l'installation

```bash
# Vérification rapide
python3 scripts/quick_check.py

# Tests complets (nécessite pytest installé)
pytest heart_app/tests/ -v
```

## Exécution rapide sans installation complète

Si vous ne pouvez pas installer pip/venv immédiatement, vous pouvez installer numpy directement via apt :

```bash
sudo apt install python3-numpy

# Puis tester directement
python3 scripts/quick_check.py
```

## Démos disponibles

Une fois numpy installé, vous pouvez exécuter :

```bash
python3 scripts/demo_rest.py
python3 scripts/demo_sleep.py
python3 scripts/demo_exercise.py
python3 scripts/demo_transitions.py
```

## Application CLI

```bash
python3 -m heart_app --scenario rest --duration 10
python3 -m heart_app --scenario exercise --intensity 140 --duration 20
python3 -m heart_app --scenario sleep --stats --quiet
```

## Statut actuel de l'implémentation

✅ **Complété :**
- Architecture orientée objet complète
- Modèles de données (HeartData, ScenarioConfig)
- Interface abstraite ISensor
- Capteur simulé avec génération BPM + HRV
- 3 scénarios pré-configurés (repos, sommeil, effort)
- Transitions progressives réalistes
- Moteur de simulation (HeartSimulationEngine)
- Suite de tests complète (pytest)
- 4 scripts de démonstration
- CLI complet avec options
- Documentation complète

⏳ **Pour exécuter :**
- Installation de numpy (et optionnellement pytest)
- Voir les instructions ci-dessus

## Structure créée

```
heart_app/
├── core/
│   ├── data_models.py      ✅ HeartData, ScenarioConfig
│   ├── sensor.py           ✅ Interface ISensor
│   └── engine.py           ✅ HeartSimulationEngine
├── sensors/
│   └── simulated_sensor.py ✅ SimulatedHeartSensor
├── scenarios/
│   └── cardiac_scenarios.py ✅ REST, SLEEP, EXERCISE + custom
├── utils/
│   └── transitions.py      ✅ Fonctions de transition progressive
├── tests/                  ✅ Suite complète pytest
│   ├── test_data_models.py
│   ├── test_scenarios.py
│   ├── test_transitions.py
│   ├── test_sensor.py
│   └── test_engine.py
├── __main__.py             ✅ Point d'entrée CLI
└── README.md               ✅ Documentation

scripts/                    ✅ Tous créés
├── demo_rest.py
├── demo_sleep.py
├── demo_exercise.py
├── demo_transitions.py
└── quick_check.py
```

