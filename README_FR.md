# SectionPy - Analyse Professionnelle de Sections Béton

<div align="center">

**Une bibliothèque Python pour l'analyse de sections en béton selon les Eurocodes**

[![Version PyPI](https://img.shields.io/pypi/v/sectionpy.svg)](https://pypi.org/project/sectionpy/)
[![Versions Python](https://img.shields.io/pypi/pyversions/sectionpy.svg)](https://pypi.org/project/sectionpy/)
[![Licence: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/Pavlishenku/sectionpy/workflows/CI/badge.svg)](https://github.com/Pavlishenku/sectionpy/actions)

[English](README.md) | **Français**

</div>

---

## ✨ Fonctionnalités

- **Conforme aux Eurocodes**: Support complet de l'EN 1992 (Eurocode 2)
- **Analyse par fibres**: Analyse avancée de sections par discrétisation en fibres
- **Modèles de matériaux**: Lois constitutives complètes pour béton et acier
- **Diagrammes d'interaction**: Génération de diagrammes N-M pour les sections
- **Géométrie flexible**: Support des sections rectangulaires, circulaires, en T et polygonales
- **Visualisation**: Outils intégrés pour tracer sections et résultats
- **Rapide**: Calculs optimisés avec NumPy
- **Extensible**: API propre pour utilisateurs avancés et chercheurs

## 📦 Installation

### Depuis PyPI (recommandé)

```bash
pip install sectionpy
```

### Depuis les sources

```bash
git clone https://github.com/Pavlishenku/sectionpy.git
cd sectionpy
pip install -e .
```

### Installation développement

```bash
git clone https://github.com/Pavlishenku/sectionpy.git
cd sectionpy
pip install -e ".[dev]"
```

## 🚀 Démarrage Rapide

```python
import sectionpy as sp

# Définir une section béton rectangulaire
section = sp.RectangularSection(width=0.3, height=0.5)

# Définir les matériaux (Eurocode 2)
concrete = sp.ConcreteEC2(fck=30)  # C30/37
steel = sp.SteelEC2(fyk=500)       # B500B

# Ajouter les armatures
rebars = sp.RebarGroup()
rebars.add_rebar(y=0.0, z=-0.20, diameter=0.020, n=3)  # 3Ø20 en bas
rebars.add_rebar(y=0.0, z=0.20, diameter=0.016, n=2)   # 2Ø16 en haut

# Créer le solveur et analyser
solver = sp.SectionSolver(section, concrete, steel, rebars)
result = solver.solve(N=500, My=0, Mz=100)  # N en kN, M en kN·m

# Vérifier les résultats
print(f"Convergence: {result.converged}")
print(f"Contrainte béton max: {result.sigma_c_max:.2f} MPa")
print(f"Contrainte acier max: {result.sigma_s_max:.2f} MPa")

# Vérifier selon EC2
checks = sp.EC2Verification.check_ULS(result, concrete.fcd, steel.fyd)
print(f"Vérif. béton: {'OK' if checks['concrete_stress']['ok'] else 'ÉCHEC'}")
print(f"Vérif. acier: {'OK' if checks['steel_stress']['ok'] else 'ÉCHEC'}")
```

## 📚 Documentation

Documentation complète disponible sur [sectionpy.readthedocs.io](https://sectionpy.readthedocs.io)

- [Guide Utilisateur](https://sectionpy.readthedocs.io/fr/latest/user_guide/index.html)
- [Référence API](https://sectionpy.readthedocs.io/fr/latest/api/index.html)
- [Exemples](https://sectionpy.readthedocs.io/fr/latest/examples/index.html)
- [Théorie](https://sectionpy.readthedocs.io/fr/latest/theory/index.html)

## 💡 Exemples

Consultez le répertoire [examples](examples/) pour plus de cas d'usage détaillés :

- [Analyse de section basique](examples/example_basic.py)
- [Diagrammes d'interaction](examples/example_interaction_diagram.py)
- [Sections personnalisées](examples/example_custom_sections.py)
- [Flexion biaxiale](examples/example_biaxial_bending.py)
- [Colonnes circulaires](examples/example_circular_column.py)
- [Conception de poutres en T](examples/example_t_beam_design.py)

## 🛠️ Développement

### Configuration environnement de développement

```bash
# Cloner le dépôt
git clone https://github.com/Pavlishenku/sectionpy.git
cd sectionpy

# Créer environnement virtuel
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Installer dépendances de développement
pip install -e ".[dev]"
```

### Lancer les tests

```bash
# Lancer tous les tests
pytest

# Avec coverage
pytest --cov=sectionpy --cov-report=html

# Test spécifique
pytest tests/test_geometry.py
```

### Qualité du code

```bash
# Formater le code
black src/ tests/

# Trier les imports
isort src/ tests/

# Linting
flake8 src/ tests/

# Vérification de types
mypy src/
```

## 🤝 Contribuer

Les contributions sont les bienvenues ! Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour :

- Code de conduite
- Processus de développement
- Soumettre des pull requests
- Standards de code
- Exigences de tests

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour les détails.

## 🙏 Remerciements

- Inspiré par le besoin d'outils de conception structurelle open-source
- Basé sur les spécifications Eurocode 2 (EN 1992-1-1)
- Construit avec NumPy et Matplotlib

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/Pavlishenku/sectionpy/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Pavlishenku/sectionpy/discussions)

## 🗺️ Feuille de Route

- [x] Analyse de section basique (EC2)
- [x] Diagrammes d'interaction
- [ ] Support ACI 318 (code US)
- [ ] Support GB 50010 (code chinois)
- [ ] Effets différés (fluage, retrait)
- [ ] Calcul d'ouverture de fissures
- [ ] Analyse de flèche
- [ ] Interface web
- [ ] Intégration CAO (import/export DXF)

## 📖 Citation

Si vous utilisez SectionPy dans un travail académique, veuillez citer :

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

**Fait avec ❤️ par la communauté SectionPy**

[⭐ Star sur GitHub](https://github.com/Pavlishenku/sectionpy) | [📖 Documentation](https://sectionpy.readthedocs.io) | [💬 Discussions](https://github.com/Pavlishenku/sectionpy/discussions)

</div>
