# opensection

Analyse de sections en beton selon les Eurocodes.

## Fonctionnalites

- Conforme aux Eurocodes (EN 1992)
- Analyse par fibres
- Modeles de materiaux pour beton et acier
- Diagrammes d'interaction N-M
- Sections rectangulaires, circulaires, en T et polygonales
- Visualisation
- Calculs optimises avec NumPy

## Installation

```bash
pip install opensection
```

## Usage

```python
import opensection as ops

section = ops.RectangularSection(width=0.3, height=0.5)
concrete = ops.ConcreteEC2(fck=30)
steel = ops.SteelEC2(fyk=500)

rebars = ops.RebarGroup()
rebars.add_rebar(y=0.0, z=-0.20, diameter=0.020, n=3)
rebars.add_rebar(y=0.0, z=0.20, diameter=0.016, n=2)

solver = ops.SectionSolver(section, concrete, steel, rebars)
result = solver.solve(N=500, My=0, Mz=100)
```

## Licence

MIT
