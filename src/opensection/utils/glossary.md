# Glossaire Terminologique opensection

## Vue d'ensemble

Ce glossaire établit une correspondance claire entre la terminologie française et anglaise utilisée dans opensection. Il garantit la cohérence et facilite la compréhension pour les utilisateurs internationaux.

## Terminologie Fondamentale

| Français | Anglais | Définition |
|----------|---------|------------|
| **Section** | Section | Élément géométrique de calcul |
| **Béton** | Concrete | Matériau de base en compression |
| **Acier** | Steel | Matériau d'armature en traction |
| **Armature** | Reinforcement/Rebar | Barres d'acier dans le béton |
| **Effort normal** | Axial force | Force axiale N (kN) |
| **Moment** | Moment | Moment de flexion M (kN·m) |
| **Courbure** | Curvature | Variation de pente χ (rad/m) |
| **Déformation** | Strain | Allongement relatif ε |
| **Contrainte** | Stress | Force par unité de surface σ (MPa) |

## Propriétés Géométriques

| Français | Anglais | Définition |
|----------|---------|------------|
| **Largeur** | Width | Dimension horizontale b (m) |
| **Hauteur** | Height | Dimension verticale h (m) |
| **Diamètre** | Diameter | Dimension circulaire d (m) |
| **Aire** | Area | Surface A (m²) |
| **Inertie** | Moment of inertia | I (m⁴) |
| **Centre de gravité** | Centroid | Point d'équilibre géométrique |
| **Axe neutre** | Neutral axis | Ligne de déformation nulle |

## Matériaux et Résistance

| Français | Anglais | Définition |
|----------|---------|------------|
| **Résistance caractéristique** | Characteristic strength | fck, fyk (MPa) |
| **Résistance de calcul** | Design strength | fcd, fyd (MPa) |
| **Module d'élasticité** | Elastic modulus | E (MPa) |
| **Coefficient de sécurité** | Partial safety factor | γ |
| **Classe de béton** | Concrete class | C30/37, etc. |
| **Nuance d'acier** | Steel grade | B500, S235, etc. |

## Analyse et Résolution

| Français | Anglais | Définition |
|----------|---------|------------|
| **Solveur** | Solver | Algorithme de résolution |
| **Analyse par fibres** | Fiber analysis | Discrétisation en éléments |
| **Convergence** | Convergence | Critère d'arrêt itératif |
| **Itération** | Iteration | Étape de résolution |
| **Tolérance** | Tolerance | Précision numérique |
| **Matrice tangente** | Tangent matrix | Jacobienne du système |

## États Limites

| Français | Anglais | Définition |
|----------|---------|------------|
| **État limite ultime (ELU)** | Ultimate limit state (ULS) | Sécurité structurale |
| **État limite de service (ELS)** | Serviceability limit state (SLS) | Confort/utilisation |
| **Vérification** | Check/Verification | Contrôle de conformité |
| **Capacité** | Capacity | Résistance maximale |

## Charges et Sollicitations

| Français | Anglais | Définition |
|----------|---------|------------|
| **Charge** | Load | Force appliquée |
| **Sollicitation** | Action/Loading | Combinaison de charges |
| **Effort tranchant** | Shear force | V (kN) |
| **Moment de torsion** | Torsion moment | T (kN·m) |
| **Flexion composée déviée** | Biaxial bending | Flexion dans deux plans |

## Conventions de Code

### Noms de Variables
- Utiliser l'anglais pour les noms de variables et fonctions
- Commentaires en français pour la documentation utilisateur
- Commentaires en anglais pour la documentation technique

### Exemple :
```python
# Fonction en anglais (standard Python)
def compute_section_properties(self) -> GeometricProperties:
    """
    Calcule les propriétés géométriques de la section.

    Returns:
        GeometricProperties: Propriétés calculées (aire, inertie, etc.)
    """
    # Code avec variables en anglais
    total_area = 0.0
    for contour in self.contours:
        area = contour.area()
        total_area += area
```

### Commentaires
- Commentaires de code : Anglais (standard pour Python scientifique)
- Docstrings : Français pour les utilisateurs finaux
- Documentation README : Français

## Règles de Traduction

1. **Termes normalisés** : Utiliser systématiquement les termes de ce glossaire
2. **Cohérence** : Même terme anglais = même terme français dans tout le projet
3. **Contexte** : Adapter la traduction selon le contexte technique
4. **Évolution** : Mettre à jour ce glossaire lors de l'ajout de nouvelles fonctionnalités

## Références

- **Eurocode 2** : Terminologie officielle EN 1992-1-1
- **Python conventions** : PEP 8 et pratiques scientifiques
- **Génie civil français** : Vocabulaire courant des BET
