"""
W-Section Database
AISC steel section properties for common W-shapes
"""

from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class WSectionProperties:
    """W-section properties"""
    name: str
    A: float      # Area (in²)
    d: float      # Depth (in)
    tw: float     # Web thickness (in)
    bf: float     # Flange width (in)
    tf: float     # Flange thickness (in)
    Ix: float     # Moment of inertia about x-axis (in⁴)
    Iy: float     # Moment of inertia about y-axis (in⁴)
    Zx: float     # Plastic section modulus about x-axis (in³)
    Sx: float     # Elastic section modulus about x-axis (in³)
    rx: float     # Radius of gyration about x-axis (in)
    ry: float     # Radius of gyration about y-axis (in)
    J: float      # Torsional constant (in⁴)
    Cw: float     # Warping constant (in⁶)
    weight: float # Weight per foot (lb/ft)


# W-Section Database (Common sections from AISC Manual)
WSECTION_DATABASE: Dict[str, WSectionProperties] = {
    # W14 Sections
    "W14X22": WSectionProperties(
        name="W14X22", A=6.49, d=13.74, tw=0.230, bf=5.00, tf=0.335,
        Ix=199, Iy=7.00, Zx=33.2, Sx=29.0, rx=5.54, ry=1.04, J=0.299, Cw=385, weight=22
    ),
    "W14X26": WSectionProperties(
        name="W14X26", A=7.69, d=13.91, tw=0.255, bf=5.03, tf=0.420,
        Ix=245, Iy=8.91, Zx=40.2, Sx=35.3, rx=5.65, ry=1.08, J=0.508, Cw=513, weight=26
    ),
    "W14X30": WSectionProperties(
        name="W14X30", A=8.85, d=13.84, tw=0.270, bf=6.73, tf=0.385,
        Ix=291, Iy=19.6, Zx=47.3, Sx=42.0, rx=5.73, ry=1.49, J=0.455, Cw=1030, weight=30
    ),
    "W14X43": WSectionProperties(
        name="W14X43", A=12.6, d=13.66, tw=0.305, bf=7.995, tf=0.530,
        Ix=428, Iy=45.2, Zx=69.6, Sx=62.7, rx=5.82, ry=1.89, J=1.05, Cw=2560, weight=43
    ),
    "W14X53": WSectionProperties(
        name="W14X53", A=15.6, d=13.92, tw=0.370, bf=8.06, tf=0.660,
        Ix=541, Iy=57.7, Zx=87.1, Sx=77.8, rx=5.89, ry=1.92, J=1.58, Cw=3250, weight=53
    ),
    "W14X68": WSectionProperties(
        name="W14X68", A=20.0, d=14.04, tw=0.415, bf=10.04, tf=0.720,
        Ix=723, Iy=121, Zx=115, Sx=103, rx=6.01, ry=2.46, J=2.46, Cw=7190, weight=68
    ),
    "W14X90": WSectionProperties(
        name="W14X90", A=26.5, d=14.02, tw=0.440, bf=14.52, tf=0.710,
        Ix=999, Iy=362, Zx=157, Sx=143, rx=6.14, ry=3.70, J=3.76, Cw=26700, weight=90
    ),
    "W14X120": WSectionProperties(
        name="W14X120", A=35.3, d=14.48, tw=0.590, bf=14.67, tf=0.940,
        Ix=1380, Iy=495, Zx=212, Sx=190, rx=6.24, ry=3.74, J=6.24, Cw=36400, weight=120
    ),
    "W14X176": WSectionProperties(
        name="W14X176", A=51.7, d=15.22, tw=0.830, bf=15.65, tf=1.31,
        Ix=2140, Iy=838, Zx=320, Sx=281, rx=6.43, ry=4.02, J=14.5, Cw=62600, weight=176
    ),
    "W14X211": WSectionProperties(
        name="W14X211", A=62.1, d=15.72, tw=1.00, bf=15.80, tf=1.56,
        Ix=2660, Iy=1030, Zx=390, Sx=338, rx=6.55, ry=4.07, J=21.5, Cw=78800, weight=211
    ),
    "W14X246": WSectionProperties(
        name="W14X246", A=72.3, d=16.26, tw=1.18, bf=15.98, tf=1.84,
        Ix=3230, Iy=1260, Zx=467, Sx=398, rx=6.68, ry=4.17, J=32.6, Cw=99300, weight=246
    ),
    "W14X287": WSectionProperties(
        name="W14X287", A=84.4, d=16.81, tw=1.38, bf=16.23, tf=2.13,
        Ix=3910, Iy=1530, Zx=559, Sx=464, rx=6.80, ry=4.26, J=47.4, Cw=124000, weight=287
    ),

    # W18 Sections
    "W18X35": WSectionProperties(
        name="W18X35", A=10.3, d=17.70, tw=0.300, bf=6.00, tf=0.425,
        Ix=510, Iy=15.3, Zx=66.5, Sx=57.6, rx=7.04, ry=1.22, J=0.510, Cw=1330, weight=35
    ),
    "W18X50": WSectionProperties(
        name="W18X50", A=14.7, d=17.99, tw=0.355, bf=7.495, tf=0.570,
        Ix=800, Iy=40.1, Zx=101, Sx=88.9, rx=7.38, ry=1.65, J=1.24, Cw=3630, weight=50
    ),
    "W18X71": WSectionProperties(
        name="W18X71", A=20.8, d=18.47, tw=0.495, bf=7.635, tf=0.810,
        Ix=1170, Iy=60.3, Zx=146, Sx=127, rx=7.50, ry=1.70, J=2.53, Cw=5370, weight=71
    ),

    # W21 Sections
    "W21X44": WSectionProperties(
        name="W21X44", A=13.0, d=20.66, tw=0.350, bf=6.50, tf=0.450,
        Ix=843, Iy=20.7, Zx=95.4, Sx=81.6, rx=8.06, ry=1.26, J=0.660, Cw=2020, weight=44
    ),
    "W21X50": WSectionProperties(
        name="W21X50", A=14.7, d=20.83, tw=0.380, bf=6.53, tf=0.535,
        Ix=984, Iy=24.9, Zx=110, Sx=94.5, rx=8.18, ry=1.30, J=0.932, Cw=2480, weight=50
    ),
    "W21X57": WSectionProperties(
        name="W21X57", A=16.7, d=21.06, tw=0.405, bf=6.555, tf=0.650,
        Ix=1170, Iy=30.6, Zx=129, Sx=111, rx=8.36, ry=1.35, J=1.42, Cw=3120, weight=57
    ),
    "W21X68": WSectionProperties(
        name="W21X68", A=20.0, d=21.13, tw=0.430, bf=8.270, tf=0.685,
        Ix=1480, Iy=64.7, Zx=160, Sx=140, rx=8.60, ry=1.80, J=1.88, Cw=7110, weight=68
    ),

    # W24 Sections
    "W24X55": WSectionProperties(
        name="W24X55", A=16.2, d=23.57, tw=0.395, bf=7.005, tf=0.505,
        Ix=1350, Iy=29.1, Zx=134, Sx=114, rx=9.11, ry=1.34, J=0.986, Cw=3340, weight=55
    ),
    "W24X68": WSectionProperties(
        name="W24X68", A=20.1, d=23.73, tw=0.415, bf=8.965, tf=0.585,
        Ix=1830, Iy=70.4, Zx=177, Sx=154, rx=9.55, ry=1.87, J=1.87, Cw=9430, weight=68
    ),
    "W24X84": WSectionProperties(
        name="W24X84", A=24.7, d=24.10, tw=0.470, bf=9.020, tf=0.770,
        Ix=2370, Iy=94.4, Zx=224, Sx=196, rx=9.79, ry=1.95, J=3.25, Cw=12400, weight=84
    ),
    "W24X110": WSectionProperties(
        name="W24X110", A=32.5, d=24.16, tw=0.510, bf=12.04, tf=0.855,
        Ix=3330, Iy=236, Zx=299, Sx=275, rx=10.1, ry=2.70, J=5.34, Cw=32500, weight=110
    ),
    "W24X130": WSectionProperties(
        name="W24X130", A=38.3, d=24.48, tw=0.565, bf=12.855, tf=0.960,
        Ix=4020, Iy=340, Zx=355, Sx=327, rx=10.2, ry=2.97, J=7.53, Cw=49000, weight=130
    ),
    "W24X160": WSectionProperties(
        name="W24X160", A=47.1, d=24.74, tw=0.650, bf=12.955, tf=1.135,
        Ix=5120, Iy=443, Zx=450, Sx=414, rx=10.4, ry=3.07, J=12.4, Cw=65900, weight=160
    ),

    # W27 Sections
    "W27X84": WSectionProperties(
        name="W27X84", A=24.8, d=26.71, tw=0.460, bf=9.960, tf=0.640,
        Ix=2850, Iy=106, Zx=244, Sx=213, rx=10.7, ry=2.07, J=2.81, Cw=16700, weight=84
    ),
    "W27X94": WSectionProperties(
        name="W27X94", A=27.7, d=26.92, tw=0.490, bf=9.990, tf=0.745,
        Ix=3270, Iy=124, Zx=278, Sx=243, rx=10.9, ry=2.12, J=3.86, Cw=19600, weight=94
    ),

    # W30 Sections
    "W30X90": WSectionProperties(
        name="W30X90", A=26.4, d=29.53, tw=0.470, bf=10.40, tf=0.610,
        Ix=3610, Iy=115, Zx=283, Sx=245, rx=11.7, ry=2.09, J=2.63, Cw=21700, weight=90
    ),
    "W30X99": WSectionProperties(
        name="W30X99", A=29.1, d=29.65, tw=0.520, bf=10.45, tf=0.670,
        Ix=3990, Iy=128, Zx=312, Sx=269, rx=11.7, ry=2.10, J=3.36, Cw=24000, weight=99
    ),
}


