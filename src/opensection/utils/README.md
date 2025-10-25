# Utils Module

Le module `utils` fournit des outils essentiels pour opensection :

## Structure

- **units.py** : Conversions d'unités
  - `UnitConverter` : Convertisseur principal
  - `Length`, `Force`, `Stress`, `Area`, `Moment` : Classes de conversion spécialisées

- **constants.py** : Constantes physiques et numériques
  - `MaterialConstants` : Propriétés des matériaux (E, gamma, etc.)
  - `NumericalConstants` : Paramètres numériques (tolérance, max_iter, etc.)
  - `GeometricConstants` : Constantes géométriques (PI, etc.)

- **math_helpers.py** : Fonctions mathématiques utilitaires
  - `safe_divide` : Division sécurisée (évite /0)
  - `normalize_vector` : Normalisation de vecteur
  - `is_converged` : Test de convergence
  - `clamp` : Limitation de valeurs
  - Et bien d'autres...

## Système d'unités

opensection utilise le système d'unités suivant :

| Grandeur | Unité | Symbole |
|----------|-------|---------|
| Longueur | mètre | m |
| Force | kilonewton | kN |
| Contrainte | mégapascal | MPa |
| Moment | kilonewton-mètre | kN·m |
| Aire | mètre carré | m² |
| Inertie | mètre puissance 4 | m⁴ |

### Conversion clé

La conversion la plus importante à comprendre :

```
σ (MPa) × A (m²) = F (MN)
```

Car 1 MPa = 1 N/mm² et 1 m² = 10⁶ mm² :

```
σ (N/mm²) × 10⁶ (mm²) = F × 10⁶ (N) = F (MN)
```

Pour convertir en kN, multiplier par 1000 :

```python
F_kN = sigma_MPa * area_m2 * 1000
```

Ceci est géré automatiquement par `UnitConverter.stress_area_to_force()`.

## Exemples d'utilisation

```python
from opensection.utils import (
    UnitConverter, 
    MaterialConstants, 
    NumericalConstants,
    safe_divide,
    clamp,
    is_converged
)

# Conversions d'unités
sigma = 10.0  # MPa
area = 0.01   # m² (100 cm²)
force = UnitConverter.stress_area_to_force(sigma, area)  # 100 kN

# Constantes
E_steel = MaterialConstants.E_STEEL_DEFAULT  # 200000 MPa
tol = NumericalConstants.TOL_FORCE_DEFAULT   # 1e-6 kN

# Fonctions mathématiques
result = safe_divide(10, 0, default=0.0)     # 0.0
value = clamp(15, 0, 10)                     # 10
converged = is_converged([1e-7, 1e-8], 1e-6) # True
```

## Méthodologie de Calcul

### Analyse par Fibres
Le solveur utilise la méthode d'analyse par fibres pour calculer le comportement non-linéaire des sections en béton armé :

```
Section discrétisée en fibres élémentaires
Chaque fibre : σ_i = f(ε_i) selon loi matériau
Effort total : N = Σ(σ_i ⋅ A_i)
Moment : M = Σ(σ_i ⋅ A_i ⋅ d_i)
```

### Algorithme de Newton-Raphson
Résolution itérative du système non-linéaire :
```
F(d) = [N(d), M_y(d), M_z(d)]^T = [N_cible, M_y_cible, M_z_cible]^T
d^{k+1} = d^k - J^{-1}(d^k) ⋅ F(d^k)
```

### Convergence
Critères de convergence basés sur :
- Tolérance force : ||F|| < TOL_FORCE (1e-6 kN)
- Tolérance déplacement : ||Δd|| < TOL_DISPLACEMENT (1e-9 m)

## Intégration dans le solver

Le module `utils` est utilisé dans `section_solver.py` pour :

1. **Conversions d'unités** : `UnitConverter` garantit la cohérence entre MPa, m², kN
2. **Constantes numériques** : `NumericalConstants` centralise les paramètres de convergence
3. **Fonctions mathématiques** : `safe_divide`, `clamp`, `is_converged` améliorent la robustesse

Cela rend le code plus maintenable et évite les erreurs d'unités.

## Références Théoriques

- **Eurocode 2** : EN 1992-1-1:2004 (Design of concrete structures)
- **Analyse par fibres** : Mari & Scordelis (1984), Spacone et al. (1996)
- **Newton-Raphson** : Crisfield (1991) - Non-linear Finite Element Analysis

