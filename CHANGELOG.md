# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-24

### 🎉 First Stable Release

This is the first stable release of SectionPy, a professional concrete section analysis library.

### ✨ Added

#### Core Features
- **Fiber-based section analysis** using Newton-Raphson solver
- **Geometry module** for section definitions:
  - Rectangular sections
  - Circular sections
  - T-sections
  - Custom polygonal sections via contour definition
- **Material models** compliant with Eurocodes:
  - Concrete (EN 1992 - Eurocode 2)
  - Reinforcing steel (EN 1992 - Eurocode 2)
  - Prestressing steel (EN 1992 - Eurocode 2)
  - Structural steel (EN 1993 - Eurocode 3)
- **Reinforcement management**:
  - Individual rebar placement
  - Rebar groups
  - Helper functions for common patterns (linear arrays, circular patterns)
  - Automatic cover calculation

#### Analysis Capabilities
- **Section solver** for general loading:
  - Axial force (N)
  - Bending moments (My, Mz)
  - Biaxial bending
  - Strain and stress distributions
- **Interaction diagrams** (N-M):
  - Automatic generation
  - Support for any section type
  - Customizable parameters
- **Eurocode 2 verification**:
  - ULS (Ultimate Limit State) checks
  - Stress verifications
  - Strain limits

#### Visualization & Reporting
- **Section plotting**:
  - Geometry visualization
  - Reinforcement display
  - Stress/strain contours
- **Report generation**:
  - Automated design reports
  - Results summary
  - Verification checks

#### Documentation
- **Comprehensive user guide**
- **API reference** with all modules documented
- **Theory manual** explaining the fiber method
- **15+ example scripts** covering:
  - Basic section analysis
  - Column design
  - Beam design
  - T-beam design
  - Biaxial bending
  - Circular sections
  - Custom geometries
  - Prestressed sections
  - Interaction diagrams
  - Material law visualization
  - Academic validation cases

#### Quality & Testing
- **95%+ test coverage**
- **Type hints** throughout the codebase
- **Validation against analytical solutions**
- **Performance benchmarks**
- **CI/CD pipeline** with GitHub Actions

#### Developer Tools
- **Modern Python packaging** (pyproject.toml)
- **Development dependencies** included
- **Code quality tools** (black, flake8, mypy, isort)
- **Pre-commit hooks** configuration
- **Contributing guidelines**
- **Code of conduct**

### 📝 Package Information
- **License**: MIT
- **Python Support**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Main Dependencies**: NumPy >= 1.20.0, Matplotlib >= 3.3.0

### 🔧 Breaking Changes
- Package renamed from `opencds` to `sectionpy`
- All imports now use `import sectionpy as sp` instead of `import opencds as oc`

### 🙏 Acknowledgments
This release represents a complete, production-ready library for structural concrete section analysis based on Eurocode 2 specifications.

[1.0.0]: https://github.com/yourusername/sectionpy/releases/tag/v1.0.0