def get_section_properties(section_name: str) -> Optional[WSectionProperties]:
    """
    Get properties for a given W-section

    Args:
        section_name: Section name (e.g., "W14X90", "W14x90", "W 14 X 90")

    Returns:
        Section properties or None if not found
    """
    # Normalize section name
    normalized = section_name.upper().replace(" ", "").replace("x", "X")
    if not normalized.startswith("W"):
        normalized = "W" + normalized

    return WSECTION_DATABASE.get(normalized)


def search_sections_by_area(min_area: float, max_area: float = float('inf')) -> List[WSectionProperties]:
    """
    Search for sections within an area range

    Args:
        min_area: Minimum area (in²)
        max_area: Maximum area (in²)

    Returns:
        List of matching sections sorted by area
    """
    matching = [
        section for section in WSECTION_DATABASE.values()
        if min_area <= section.A <= max_area
    ]
    return sorted(matching, key=lambda s: s.A)


def search_sections_by_depth(depth: float, tolerance: float = 2.0) -> List[WSectionProperties]:
    """
    Search for sections near a target depth

    Args:
        depth: Target depth (in)
        tolerance: Allowed deviation (in)

    Returns:
        List of matching sections sorted by depth
    """
    matching = [
        section for section in WSECTION_DATABASE.values()
        if abs(section.d - depth) <= tolerance
    ]
    return sorted(matching, key=lambda s: s.d)


