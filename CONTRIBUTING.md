# Contributing to opensection

First off, thank you for considering contributing to opensection! It's people like you that make opensection such a great tool for the structural engineering community.

## [LIST] Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

##  Code of Conduct

This project and everyone participating in it is governed by the [opensection Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## [>] Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic knowledge of structural engineering and Eurocodes

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/opensection.git
   cd opensection
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

5. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

6. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## [THINK] How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**When reporting a bug, please include**:
- opensection version
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Minimal code example
- Error messages and stack traces

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md).

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.

**When suggesting an enhancement, please include**:
- Clear description of the feature
- Rationale and use cases
- Examples of how it would work
- Potential implementation approach

Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md).

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `documentation` - Documentation improvements

### Pull Requests

1. Follow the [development process](#development-process)
2. Follow the [coding standards](#coding-standards)
3. Add or update tests as needed
4. Update documentation as needed
5. Ensure all tests pass
6. Fill in the pull request template

## [CONFIG] Development Process

### 1. Make Your Changes

- Write clear, documented code
- Follow existing code style
- Add docstrings to new functions/classes
- Keep commits atomic and well-described

### 2. Test Your Changes

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=opensection --cov-report=html

# Run specific test file
pytest tests/test_geometry.py

# Run specific test
pytest tests/test_geometry.py::test_rectangular_section
```

### 3. Lint Your Code

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Run linters
flake8 src/ tests/
mypy src/
```

### 4. Update Documentation

If you've changed the API or added features:
- Update docstrings
- Update user guide if needed
- Add examples if applicable

### 5. Commit Your Changes

```bash
git add .
git commit -m "feat: add support for circular hollow sections"
```

**Commit message format**:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code refactoring
- `style:` Formatting changes
- `chore:` Maintenance tasks

##  Coding Standards

### Python Style

We follow [PEP 8](https://pep8.org/) with some modifications:
- Line length: 100 characters
- Use Black for formatting
- Use isort for import ordering

### Docstrings

Use Google-style docstrings:

```python
def calculate_moment(force: float, distance: float) -> float:
    """
    Calculate bending moment from force and distance.
    
    Args:
        force: Applied force in kN
        distance: Distance from point in m
    
    Returns:
        Bending moment in kN·m
    
    Raises:
        ValueError: If force or distance is negative
    
    Examples:
        >>> calculate_moment(100, 2.5)
        250.0
    """
    if force < 0 or distance < 0:
        raise ValueError("Force and distance must be positive")
    return force * distance
```

### Type Hints

Always use type hints:

```python
from typing import List, Tuple, Optional

def process_rebars(
    rebars: List[Rebar],
    diameter: float
) -> Tuple[float, int]:
    """Process reinforcement bars."""
    # Implementation
    return total_area, count
```

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `SectionSolver`)
- **Functions/methods**: `snake_case` (e.g., `compute_properties`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_ITERATIONS`)
- **Private**: prefix with `_` (e.g., `_internal_method`)

## [TEST] Testing

### Writing Tests

- Use pytest
- Aim for >80% code coverage
- Test edge cases and error conditions
- Use descriptive test names

```python
import pytest
import numpy as np
from opensection import RectangularSection

def test_rectangular_section_area():
    """Test area calculation for rectangular section."""
    section = RectangularSection(width=0.3, height=0.5)
    expected_area = 0.15
    assert np.isclose(section.properties.area, expected_area)

def test_rectangular_section_invalid_dimensions():
    """Test that negative dimensions raise ValueError."""
    with pytest.raises(ValueError):
        RectangularSection(width=-0.3, height=0.5)
```

### Test Organization

```
tests/
 test_geometry.py       # Geometry module tests
 test_materials.py      # Material models tests
 test_solver.py         # Solver tests
 test_integration.py    # Integration tests
 fixtures/              # Test data and fixtures
```

## [DOCS] Documentation

### Building Documentation

```bash
cd docs
make html
```

View at `docs/_build/html/index.html`.

### Documentation Structure

- **Tutorials**: Step-by-step guides for beginners
- **How-to guides**: Recipes for specific tasks
- **Reference**: API documentation (auto-generated)
- **Explanation**: Background theory and concepts

##  Submitting Changes

### Before Submitting

- [ ] Tests pass locally
- [ ] Code is formatted (black, isort)
- [ ] Linters pass (flake8, mypy)
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (for significant changes)
- [ ] Commit messages follow conventions

### Pull Request Process

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create pull request** on GitHub

3. **Fill in the PR template** with:
   - Description of changes
   - Related issues
   - Type of change
   - Testing performed
   - Screenshots (if UI changes)

4. **Wait for review**:
   - Address review comments
   - Push additional commits if needed
   - Be patient and respectful

5. **After approval**:
   - Squash commits if requested
   - Maintainer will merge

### Review Criteria

Pull requests are reviewed for:
- Correctness and completeness
- Code quality and style
- Test coverage
- Documentation
- Performance implications
- API consistency

## [WORLD] Translation Contributions

We welcome translations! See [Translation Guide](docs/TRANSLATION.md) for:
- How to add new language
- Translation workflow
- Using sphinx-intl
- Translation guidelines

Priority languages:
- English (base)
- French
- Japanese
- Chinese (Simplified)

## [IDEA] Questions?

- **General questions**: [GitHub Discussions](https://github.com/opensection/opensection/discussions)
- **Bug reports**: [GitHub Issues](https://github.com/opensection/opensection/issues)
- **Email**: pavlishenku@gmail.com

## [AWARD] Recognition

Contributors are recognized in:
- [AUTHORS.md](AUTHORS.md)
- GitHub contributors page
- Release notes
- Annual summary posts

Thank you for contributing to opensection! [SUCCESS]

