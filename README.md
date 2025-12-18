# Heart Rate Kafka – Monitoring Cardiaque en Temps Réel

> Simulation et streaming de données cardiaques pour l'expérimentation de pipelines de données modernes

---

## 📊 Présentation Générale

**Heart Rate Kafka** est un projet personnel de simulation et de monitoring de fréquence cardiaque conçu pour alimenter une architecture de streaming événementiel moderne (Kafka → Spark → ML/Analytics). 

L'objectif principal est de **disposer d'un flux continu de données cardiaques réalistes** pour tester, prototyper et expérimenter avec :
- Des **pipelines de traitement de données en temps réel** (streaming avec Apache Kafka et Apache Spark)
- Des **scénarios de machine learning** appliqués à la santé connectée
- Une **architecture Big Data complète** orchestrée via Docker

À terme, ce projet vise à remplacer les données simulées par un **vrai capteur cardiaque Bluetooth Low Energy (BLE)**, permettant ainsi un monitoring temps réel authentique.

---

## 🎯 Cas d'Usage et Objectifs

### Cas d'usage typiques
Le projet simule différents états physiologiques d'un utilisateur :
- **Repos** : fréquence cardiaque au calme (~60 BPM)
- **Sommeil** : rythme ralenti avec variabilité accrue (~52 BPM)
- **Effort physique** : intensité progressive et personnalisable (jusqu'à 120-150 BPM)
- **Transitions réalistes** : passages fluides entre états (ex. repos → effort → récupération)

### Intérêts pédagogiques et techniques
- **Monitoring sportif et santé connectée** : comprendre les indicateurs cardiaques (BPM, HRV)
- **Expérimentation de pipelines data** : ingestion Kafka, traitement Spark, storage, visualisation
- **Prototypage IA/ML** : détection d'anomalies, classification d'activités, prédiction de patterns
- **Apprentissage de l'architecture événementielle** : streaming, partitionnement, scalabilité

---

## 🔬 Données Simulées (État Actuel)

### Génération factice mais réaliste
Pour l'instant, **toutes les données sont entièrement simulées** via un moteur Python sophistiqué. Ce simulateur génère :

- **BPM (Battements Par Minute)** : fréquence cardiaque instantanée
  - Repos : ~60 BPM (55-70)
  - Sommeil : ~52 BPM (45-60)
  - Effort : ~120 BPM (90-150, configurable)

- **HRV (Heart Rate Variability)** : variabilité cardiaque mesurée via les **intervalles RR** (temps entre deux battements consécutifs)
  - Repos : ~1000 ms ±100 ms
  - Sommeil : ~1150 ms ±150 ms (variabilité accrue, signe de relaxation)
  - Effort : ~500 ms ±50 ms (variabilité réduite, cœur sous tension)

### Réalisme physiologique
Le moteur de simulation intègre plusieurs caractéristiques pour garantir des données crédibles :
- **Transitions progressives** : limite physiologique de ~3-5 BPM/seconde lors des changements d'état
- **Oscillations lentes** : variabilité naturelle à long terme (cycles respiratoires, tonus vagal)
- **Bruit gaussien court-terme** : microvariations battement par battement

### Scénarios paramétrables
Plusieurs scénarios pré-configurés sont disponibles :
- `REST_SCENARIO` : état de repos standard
- `SLEEP_SCENARIO` : sommeil profond
- `EXERCISE_SCENARIO` : effort modéré personnalisable
- Scénarios **custom** : possibilité de définir vos propres paramètres (BPM cible, variance, etc.)

> 💡 **Note importante** : Ces données simulées servent de **remplaçant temporaire** en attendant l'intégration d'un capteur physique réel. Elles permettent de développer et valider toute la chaîne de traitement sans dépendre du matériel.

---

## 🛠️ Stack Technique (Vue d'Ensemble)

### Cœur applicatif : Python (`heart_app/`)
L'application Python est organisée en **modules orientés objet** pour garantir modularité et extensibilité :

- **`core/`** : composants fondamentaux
  - `data_models.py` : structures de données (`HeartData`, `ScenarioConfig`)
  - `sensor.py` : interface abstraite `ISensor` (permet de brancher n'importe quel type de capteur)
  - `engine.py` : moteur de simulation `HeartSimulationEngine` (orchestration du streaming)

- **`sensors/`** : implémentations de capteurs
  - `simulated_sensor.py` : capteur simulé actuel (génération algorithmique)
  - *(futur)* : `movesense_sensor.py`, `polar_sensor.py`, etc.

- **`scenarios/`** : bibliothèque de scénarios physiologiques pré-configurés

- **`utils/`** : utilitaires (fonctions de transition, calculs HRV, etc.)

- **`tests/`** : suite de tests complète avec pytest

### Interface utilisateur : CLI & Scripts de démo
- **CLI modulaire** (`python -m heart_app`) : permet de lancer facilement des simulations avec options personnalisables (durée, scénario, intensité, fréquence d'échantillonnage)
- **Scripts de démonstration** (`scripts/`) : exemples prêts à l'emploi pour découvrir chaque scénario
  - `demo_rest.py` : démonstration au repos
  - `demo_sleep.py` : simulation de sommeil
  - `demo_exercise.py` : effort avec phase de récupération
  - `demo_transitions.py` : enchaînement de plusieurs états

### Infrastructure data : Docker Compose
Le fichier `docker-compose.yml` orchestre une **stack complète de traitement de données** :

#### 🚀 Apache Kafka (streaming événementiel)
- **Zookeeper** : coordination du cluster Kafka
- **Kafka broker** : bus de messages pour ingestion des données cardiaques en temps réel
- **Kafka UI** : interface web pour visualiser topics, partitions, messages

#### ⚡ Apache Spark (traitement distribué)
- **Spark Master** : nœud de coordination
- **2 Workers Spark** : nœuds d'exécution pour paralléliser le traitement
- **Configuration** : jars Kafka pré-chargés pour connexion Kafka ↔ Spark

#### 📓 Jupyter Notebook
- Environnement interactif pour exploration de données et prototypage rapide
- Pré-configuré avec PySpark et accès au cluster Spark

### Applications Spark futures (`spark-apps/`)
Dossier prévu pour héberger les **jobs de traitement Spark** :
- **Consumers Kafka** : lecture des données en streaming ou batch
- **Transformations** : agrégations, windowing temporel, calcul de métriques dérivées
- **Outputs** : écriture vers bases de données, fichiers Parquet, dashboards, etc.
- **Notebooks** : expérimentation interactive avec les données réelles

---

## 🚀 Prise en Main Rapide

### Prérequis
- Python 3.8+ avec `pip` et `venv`
- Docker & Docker Compose (pour l'infrastructure Kafka/Spark, optionnel en phase 1)

### Installation

```bash
# 1. Cloner le dépôt
cd /home/ricardo/projects/heart_rate_kafka

# 2. Créer l'environnement virtuel Python
python3 -m venv .venv
source .venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt
```

### Vérification de l'installation

```bash
# Test rapide du moteur de simulation
python3 scripts/quick_check.py

# Tests complets (recommandé)
pytest heart_app/tests/ -v
```

### Premier lancement : simuler un flux cardiaque

```bash
# Simulation de 30 secondes au repos
python3 -m heart_app --scenario rest --duration 30

# Effort physique à 140 BPM pendant 1 minute
python3 -m heart_app --scenario exercise --intensity 140 --duration 60

# Sommeil en mode silencieux avec statistiques finales
python3 -m heart_app --scenario sleep --duration 20 --quiet --stats
```

### Lancer les scripts de démonstration

```bash
# Démonstration repos
python3 scripts/demo_rest.py

# Démonstration effort + récupération
python3 scripts/demo_exercise.py

# Démonstration transitions multiples
python3 scripts/demo_transitions.py
```

### Lancer l'infrastructure Docker (optionnel)

```bash
# Démarrer Kafka + Spark + Jupyter
docker-compose up -d

# Vérifier les services
docker-compose ps

# Accéder aux interfaces web :
# - Kafka UI : http://localhost:8080
# - Spark Master UI : http://localhost:9090
# - Jupyter Lab : http://localhost:8888 (token : voir .env)
```

---

## 🗺️ Roadmap et Évolutions Prévues

### Phase 1 : Capteur Simulé (✅ Terminé)
- [x] Moteur de simulation cardiaque réaliste
- [x] Plusieurs scénarios physiologiques (repos, sommeil, effort)
- [x] Transitions progressives entre états
- [x] CLI et scripts de démonstration
- [x] Architecture modulaire extensible

### Phase 2 : Infrastructure de Streaming (🚧 En cours)
- [x] Mise en place Kafka + Zookeeper
- [x] Mise en place Spark (master + workers)
- [x] Configuration Jupyter pour exploration
- [ ] Producteur Kafka pour envoyer les données simulées
- [ ] Consumer Kafka/Spark pour traitement en temps réel

### Phase 3 : Capteur Physique Réel (📋 À venir)
**Objectif principal** : remplacer le capteur simulé par un **vrai capteur BLE (Bluetooth Low Energy)**.

#### Benchmark de capteurs envisagé
- **Movesense** (choix privilégié actuellement)
  - SDK Python disponible
  - Précision médicale
  - Support RR intervals natif (crucial pour HRV)
  - Open-source friendly
- **Polar H10** (alternative)
  - Excellente précision
  - Bluetooth standard
  - Populaire dans le monde sportif
- Autres options : Wahoo TICKR, Garmin HRM-Pro, etc.

#### Intégration prévue
- Connexion BLE Python (via `bleak` ou SDK constructeur)
- Implémentation de `MovesenseSensor(ISensor)` conforme à l'interface existante
- Mode hybride : possibilité de basculer entre capteur réel et simulé
- Calibration et gestion des erreurs de connexion

### Phase 4 : Traitement Avancé & Machine Learning (🔮 Futur)
- **Traitement distribué Spark** :
  - Agrégations temporelles (fenêtres glissantes, windowing)
  - Calcul de métriques dérivées (RMSSD, pNN50, LF/HF ratio, etc.)
  - Détection d'anomalies en temps réel
  
- **Features avancées HRV** :
  - Analyse spectrale (domaine fréquentiel)
  - Métriques non-linéaires (entropie, Poincaré plot)
  - Corrélation avec contexte (heure, activité, stress)

- **Machine Learning** :
  - Classification d'activités (repos/effort/sommeil) via ML supervisé
  - Détection de patterns anormaux (arythmies, stress excessif)
  - Prédiction de zones de fréquence cardiaque optimales
  - Modèles de séries temporelles (LSTM, Prophet)

- **Visualisation & Monitoring** :
  - Dashboard temps réel (Grafana / Kibana / Streamlit)
  - Alertes personnalisables
  - Historique et tendances long terme

---

## 🌟 Perspectives et Ouverture

Ce projet est pensé comme un **terrain d'expérimentation complet** pour :
- Comprendre les architectures de streaming événementiel modernes
- Manipuler des données de santé connectée de manière éthique et contrôlée
- Prototyper des pipelines Big Data de bout en bout
- Explorer les applications de l'IA au monitoring physiologique

### Applications potentielles
- **Santé & Bien-être** : détection précoce de fatigue, optimisation de l'entraînement sportif
- **Recherche** : jeux de données cardiaques annotés pour publications scientifiques
- **IoT & Edge Computing** : traitement local sur appareil avant envoi vers le cloud
- **Prototypage produit** : base solide pour développer un vrai service de monitoring

### Philosophie du projet
- **Open & Éducatif** : code documenté, architecture claire, choix technologiques justifiés
- **Évolutif** : chaque composant peut être remplacé ou étendu sans tout reconstruire
- **Réaliste** : les données simulées et l'architecture sont conçues pour être représentatives d'un cas d'usage réel

---

## 📚 Ressources et Références

### Concepts clés abordés
- **Streaming événementiel** : Kafka, topics, partitioning, consumer groups
- **Traitement distribué** : Spark Structured Streaming, windowing, stateful operations
- **BLE (Bluetooth Low Energy)** : protocole de communication des capteurs modernes
- **HRV (Heart Rate Variability)** : indicateur clé de l'état du système nerveux autonome
- **Intervalles RR** : temps entre battements successifs, base du calcul de la HRV

### Technologies utilisées
- **Python** : langage principal (3.8+)
- **NumPy** : calculs mathématiques et génération aléatoire
- **Apache Kafka** : bus de messages distribué
- **Apache Spark** : moteur de traitement Big Data
- **Docker & Docker Compose** : conteneurisation et orchestration
- **Pytest** : framework de tests

---

## 📞 Contact & Contribution

Ce projet est développé dans un cadre personnel et pédagogique. Il est ouvert aux suggestions et aux retours constructifs.

Pour toute question, amélioration ou collaboration potentielle, n'hésitez pas à ouvrir une issue ou à proposer une pull request.

---

**Bon monitoring ! 💓📊**
