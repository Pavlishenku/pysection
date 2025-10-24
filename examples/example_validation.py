"""
Exemple d'utilisation du module de validation SectionPy
"""

from sectionpy import RectangularSection, ConcreteEC2, SteelEC2, RebarGroup
from sectionpy.validation import (
    SectionValidator,
    GeometryValidator,
    MaterialValidator,
    RebarValidator,
    ValidationError,
)


def example_validation_complete():
    """Exemple de validation complète d'une section"""
    print("=" * 70)
    print("EXEMPLE 1 : Validation complète d'une section")
    print("=" * 70)
    
    # Créer une section valide
    section = RectangularSection(width=0.3, height=0.5)
    concrete = ConcreteEC2(fck=30)
    steel = SteelEC2(fyk=500)
    rebars = RebarGroup()
    rebars.add_rebar(y=0.20, z=0.0, diameter=0.016, n=3)
    rebars.add_rebar(y=-0.20, z=0.0, diameter=0.016, n=3)
    
    try:
        SectionValidator.validate_all(
            section, concrete, steel, rebars,
            N=500, M_y=0, M_z=100
        )
        print("[OK] Section validee avec succes !")
        print(f"  - Largeur : {section.width*100:.1f} cm")
        print(f"  - Hauteur : {section.height*100:.1f} cm")
        print(f"  - Béton : C{int(concrete.fck)}/37")
        print(f"  - Acier : B{int(steel.fyk)}")
        print(f"  - Armatures : {rebars.n_rebars} barres")
        print(f"  - Charges : N={500} kN, M={100} kN·m")
    except ValidationError as e:
        print(f"[ERREUR] Erreur de validation : {e}")
    
    print()


def example_dimension_error():
    """Exemple d'erreur de dimension"""
    print("=" * 70)
    print("EXEMPLE 2 : Détection d'une dimension négative")
    print("=" * 70)
    
    try:
        # Tentative de créer une section avec largeur négative
        GeometryValidator.validate_dimension(-0.3, "largeur")
        print("[OK] Dimension validée")
    except ValidationError as e:
        print(f"[ERREUR] Erreur détectée : {e}")
    
    print()


def example_rebar_outside():
    """Exemple d'armature hors section"""
    print("=" * 70)
    print("EXEMPLE 3 : Détection d'armature hors section")
    print("=" * 70)
    
    section = RectangularSection(width=0.3, height=0.5)
    concrete = ConcreteEC2(fck=30)
    steel = SteelEC2(fyk=500)
    rebars = RebarGroup()
    
    # Armature hors de la section
    rebars.add_rebar(y=0.30, z=0.0, diameter=0.016, n=3)  # y = 30 cm > hauteur/2 = 25 cm
    
    try:
        SectionValidator.validate_all(section, concrete, steel, rebars)
        print("[OK] Section validée")
    except ValidationError as e:
        print(f"[ERREUR] Erreur détectée : {e}")
        print("  Conseil : Vérifiez la position des armatures")
    
    print()


def example_weak_concrete():
    """Exemple de béton trop faible"""
    print("=" * 70)
    print("EXEMPLE 4 : Détection de béton hors normes EC2")
    print("=" * 70)
    
    try:
        # Tentative d'utiliser C10 (< C12/15 minimum EC2)
        MaterialValidator.validate_concrete_strength(10)
        print("[OK] Résistance béton validée")
    except ValidationError as e:
        print(f"[ERREUR] Erreur détectée : {e}")
        print("  Conseil : Utilisez au minimum C12/15")
    
    print()


def example_unrealistic_load():
    """Exemple de charge aberrante"""
    print("=" * 70)
    print("EXEMPLE 5 : Détection de charge aberrante")
    print("=" * 70)
    
    section = RectangularSection(width=0.3, height=0.5)
    concrete = ConcreteEC2(fck=30)
    steel = SteelEC2(fyk=500)
    rebars = RebarGroup()
    rebars.add_rebar(y=0.20, z=0.0, diameter=0.016, n=3)
    
    try:
        # Charge irréaliste (probablement erreur d'unités)
        SectionValidator.validate_all(
            section, concrete, steel, rebars,
            N=500000,  # 500 MN au lieu de 500 kN ?
            M_z=100
        )
        print("[OK] Charges validées")
    except ValidationError as e:
        print(f"[ERREUR] Erreur détectée : {e}")
        print("  Conseil : Vérifiez les unités (kN attendus)")
    
    print()


def example_progressive_validation():
    """Exemple de validation progressive"""
    print("=" * 70)
    print("EXEMPLE 6 : Validation progressive lors de la saisie")
    print("=" * 70)
    
    print("Création d'une section étape par étape avec validation...")
    
    # Étape 1 : Dimensions
    print("\n1. Validation des dimensions...")
    try:
        width = 0.3
        height = 0.5
        GeometryValidator.validate_dimension(width, "largeur")
        GeometryValidator.validate_dimension(height, "hauteur")
        print(f"   [OK] Dimensions OK : {width*100:.0f} x {height*100:.0f} cm")
    except ValidationError as e:
        print(f"   ✗ {e}")
        return
    
    # Étape 2 : Matériaux
    print("\n2. Validation des matériaux...")
    try:
        fck = 30
        fyk = 500
        MaterialValidator.validate_concrete_strength(fck)
        MaterialValidator.validate_steel_strength(fyk)
        print(f"   [OK] Matériaux OK : C{fck}/37, B{fyk}")
    except ValidationError as e:
        print(f"   ✗ {e}")
        return
    
    # Étape 3 : Armatures
    print("\n3. Validation des armatures...")
    try:
        diameter = 0.016
        y, z = 0.20, 0.0
        RebarValidator.validate_diameter(diameter)
        RebarValidator.validate_rebar_position(y, z, diameter, width, height)
        print(f"   [OK] Armatures OK : HA{int(diameter*1000)} à y={y*100:.0f} cm")
    except ValidationError as e:
        print(f"   ✗ {e}")
        return
    
    print("\n[OK] Toutes les validations passées !")
    print()


def example_warnings():
    """Exemple d'avertissements (non bloquants)"""
    print("=" * 70)
    print("EXEMPLE 7 : Avertissements (valeurs inhabituelles)")
    print("=" * 70)
    
    import warnings
    
    print("Validation d'une résistance béton non-standard...")
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        MaterialValidator.validate_concrete_strength(33)  # C33 non-standard
        if w:
            print(f"[WARNING] Avertissement : {w[0].message}")
            print("   (La validation continue quand même)")
    
    print()


def main():
    """Exécuter tous les exemples"""
    print("\n")
    print("*" * 70)
    print("  EXEMPLES DE VALIDATION SectionPy")
    print("*" * 70)
    print()
    
    example_validation_complete()
    example_dimension_error()
    example_rebar_outside()
    example_weak_concrete()
    example_unrealistic_load()
    example_progressive_validation()
    example_warnings()
    
    print("=" * 70)
    print("RÉSUMÉ")
    print("=" * 70)
    print("Le module de validation SectionPy détecte :")
    print("  - Dimensions negatives ou aberrantes")
    print("  [OK] Armatures hors de la section")
    print("  [OK] Résistances matériaux hors normes EC2")
    print("  [OK] Charges irréalistes")
    print("  [OK] Erreurs d'unités probables")
    print("  [OK] Enrobages insuffisants")
    print("  [OK] Taux d'armature min/max")
    print()
    print("Utilisez SectionValidator.validate_all() pour une validation complète")
    print("avant de lancer vos calculs !")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()

