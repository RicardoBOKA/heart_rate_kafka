"""
Fonctions pour gérer les transitions progressives entre scénarios.
"""

import numpy as np


def interpolate(current_value: float, target_value: float, alpha: float) -> float:
    """
    Interpole linéairement entre la valeur actuelle et la valeur cible.
    
    Args:
        current_value: Valeur actuelle
        target_value: Valeur cible
        alpha: Facteur d'interpolation (0.0 = current, 1.0 = target)
        
    Returns:
        Valeur interpolée
    """
    alpha = np.clip(alpha, 0.0, 1.0)
    return current_value + (target_value - current_value) * alpha


def smooth_transition(
    current_value: float,
    target_value: float,
    max_change_per_step: float
) -> float:
    """
    Effectue une transition progressive vers une valeur cible avec limite de changement.
    
    Cette fonction assure que la transition est réaliste en limitant le changement
    maximum par appel (par exemple, max 3-5 BPM par seconde).
    
    Args:
        current_value: Valeur actuelle
        target_value: Valeur cible à atteindre
        max_change_per_step: Changement maximum autorisé par étape
        
    Returns:
        Nouvelle valeur après transition limitée
        
    Examples:
        >>> smooth_transition(60.0, 120.0, 5.0)
        65.0  # Montée de 5 BPM maximum
        
        >>> smooth_transition(120.0, 60.0, 5.0)
        115.0  # Descente de 5 BPM maximum
    """
    difference = target_value - current_value
    
    # Si la différence est petite, on va directement à la cible
    if abs(difference) <= max_change_per_step:
        return target_value
    
    # Sinon, on progresse avec la limite de changement
    step = max_change_per_step if difference > 0 else -max_change_per_step
    return current_value + step


def calculate_transition_progress(
    elapsed_time: float,
    transition_duration: float
) -> float:
    """
    Calcule le progrès d'une transition en fonction du temps écoulé.
    
    Args:
        elapsed_time: Temps écoulé depuis le début de la transition (secondes)
        transition_duration: Durée totale de la transition (secondes)
        
    Returns:
        Progrès entre 0.0 (début) et 1.0 (fin)
    """
    if transition_duration <= 0:
        return 1.0
    
    progress = elapsed_time / transition_duration
    return np.clip(progress, 0.0, 1.0)


def ease_in_out(t: float) -> float:
    """
    Fonction d'easing pour des transitions plus naturelles.
    
    Applique une courbe ease-in-out (lent au début et à la fin, rapide au milieu).
    
    Args:
        t: Valeur entre 0.0 et 1.0
        
    Returns:
        Valeur transformée entre 0.0 et 1.0 avec easing
    """
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)

