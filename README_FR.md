# opensection - Analyse Professionnelle de Sections Béton

<div align="center">

**Une bibliothèque Python pour l'analyse de sections en béton selon les Eurocodes**

[![Version PyPI](https://img.shields.io/pypi/v/opensection.svg)](https://pypi.org/project/opensection/)
[![Versions Python](https://img.shields.io/pypi/pyversions/opensection.svg)](https://pypi.org/project/opensection/)
[![Licence: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/Pavlishenku/opensection/workflows/CI/badge.svg)](https://github.com/Pavlishenku/opensection/actions)

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
pip install opensection
```

### Depuis les sources

```bash
git clone https://github.com/Pavlishenku/opensection.git
cd opensection
pip install -e .
```

### Installation développement

```bash
git clone https://github.com/Pavlishenku/opensection.git
cd opensection
pip install -e ".[dev]"
```

## 🚀 Démarrage Rapide

```python
import opensection as ops

# Définir une section béton rectangulaire
section = ops.RectangularSection(width=0.3, height=0.5)

# Définir les matériaux (Eurocode 2)
concrete = ops.ConcreteEC2(fck=30)  # C30/37
steel = ops.SteelEC2(fyk=500)       # B500B

# Ajouter les armatures
rebars = ops.RebarGroup()
rebars.add_rebar(y=0.0, z=-0.20, diameter=0.020, n=3)  # 3Ø20 en bas
rebars.add_rebar(y=0.0, z=0.20, diameter=0.016, n=2)   # 2Ø16 en haut

# Créer le solveur et analyser
solver = ops.SectionSolver(section, concrete, steel, rebars)
result = solver.solve(N=500, My=0, Mz=100)  # N en kN, M en kN·m

# Vérifier les résultats
print(f"Convergence: {result.converged}")
print(f"Contrainte béton max: {result.sigma_c_max:.2f} MPa")
print(f"Contrainte acier max: {result.sigma_s_max:.2f} MPa")

# Vérifier selon EC2
checks = ops.EC2Verification.check_ULS(result, concrete.fcd, steel.fyd)
print(f"Vérif. béton: {'OK' if checks['concrete_stress']['ok'] else 'ÉCHEC'}")
print(f"Vérif. acier: {'OK' if checks['steel_stress']['ok'] else 'ÉCHEC'}")
```

## 📚 Documentation

Documentation complète disponible sur [opensection.readthedocs.io](https://opensection.readthedocs.io)

- [Guide Utilisateur](https://opensection.readthedocs.io/fr/latest/user_guide/index.html)
- [Référence API](https://opensection.readthedocs.io/fr/latest/api/index.html)
- [Exemples](https://opensection.readthedocs.io/fr/latest/examples/index.html)
- [Théorie](https://opensection.readthedocs.io/fr/latest/theory/index.html)

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
git clone https://github.com/Pavlishenku/opensection.git
cd opensection

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
pytest --cov=opensection --cov-report=html

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

- **Issues**: [GitHub Issues](https://github.com/Pavlishenku/opensection/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Pavlishenku/opensection/discussions)

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

Si vous utilisez opensection dans un travail académique, veuillez citer :

```bibtex
@software{opensection2025,
  author = {opensection Contributors},
  title = {opensection: Professional Concrete Section Analysis},
  year = {2025},
  url = {https://github.com/Pavlishenku/opensection},
  version = {1.0.0}
}
```

---

<div align="center">

**Fait avec ❤️ par la communauté opensection**

[⭐ Star sur GitHub](https://github.com/Pavlishenku/opensection) | [📖 Documentation](https://opensection.readthedocs.io) | [💬 Discussions](https://github.com/Pavlishenku/opensection/discussions)

</div>
