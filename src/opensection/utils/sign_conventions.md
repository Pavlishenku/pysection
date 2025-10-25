# Conventions de Signe dans opensection

## Vue d'ensemble

opensection utilise des conventions de signe mixtes adaptées aux pratiques du génie civil pour le béton armé :

- **Béton** : Convention traditionnelle du béton armé
- **Acier** : Convention mécanique classique

Cette approche est nécessaire car le béton et l'acier ont des comportements différents dans les structures en béton armé.

## Conventions Détaillées

### Béton (ConcreteEC2)
```
Déformation (ε) :
- ε > 0 : Compression
- ε < 0 : Traction

Contrainte (σ) :
- σ > 0 : Compression
- σ < 0 : Traction
```

### Acier (SteelEC2)
```
Déformation (ε) :
- ε > 0 : Traction
- ε < 0 : Compression

Contrainte (σ) :
- σ > 0 : Traction
- σ < 0 : Compression
```

## Cohérence dans le Solveur

Dans le solveur `SectionSolver`, les déformations sont calculées de manière cohérente :

```
ε(y,z) = ε₀ + χ_y ⋅ (y - y_cg) + χ_z ⋅ (z - z_cg)
```

Où :
- `ε₀` : Déformation axiale (même signe pour béton et acier)
- `χ_y`, `χ_z` : Courbures (même signe pour béton et acier)
- `y`, `z` : Coordonnées (même référentiel géométrique)

## Exemple Pratique

Pour une section en flexion simple (flexion autour de z) :

```
Section verticale (y positif vers le haut) :
- Fibre supérieure : y = +h/2 → compression du béton
- Fibre inférieure : y = -h/2 → traction de l'acier

Déformation :
ε(y) = ε₀ + χ ⋅ y

Si ε₀ = 0 et χ > 0 :
- Fibre supérieure (y > 0) : ε > 0 → béton en compression ✓
- Fibre inférieure (y < 0) : ε < 0 → acier en traction ✓
```

## Règles d'Implémentation

1. **Calcul de déformation** : Utiliser la même formule pour béton et acier
2. **Application de la loi** : Chaque matériau interprète le signe selon sa convention
3. **Forces internes** : Additionner directement les contributions (signes cohérents)

## Validation

Les conventions sont validées par :
- Tests unitaires sur chaque matériau
- Tests d'intégration avec sections mixtes
- Cas analytiques de référence

## Références

- Eurocode 2 (EN 1992-1-1)
- Pratique courante en génie civil français
- Standards de la mécanique des solides pour l'acier
