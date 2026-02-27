"""
Column Load Analysis and Optimization
Calculates column loads and optimizes column sections
"""

from typing import Dict, List, Optional


def calculate_tributary_area(
    room_width: float,
    room_length: float,
    num_columns_width: int = 2,
    num_columns_length: int = 2
) -> float:
    """
    Calculate tributary area for a column.
    
    Args:
        room_width: Width of room in feet
        room_length: Length of room in feet
        num_columns_width: Number of columns along width
        num_columns_length: Number of columns along length
    
    Returns:
        Tributary area in square feet
    """
    spacing_width = room_width / (num_columns_width - 1) if num_columns_width > 1 else room_width
    spacing_length = room_length / (num_columns_length - 1) if num_columns_length > 1 else room_length
    
    tributary_area = spacing_width * spacing_length
    return tributary_area


def calculate_column_load(
    tributary_area: float,
    dead_load_psf: float = 50,
    live_load_psf: float = 40,
    num_floors: int = 1
) -> float:
    """
    Calculate total axial load on a column.
    
    Args:
        tributary_area: Tributary area in square feet
        dead_load_psf: Dead load in pounds per square foot (structure weight)
                      Typical: 50-150 psf for concrete/steel buildings
        live_load_psf: Live load in pounds per square foot (occupancy)
                      ASCE residential: 40 psf, office: 50 psf
        num_floors: Number of floors the column supports
    
    Returns:
        Total axial load in pounds
    """
    total_load_per_floor = tributary_area * (dead_load_psf + live_load_psf)
    total_load = total_load_per_floor * num_floors
    return total_load


def calculate_all_column_loads(
    blueprint_params: dict,
    dead_load_psf: float = 50,
    live_load_psf: float = 40,
    num_floors: int = 1
) -> Dict[str, float]:
    """
    Calculate loads for all columns in the building.
    
    Args:
        blueprint_params: Building blueprint parameters
        dead_load_psf: Dead load in psf
        live_load_psf: Live load in psf
        num_floors: Number of floors
    
    Returns:
        Dictionary mapping column positions to loads (in pounds)
    """
    rooms = blueprint_params.get("rooms", [])
    column_loads = {}
    
    for room in rooms:
        x = room.get("x", 0)
        y = room.get("y", 0)
        width = room.get("width", 20)
        height = room.get("height", 15)
        
        # Calculate tributary area (assume 2x2 column grid per room)
        tributary_area = calculate_tributary_area(width, height, 2, 2)
        column_load = calculate_column_load(tributary_area, dead_load_psf, live_load_psf, num_floors)
        
        # Define corner columns
        corners = [
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height)
        ]
        
        for corner in corners:
            corner_key = f"Column_({corner[0]:.1f},{corner[1]:.1f})"
            
            # If column is shared by multiple rooms, add loads
            if corner_key in column_loads:
                column_loads[corner_key] += column_load / 4
            else:
                column_loads[corner_key] = column_load / 4
    
    return column_loads


def predict_column_strength(column_section: dict, material: str = "steel") -> float:
    """
    Predict column strength based on section properties.
    
    Args:
        column_section: Dictionary with section properties
        material: Material type (steel or concrete)
    
    Returns:
        Predicted column strength in pounds
    """
    if material == "steel":
        # Steel column capacity: P_n = F_y * A_g * φ
        area = column_section.get("area", 10)  # square inches
        fy = column_section.get("fy", 50)  # ksi (A992 steel default)
        phi = 0.9  # resistance factor
        
        capacity = area * fy * 1000 * phi  # Convert ksi to psi
        return capacity
        
    elif material == "concrete":
        # Concrete column capacity: P_n = 0.85 * f'c * A_g * φ
        area = column_section.get("area", 144)  # square inches
        fc = column_section.get("fc", 4)  # ksi
        phi = 0.65  # resistance factor
        
        capacity = 0.85 * fc * 1000 * area * phi
        return capacity
    
    return 0


