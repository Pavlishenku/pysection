# SectionPy - Professional Concrete Section Analysis

<div align="center">

**A Python library for structural concrete section analysis according to Eurocodes**

[![PyPI version](https://img.shields.io/pypi/v/sectionpy.svg)](https://pypi.org/project/sectionpy/)
[![Python versions](https://img.shields.io/pypi/pyversions/sectionpy.svg)](https://pypi.org/project/sectionpy/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/Pavlishenku/sectionpy/workflows/CI/badge.svg)](https://github.com/Pavlishenku/sectionpy/actions)
[![codecov](https://codecov.io/gh/Pavlishenku/sectionpy/branch/main/graph/badge.svg)](https://codecov.io/gh/Pavlishenku/sectionpy)
[![Documentation Status](https://readthedocs.org/projects/sectionpy/badge/?version=latest)](https://sectionpy.readthedocs.io/en/latest/?badge=latest)

[English](README.md) | [Français](README_FR.md)

</div>

---

## ✨ Features

- **Eurocode-compliant**: Full support for EN 1992 (Eurocode 2) for concrete structures
- **Fiber-based analysis**: Advanced section analysis using fiber discretization
- **Material models**: Comprehensive constitutive laws for concrete and reinforcing steel
- **Interaction diagrams**: Generate N-M interaction diagrams for sections
- **Flexible geometry**: Support for rectangular, circular, T-sections, and custom polygons
- **Visualization**: Built-in tools for plotting sections and results
- **Fast**: Optimized NumPy-based computations
- **Extensible**: Clean API for advanced users and researchers

## 📦 Installation

### From PyPI (recommended)

```bash
pip install sectionpy
```

### From source

```bash
git clone https://github.com/Pavlishenku/sectionpy.git
cd sectionpy
pip install -e .
```

### Development installation

```bash
git clone https://github.com/Pavlishenku/sectionpy.git
cd sectionpy
pip install -e ".[dev]"
```

## 🚀 Quick Start

```python
import sectionpy as sp

# Define a rectangular concrete section
section = sp.RectangularSection(width=0.3, height=0.5)

# Define materials (Eurocode 2)
concrete = sp.ConcreteEC2(fck=30)  # C30/37
steel = sp.SteelEC2(fyk=500)       # B500B

# Add reinforcement
rebars = sp.RebarGroup()
rebars.add_rebar(y=0.0, z=-0.20, diameter=0.020, n=3)  # 3Ø20 bottom
rebars.add_rebar(y=0.0, z=0.20, diameter=0.016, n=2)   # 2Ø16 top

# Create solver and analyze
solver = sp.SectionSolver(section, concrete, steel, rebars)
result = solver.solve(N=500, My=0, Mz=100)  # N in kN, M in kN·m

# Check results
print(f"Converged: {result.converged}")
print(f"Max concrete stress: {result.sigma_c_max:.2f} MPa")
print(f"Max steel stress: {result.sigma_s_max:.2f} MPa")

# Verify according to EC2
checks = sp.EC2Verification.check_ULS(result, concrete.fcd, steel.fyd)
print(f"Concrete check: {'OK' if checks['concrete_stress']['ok'] else 'FAIL'}")
print(f"Steel check: {'OK' if checks['steel_stress']['ok'] else 'FAIL'}")
```

## 📚 Documentation

Full documentation is available at [sectionpy.readthedocs.io](https://sectionpy.readthedocs.io)

- [User Guide](https://sectionpy.readthedocs.io/en/latest/user_guide/index.html)
- [API Reference](https://sectionpy.readthedocs.io/en/latest/api/index.html)
- [Examples](https://sectionpy.readthedocs.io/en/latest/examples/index.html)
- [Theory](https://sectionpy.readthedocs.io/en/latest/theory/index.html)

## 💡 Examples

Check out the [examples](examples/) directory for more detailed use cases:

- [Basic section analysis](examples/example_basic.py)
- [Interaction diagrams](examples/example_interaction_diagram.py)
- [Custom sections](examples/example_custom_sections.py)
- [Biaxial bending](examples/example_biaxial_bending.py)
- [Circular columns](examples/example_circular_column.py)
- [T-beam design](examples/example_t_beam_design.py)

## 🛠️ Development

### Setting up development environment

```bash
# Clone the repository
git clone https://github.com/Pavlishenku/sectionpy.git
cd sectionpy

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Running tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=sectionpy --cov-report=html

# Run specific test file
pytest tests/test_geometry.py
```

### Code quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint
flake8 src/ tests/

# Type checking
mypy src/
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on:

- Code of conduct
- Development process
- Submitting pull requests
- Coding standards
- Testing requirements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the need for open-source structural design tools
- Based on Eurocode 2 (EN 1992-1-1) specifications
- Built with NumPy and Matplotlib

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/Pavlishenku/sectionpy/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Pavlishenku/sectionpy/discussions)

## 🗺️ Roadmap

- [x] Basic section analysis (EC2)
- [x] Interaction diagrams
- [ ] Support for ACI 318 (US code)
- [ ] Support for GB 50010 (Chinese code)
- [ ] Time-dependent effects (creep, shrinkage)
- [ ] Crack width calculations
- [ ] Deflection analysis
- [ ] Web interface
- [ ] CAD integration (DXF import/export)

## 📖 Citation

If you use SectionPy in academic work, please cite:

```bibtex
@software{sectionpy2025,
  author = {SectionPy Contributors},
  title = {SectionPy: Professional Concrete Section Analysis},
  year = {2025},
  url = {https://github.com/Pavlishenku/sectionpy},
  version = {1.0.0}
}
```

---

<div align="center">

**Made with ❤️ by the SectionPy community**

[⭐ Star us on GitHub](https://github.com/Pavlishenku/sectionpy) | [📖 Read the docs](https://sectionpy.readthedocs.io) | [💬 Join the discussion](https://github.com/Pavlishenku/sectionpy/discussions)

</div>
