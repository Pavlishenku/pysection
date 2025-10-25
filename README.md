# opensection

Structural concrete section analysis according to Eurocode 2.

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

## License

MIT
