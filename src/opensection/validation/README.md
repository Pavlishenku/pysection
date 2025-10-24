

# Module de Validation opensection

Ce module fournit des outils pour valider les données d'entrée et garantir la cohérence avant les calculs.

## Objectif

Éviter les erreurs courantes de l'utilisateur :
- ✓ Dimensions négatives ou aberrantes
- ✓ Armatures hors de la section
- ✓ Résistances matériaux hors normes EC2
- ✓ Charges irréalistes
- ✓ Erreurs d'unités
- ✓ Enrobages insuffisants
- ✓ Taux d'armature min/max

## Structure

```
validation/
├── __init__.py         # Exports
├── exceptions.py       # Exceptions personnalisées
├── validators.py       # Classes de validation
└── README.md           # Ce fichier
```

## Classes de Validation

### 1. GeometryValidator

Valide les paramètres géométriques :

```python
from opensection.validation import GeometryValidator

# Valider une dimension
GeometryValidator.validate_dimension(0.3, "largeur")  # OK
GeometryValidator.validate_dimension(0.005, "largeur")  # Erreur : trop petit

# Valider une section rectangulaire
GeometryValidator.validate_rectangular_section(0.3, 0.5)  # OK

# Vérifier qu'un point est dans la section
inside = GeometryValidator.validate_point_in_rectangle(
    y=0.1, z=0.05, width=0.3, height=0.5
)
```

**Limites :**
- Dimension min : 1 cm
- Dimension max : 10 m
- Ratio H/L > 10 : avertissement

### 2. MaterialValidator

Valide les propriétés des matériaux selon EC2 :

```python
from opensection.validation import MaterialValidator

# Valider résistance béton
MaterialValidator.validate_concrete_strength(30)  # OK (C30/37)
MaterialValidator.validate_concrete_strength(10)  # Erreur : < C12/15

# Valider acier
MaterialValidator.validate_steel_strength(500)  # OK (B500)
MaterialValidator.validate_steel_strength(300)  # Erreur : trop faible

# Coefficients de sécurité
MaterialValidator.validate_safety_factor(1.5, "gamma_c")  # OK
```

**Limites EC2 :**
- Béton : C12/15 à C90/105 (12-90 MPa)
- Acier : B400 à B600 (400-600 MPa)
- Gamma >= 1.0

### 3. RebarValidator

Valide les armatures :

```python
from opensection.validation import RebarValidator

# Valider diamètre
RebarValidator.validate_diameter(0.016)  # OK (HA16)
RebarValidator.validate_diameter(0.004)  # Erreur : trop petit

# Valider position dans section
RebarValidator.validate_rebar_position(
    y=0.20, z=0.0, diameter=0.016,
    section_width=0.3, section_height=0.5,
    cover=0.03  # Enrobage 3 cm
)

# Valider taux d'armature
RebarValidator.validate_minimum_reinforcement(As=0.0006, Ac=0.15)  # 0.4%
RebarValidator.validate_maximum_reinforcement(As=0.0006, Ac=0.15)  # 0.4%
```

**Limites :**
- Diamètre : 6 mm à 50 mm
- Diamètres standards : 6, 8, 10, 12, 14, 16, 20, 25, 32, 40, 50 mm
- Taux min : 0.2% (EC2)
- Taux max : 8% (EC2)
- Enrobage min : 3 cm (recommandé)

### 4. LoadValidator

Valide les charges appliquées :

```python
from opensection.validation import LoadValidator

# Valider effort normal
LoadValidator.validate_axial_load(
    N=500,  # kN
    section_area=0.15,  # m²
    concrete_strength=17  # MPa
)

# Valider moment
LoadValidator.validate_moment(
    M=100,  # kN·m
    section_height=0.5,  # m
    section_area=0.15,  # m²
    concrete_strength=17  # MPa
)

# Vérifier cohérence unités
LoadValidator.validate_unit_consistency(N=500, M=100)
```

**Vérifications :**
- Charge < 2× capacité estimée
- Cohérence des unités (kN, kN·m)

### 5. SectionValidator

Validation globale d'une section complète :

```python
from opensection.validation import SectionValidator
from opensection import RectangularSection, ConcreteEC2, SteelEC2, RebarGroup

section = RectangularSection(width=0.3, height=0.5)
concrete = ConcreteEC2(fck=30)
steel = SteelEC2(fyk=500)
rebars = RebarGroup()
rebars.add_rebar(y=0.20, z=0.0, diameter=0.016, n=3)

# Valider tout
SectionValidator.validate_all(
    section, concrete, steel, rebars,
    N=500, M_y=0, M_z=100
)
```