def optimize_column_section(
    required_load: float,
    material: str = "steel",
    available_sections: Optional[List[dict]] = None
) -> dict:
    """
    Select optimal column section to support required load.
    
    Args:
        required_load: Required axial load capacity in pounds
        material: Material type
        available_sections: List of available sections
    
    Returns:
        Optimal column section dictionary
    """
    if available_sections is None:
        # Default steel W-sections (AISC standard sections)
        available_sections = [
            {"type": "W14x90", "area": 26.5, "fy": 50, "cost_factor": 1.0},
            {"type": "W14x120", "area": 35.3, "fy": 50, "cost_factor": 1.33},
            {"type": "W14x145", "area": 42.7, "fy": 50, "cost_factor": 1.61},
            {"type": "W12x72", "area": 21.1, "fy": 50, "cost_factor": 0.80},
            {"type": "W12x96", "area": 28.2, "fy": 50, "cost_factor": 1.06},
            {"type": "W10x60", "area": 17.6, "fy": 50, "cost_factor": 0.66},
            {"type": "W10x77", "area": 22.6, "fy": 50, "cost_factor": 0.85},
            {"type": "W8x48", "area": 14.1, "fy": 50, "cost_factor": 0.53},
            {"type": "W8x67", "area": 19.7, "fy": 50, "cost_factor": 0.74},
        ]
    
    optimal_section = None
    min_cost = float('inf')
    
    for section in available_sections:
        # Predict capacity
        capacity = predict_column_strength(section, material)
        
        # Check if meets requirement with safety margin
        if capacity >= required_load * 1.1:  # 10% safety margin
            cost = section["area"] * section.get("cost_factor", 1.0)
            
            if cost < min_cost:
                min_cost = cost
                optimal_section = section.copy()
                optimal_section["capacity"] = capacity
                optimal_section["utilization"] = required_load / capacity
    
    if optimal_section is None:
        # No suitable section found, return largest available
        largest = max(available_sections, key=lambda s: s["area"])
        capacity = predict_column_strength(largest, material)
        optimal_section = largest.copy()
        optimal_section["capacity"] = capacity
        optimal_section["utilization"] = required_load / capacity
        optimal_section["warning"] = "Required load exceeds all available sections!"
    
    return optimal_section


def generate_column_design_report(
    blueprint_params: dict,
    dead_load_psf: float = 50,
    live_load_psf: float = 40,
    num_floors: int = 1,
    material: str = "steel"
) -> dict:
    """
    Generate comprehensive column design report.
    
    Args:
        blueprint_params: Building blueprint parameters
        dead_load_psf: Dead load in psf
        live_load_psf: Live load in psf
        num_floors: Number of floors
        material: Column material
    
    Returns:
        Dictionary with column analysis and design recommendations
    """
    # Calculate column loads
    column_loads = calculate_all_column_loads(
        blueprint_params,
        dead_load_psf,
        live_load_psf,
        num_floors
    )
    
    # Optimize each column
    column_designs = {}
    total_steel_weight = 0
    
    for col_name, required_load in column_loads.items():
        optimal_section = optimize_column_section(required_load, material)
        column_designs[col_name] = optimal_section
        
        # Calculate steel weight (approximate)
        building_height = blueprint_params.get("building_elevation", 10)
        weight_per_foot = optimal_section["area"] * 3.4  # lbs/ft for steel
        total_steel_weight += weight_per_foot * building_height
    
    report = {
        "summary": {
            "total_columns": len(column_loads),
            "total_load": sum(column_loads.values()),
            "total_steel_weight": total_steel_weight,
            "material": material,
            "num_floors": num_floors
        },
        "column_loads": column_loads,
        "column_designs": column_designs,
        "warnings": []
    }
    
    # Check for warnings
    for col_name, design in column_designs.items():
        if "warning" in design:
            report["warnings"].append({
                "column": col_name,
                "message": design["warning"]
            })
        elif design.get("utilization", 0) > 0.95:
            report["warnings"].append({
                "column": col_name,
                "message": f"High utilization: {design['utilization']:.1%}"
            })
    
    return report