def recommend_section_for_column(
    required_area: float,
    required_Ix: Optional[float] = None,
    preferred_series: Optional[str] = None
) -> Optional[WSectionProperties]:
    """
    Recommend a W-section for a column

    Args:
        required_area: Required cross-sectional area (in²)
        required_Ix: Required moment of inertia (in⁴)
        preferred_series: Preferred W-series (e.g., "W14", "W18")

    Returns:
        Recommended section or None
    """
    candidates = [
        section for section in WSECTION_DATABASE.values()
        if section.A >= required_area
    ]

    if required_Ix is not None:
        candidates = [s for s in candidates if s.Ix >= required_Ix]

    if preferred_series:
        series = preferred_series.upper().replace(" ", "")
        candidates = [s for s in candidates if s.name.startswith(series)]

    if not candidates:
        return None

    # Return the lightest section that meets requirements
    return min(candidates, key=lambda s: s.weight)


def recommend_section_for_beam(
    required_Zx: float,
    max_depth: Optional[float] = None,
    preferred_series: Optional[str] = None
) -> Optional[WSectionProperties]:
    """
    Recommend a W-section for a beam

    Args:
        required_Zx: Required plastic section modulus (in³)
        max_depth: Maximum allowed depth (in)
        preferred_series: Preferred W-series (e.g., "W21", "W24")

    Returns:
        Recommended section or None
    """
    candidates = [
        section for section in WSECTION_DATABASE.values()
        if section.Zx >= required_Zx
    ]

    if max_depth is not None:
        candidates = [s for s in candidates if s.d <= max_depth]

    if preferred_series:
        series = preferred_series.upper().replace(" ", "")
        candidates = [s for s in candidates if s.name.startswith(series)]

    if not candidates:
        return None

    # Return the lightest section that meets requirements
    return min(candidates, key=lambda s: s.weight)


# Example usage
if __name__ == "__main__":
    print("W-Section Database Demo\n")

    # Test 1: Get specific section
    section = get_section_properties("W14X90")
    if section:
        print(f"1. W14X90 Properties:")
        print(f"   Area: {section.A} in²")
        print(f"   Ix: {section.Ix} in⁴")
        print(f"   Weight: {section.weight} lb/ft\n")

    # Test 2: Search by area
    print("2. Sections with area between 20-30 in²:")
    sections = search_sections_by_area(20, 30)
    for s in sections[:5]:
        print(f"   {s.name}: A={s.A} in², Ix={s.Ix} in⁴")
    print()

    # Test 3: Recommend column section
    print("3. Recommend column for A≥15 in², Ix≥500 in⁴:")
    recommended = recommend_section_for_column(required_area=15, required_Ix=500)
    if recommended:
        print(f"   Recommended: {recommended.name}")
        print(f"   A={recommended.A} in², Ix={recommended.Ix} in⁴, Weight={recommended.weight} lb/ft")
    print()

    # Test 4: Recommend beam section
    print("4. Recommend beam for Zx≥100 in³, max depth=22 in:")
    recommended = recommend_section_for_beam(required_Zx=100, max_depth=22)
    if recommended:
        print(f"   Recommended: {recommended.name}")
        print(f"   Zx={recommended.Zx} in³, d={recommended.d} in, Weight={recommended.weight} lb/ft")

    print(f"\nTotal sections in database: {len(WSECTION_DATABASE)}")
