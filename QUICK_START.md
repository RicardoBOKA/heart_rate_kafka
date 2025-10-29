# 🚀 Quick Start - Moteur de Simulation Cardiaque

## ⚡ Démarrage ultra-rapide

### 1️⃣ Installer numpy (minimum requis)

```bash
sudo apt install python3-numpy
```

### 2️⃣ Tester immédiatement

```bash
cd /home/ricardo/projects/heart_rate_kafka
python3 scripts/quick_check.py
```

### 3️⃣ Lancer une démo

```bash
# Simulation de repos (30 secondes)
python3 scripts/demo_rest.py

# Simulation avec transitions
python3 scripts/demo_transitions.py
```

---

## 📦 Installation complète (recommandé)

### Étape 1 : Dépendances système

```bash
sudo apt update
sudo apt install python3-venv python3-pip
```

### Étape 2 : Environnement virtuel

```bash
cd /home/ricardo/projects/heart_rate_kafka
python3 -m venv .venv
source .venv/bin/activate
```

### Étape 3 : Dépendances Python

```bash
pip install -r requirements.txt
```

### Étape 4 : Tests

```bash
pytest heart_app/tests/ -v
```

---

## 🎯 Utilisation

### CLI Interactive

```bash
# Exécuter via le module
python3 -m heart_app --help

# Repos pendant 30 secondes
python3 -m heart_app --scenario rest --duration 30

# Effort à 140 BPM pendant 60 secondes
python3 -m heart_app --scenario exercise --intensity 140 --duration 60

# Mode silencieux avec statistiques
python3 -m heart_app --scenario sleep --quiet --stats
```

### Scripts de démonstration

```bash
# 1. Repos (30s)
python3 scripts/demo_rest.py

# 2. Sommeil (30s)
python3 scripts/demo_sleep.py

# 3. Effort + récupération
python3 scripts/demo_exercise.py

# 4. Transitions multiples (tous les scénarios)
python3 scripts/demo_transitions.py
```

### Utilisation programmatique

```python
from heart_app.sensors import SimulatedHeartSensor
from heart_app.core.engine import HeartSimulationEngine
from heart_app.scenarios import REST_SCENARIO, EXERCISE_SCENARIO

# Créer le capteur
sensor = SimulatedHeartSensor(initial_scenario=REST_SCENARIO)

# Créer le moteur (1 échantillon/seconde)
engine = HeartSimulationEngine(sensor, sampling_rate=1.0)

# Lecture unique
data = engine.get_sample()
print(f"BPM: {data.bpm:.1f}, RR: {data.rr_interval_ms:.0f}ms")

# Stream pendant 10 secondes
for data in engine.stream(duration=10.0):
    print(data)

# Changer de scénario avec transition progressive
engine.change_scenario(EXERCISE_SCENARIO)

# Continuer le stream
for data in engine.stream(duration=20.0):
    print(data)
```

---

## 📊 Exemples de sortie

### Données en console

```
[rest] BPM: 58.3 | RR: 1030ms | Time: 0.00s
[rest] BPM: 60.1 | RR: 998ms | Time: 1.01s
[rest] BPM: 61.5 | RR: 976ms | Time: 2.02s
```

### Statistiques

```
============================================================
STATISTIQUES DE LA SIMULATION
============================================================
Scénario: rest
Échantillons collectés: 30
Durée effective: 30.00 secondes

BPM (Battements par minute):
  Moyenne: 60.2 BPM
  Minimum: 55.8 BPM
  Maximum: 64.3 BPM
  Cible: 60.0 ±5.0 BPM

Intervalles RR (HRV):
  Moyenne: 998 ms
  Écart-type: 95 ms
  Cible: 1000 ±100 ms
============================================================
```

---

## 🧪 Tests disponibles

```bash
# Tous les tests
pytest heart_app/tests/ -v

# Tests spécifiques
pytest heart_app/tests/test_sensor.py -v
pytest heart_app/tests/test_engine.py -v

# Avec couverture
pytest --cov=heart_app heart_app/tests/

# Mode verbeux avec détails
pytest -vv heart_app/tests/
```

---

## 🎓 Scénarios disponibles

| Scénario | BPM cible | RR moyen | Description |
|----------|-----------|----------|-------------|
| **rest** | 60 ±5 | 1000 ms ±100 | Repos, calme |
| **sleep** | 52 ±4 | 1150 ms ±150 | Sommeil profond |
| **exercise** | 120 ±10 | 500 ms ±50 | Effort modéré |
| **custom** | Variable | Calculé | Intensité personnalisée |

---

## 🔧 Options CLI complètes

```
Options disponibles:
  --scenario {rest,sleep,exercise}
                        Scénario à simuler (défaut: rest)
  
  --duration SECONDS    Durée de la simulation (défaut: 30)
  
  --rate HZ             Fréquence d'échantillonnage (défaut: 1.0)
  
  --intensity BPM       BPM cible pour l'effort
                        (uniquement avec --scenario exercise)
  
  --quiet               Mode silencieux (seulement stats finales)
  
  --stats               Affiche statistiques détaillées
```

### Exemples avancés

```bash
# Échantillonnage rapide (5 Hz)
python3 -m heart_app --scenario rest --rate 5.0 --duration 10

# Effort intense personnalisé
python3 -m heart_app --scenario exercise --intensity 160 --duration 30

# Long sommeil avec stats
python3 -m heart_app --scenario sleep --duration 300 --stats
```

---

## 📚 Documentation complète

- **heart_app/README.md** : Documentation de l'application
- **PROJECT_SUMMARY.md** : Résumé complet du projet
- **INSTALLATION.md** : Guide d'installation détaillé
- **SETUP_INSTRUCTIONS.md** : Instructions de configuration

---

## ✅ Checklist de vérification

Après installation, vérifiez que tout fonctionne :

- [ ] `python3 scripts/quick_check.py` → ✅ SUCCÈS
- [ ] `python3 scripts/demo_rest.py` → Affiche données
- [ ] `python3 -m heart_app --help` → Affiche l'aide
- [ ] `pytest heart_app/tests/ -v` → Tous les tests passent

---

## 🆘 Résolution de problèmes

### ❌ "No module named 'numpy'"

```bash
# Solution rapide
sudo apt install python3-numpy

# Ou via pip
pip install numpy
```

### ❌ "No module named 'pytest'"

```bash
pip install pytest
```

### ❌ "Command 'python' not found"

```bash
# Utiliser python3
python3 -m heart_app
```

---

## 📞 Support

Pour toute question ou problème :

1. Consultez `PROJECT_SUMMARY.md` pour vue d'ensemble
2. Lisez `heart_app/README.md` pour détails API
3. Examinez les tests dans `heart_app/tests/` pour exemples

---

**Bon codage ! 🎉**