## Exceptions

```python
from opensection.validation import (
    ValidationError,            # Exception de base
    GeometryValidationError,    # Erreur géométrie
    MaterialValidationError,    # Erreur matériau
    RebarValidationError,       # Erreur armatures
    LoadValidationError,        # Erreur charges
)

try:
    GeometryValidator.validate_dimension(-0.5, "largeur")
except GeometryValidationError as e:
    print(f"Erreur : {e}")
```

## Utilisation Recommandée

### 1. Validation automatique dans le solver

```python
from opensection import SectionSolver
from opensection.validation import SectionValidator

# Créer section, matériaux, armatures...
section = RectangularSection(width=0.3, height=0.5)
concrete = ConcreteEC2(fck=30)
steel = SteelEC2(fyk=500)
rebars = RebarGroup()
rebars.add_rebar(y=0.20, z=0.0, diameter=0.016, n=3)

# Valider AVANT de créer le solver
SectionValidator.validate_all(section, concrete, steel, rebars, N=500, M_z=100)

# Créer le solver (données validées)
solver = SectionSolver(section, concrete, steel, rebars)
result = solver.solve(N=500, M_z=100)
```

### 2. Validation progressive

```python
from opensection.validation import GeometryValidator, RebarValidator

# Valider au fur et à mesure de la saisie
width = 0.3
height = 0.5
GeometryValidator.validate_dimension(width, "largeur")
GeometryValidator.validate_dimension(height, "hauteur")

section = RectangularSection(width=width, height=height)

# Valider chaque armature avant ajout
y, z, dia = 0.20, 0.0, 0.016
RebarValidator.validate_diameter(dia)
RebarValidator.validate_rebar_position(y, z, dia, width, height)
rebars.add_rebar(y=y, z=z, diameter=dia, n=3)
```

### 3. Gestion des erreurs

```python
from opensection.validation import ValidationError

try:
    SectionValidator.validate_all(section, concrete, steel, rebars, N=500)
except ValidationError as e:
    print(f"Erreur de validation : {e}")
    print("Vérifiez vos données d'entrée")
    # Demander à l'utilisateur de corriger
except Exception as e:
    print(f"Erreur inattendue : {e}")
    # Logger l'erreur
```

## Avertissements vs Erreurs

Le module utilise deux niveaux de vérification :

**Erreurs (exceptions levées) :**
- Données invalides qui empêchent le calcul
- Hors des limites EC2
- Violations physiques (armature hors section)

**Avertissements (warnings) :**
- Données inhabituelles mais possibles
- Valeurs non-standard
- Situations à risque (congestion, etc.)

```python
import warnings

# Capturer les avertissements
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    MaterialValidator.validate_concrete_strength(33)  # Non-standard
    if w:
        print(f"Avertissement : {w[0].message}")
```

## Exemples d'Erreurs Détectées

### Armature hors section
```python
rebars.add_rebar(y=0.30, z=0.0, diameter=0.016, n=3)
SectionValidator.validate_all(...)
# RebarValidationError: Armature hors section (y = 30.0 cm, hauteur = 50.0 cm)
```

### Béton trop faible
```python
concrete = ConcreteEC2(fck=10)
MaterialValidator.validate_concrete_strength(10)
# MaterialValidationError: Résistance béton trop faible : 10 MPa (minimum EC2 : 12 MPa)
```

### Dimension négative
```python
section = RectangularSection(width=-0.3, height=0.5)
# GeometryValidationError: Largeur doit être positif, reçu : -0.3
```

### Charge aberrante
```python
LoadValidator.validate_axial_load(N=500000, section_area=0.15, concrete_strength=17)
# LoadValidationError: Effort normal très élevé : 500000 kN (capacité ≈ 2550 kN)
```

## Tests

Le module est entièrement testé :

```bash
pytest tests/test_validation.py -v
```

**Couverture : > 90%**

## Intégration Future

Le module de validation pourra être intégré automatiquement dans :
- Les constructeurs de classes (Section, Material, etc.)
- Le solver (validation avant calcul)
- Les interfaces graphiques (validation temps réel)
- Les API web (validation des requêtes)

## Contribuer

Pour ajouter de nouvelles validations :
1. Ajouter la méthode dans la classe appropriée de `validators.py`
2. Ajouter les tests dans `test_validation.py`
3. Documenter dans ce README
4. S'assurer que les messages d'erreur sont clairs et en français

