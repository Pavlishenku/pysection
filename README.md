# opensection

Python library for structural concrete section analysis according to Eurocode 2.

[![PyPI](https://img.shields.io/pypi/v/opensection.svg)](https://pypi.org/project/opensection/)
[![Python](https://img.shields.io/pypi/pyversions/opensection.svg)](https://pypi.org/project/opensection/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Installation

```bash
pip install opensection
```

## Quick Start

```python
import opensection as ops

# Define section and materials
section = ops.RectangularSection(width=0.3, height=0.5)
concrete = ops.ConcreteEC2(fck=30)  # C30/37
steel = ops.SteelEC2(fyk=500)       # B500B

# Add reinforcement
rebars = ops.RebarGroup()
rebars.add_rebar(y=0.0, z=-0.20, diameter=0.020, n=3)
rebars.add_rebar(y=0.0, z=0.20, diameter=0.016, n=2)

# Solve
solver = ops.SectionSolver(section, concrete, steel, rebars)
result = solver.solve(N=500, My=0, Mz=100)

print(f"Converged: {result.converged}")
print(f"σc,max = {result.sigma_c_max:.2f} MPa")
print(f"σs,max = {result.sigma_s_max:.2f} MPa")
```

## Features

- Eurocode 2 compliant analysis
- Fiber-based section solver
- Rectangular, circular, T-sections, and custom geometries
- N-M interaction diagrams
- Material models: concrete (EC2), steel (EC2, EC3)
- Visualization tools

## Documentation

- [User Guide](https://opensection.readthedocs.io)
- [API Reference](https://opensection.readthedocs.io/en/latest/api/)
- [Examples](examples/)

## License

MIT License - see [LICENSE](LICENSE) file.
