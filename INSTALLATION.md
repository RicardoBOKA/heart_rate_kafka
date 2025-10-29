# Guide d'installation - Heart App

## Prérequis système

Sur les systèmes Debian/Ubuntu (incluant WSL), vous devez installer les packages suivants :

```bash
sudo apt update
sudo apt install python3-venv python3-pip
```

## Installation de l'environnement

### 1. Créer l'environnement virtuel

```bash
cd /home/ricardo/projects/heart_rate_kafka
python3 -m venv .venv
```

### 2. Activer l'environnement virtuel

```bash
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Vérification de l'installation

### Exécuter les tests

```bash
pytest heart_app/tests/ -v
```

### Tester un script de démonstration

```bash
python scripts/demo_rest.py
```

### Utiliser l'application CLI

```bash
python -m heart_app --scenario rest --duration 10
```

## Structure du projet après installation

```
heart_rate_kafka/
├── .venv/              # Environnement virtuel Python
├── heart_app/          # Application principale
│   ├── core/
│   ├── sensors/
│   ├── scenarios/
│   ├── utils/
│   └── tests/
├── scripts/            # Scripts de démonstration
├── requirements.txt    # Dépendances Python
└── docker-compose.yml  # Configuration Kafka (pour plus tard)
```

## Résolution de problèmes

### Erreur : "No module named pytest"

```bash
# Assurez-vous que l'environnement virtuel est activé
source .venv/bin/activate

# Installez les dépendances
pip install -r requirements.txt
```

### Erreur : "ensurepip is not available"

```bash
# Installez python3-venv
sudo apt install python3-venv python3-pip
```

### Erreur : "Command 'python' not found"

```bash
# Utilisez python3 au lieu de python
python3 -m heart_app
```

## Prochaines étapes

Une fois l'installation terminée, vous pouvez :

1. Exécuter les tests : `pytest heart_app/tests/ -v`
2. Essayer les démos : `python scripts/demo_rest.py`
3. Explorer l'API : voir `heart_app/README.md`
4. Développer de nouveaux capteurs ou scénarios

