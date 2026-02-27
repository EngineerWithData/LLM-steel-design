"""
Blueprint Generator
Generates 3D perspective SVG blueprints from building parameters
"""

import math
try:
    import svgwrite
except ImportError:
    svgwrite = None
    print("Warning: svgwrite not installed. Run: pip install svgwrite")


def rotate_z(point: tuple, angle_deg: float) -> tuple:
    """
    Rotate a 3D point about the z-axis.
    
    Args:
        point: (x, y, z) coordinates
        angle_deg: Rotation angle in degrees
    
    Returns:
        Rotated (x, y, z) coordinates
    """
    x, y, z = point
    theta = math.radians(angle_deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    return (x * cos_t - y * sin_t, x * sin_t + y * cos_t, z)


def perspective_project(point: tuple, vantage: tuple, screen_z: float = 0.0) -> tuple:
    """
    Project a 3D point onto a 2D plane using perspective projection.
    
    Args:
        point: (x, y, z) 3D point
        vantage: (x, y, z) camera position
        screen_z: Z-coordinate of projection plane
    
    Returns:
        (x, y) 2D projected coordinates
    """
    px, py, pz = point
    vx, vy, vz = vantage
    
    if abs(pz - vz) < 1e-9:
        return (px, py)
    
    t = (screen_z - vz) / (pz - vz)
    return (vx + t * (px - vx), vy + t * (py - vy))


def transform_room_polygon(room: dict, rotation_angle: float) -> list:
    """
    Transform room corners to 3D coordinates with rotation.
    
    Args:
        room: Room dictionary with x, y, width, height
        rotation_angle: Rotation angle in degrees
    
    Returns:
        List of 3D corner points
    """
    x = room.get("x", 0)
    y = room.get("y", 0)
    w = room.get("width", 20)
    h = room.get("height", 15)
    
    corners = [
        (x, y, 0),
        (x + w, y, 0),
        (x + w, y + h, 0),
        (x, y + h, 0)
    ]
    
    return [rotate_z(pt, rotation_angle) for pt in corners]


def generate_blueprint(blueprint_params: dict, filename: str = "blueprint.svg") -> str:
    """
    Generate a 3D perspective SVG blueprint from building parameters.
    
    Args:
        blueprint_params: Dictionary with rooms, connections, building_elevation, etc.
        filename: Output SVG filename
    
    Returns:
        Path to generated SVG file
    """
    if svgwrite is None:
        raise ImportError("svgwrite is required. Install with: pip install svgwrite")
    
    # Extract parameters
    building_elevation = blueprint_params.get("building_elevation", 10)
    rotation_angle = blueprint_params.get("rotation_angle", 30)
    vantage_point = tuple(blueprint_params.get("vantage_point", [300, 1000, 600]))
    margin = blueprint_params.get("margin", 50)
    rooms = blueprint_params.get("rooms", [])
    connections = blueprint_params.get("connections", [])
    
    # Calculate canvas dimensions
    all_proj_points = []
    for rm in rooms:
        rm_poly = transform_room_polygon(rm, rotation_angle)
        for pt in rm_poly:
            # Floor projection
            floor_pt = perspective_project(pt, vantage_point)
            all_proj_points.append(floor_pt)
            # Roof projection
            roof_pt = perspective_project((pt[0], pt[1], building_elevation), vantage_point)
            all_proj_points.append(roof_pt)
    
    if not all_proj_points:
        all_proj_points = [(0, 0)]
    
    min_x = min(pt[0] for pt in all_proj_points)
    max_x = max(pt[0] for pt in all_proj_points)
    min_y = min(pt[1] for pt in all_proj_points)
    max_y = max(pt[1] for pt in all_proj_points)
    
    canvas_w = (max_x - min_x) + 2 * margin
    canvas_h = (max_y - min_y) + 2 * margin
    
    # Create SVG drawing
    dwg = svgwrite.Drawing(filename, size=(canvas_w, canvas_h))
    offset_x = margin - min_x
    offset_y = margin - min_y
    
    def shift(pt):
        return (pt[0] + offset_x, pt[1] + offset_y)
    
    g = dwg.g()
    
    # Store room centers for connections
    room_centers_floor = {}
    room_centers_roof = {}
    all_room_vertices = []
    
    # Draw room outlines on floor
    for rm in rooms:
        rm_poly = transform_room_polygon(rm, rotation_angle)
        
        # Draw floor outline (blue)
        floor_proj = [perspective_project(pt, vantage_point) for pt in rm_poly]
        g.add(dwg.polygon(
            points=[shift(pt) for pt in floor_proj],
            fill="none",
            stroke="blue",
            stroke_width=2
        ))
        
        # Save vertices for columns
        all_room_vertices.extend(rm_poly)
        
        # Calculate room center
        rx = rm.get("x", 0)
        ry = rm.get("y", 0)
        w = rm.get("width", 20)
        h = rm.get("height", 15)
        
        center_floor_3d = (rx + w / 2, ry + h / 2, 0)
        center_floor_rot = rotate_z(center_floor_3d, rotation_angle)
        center_floor_2d = perspective_project(center_floor_rot, vantage_point)
        room_centers_floor[rm.get("label", "Room")] = center_floor_2d
        
        # Add room label
        g.add(dwg.text(
            rm.get("label", "Room"),
            insert=shift(center_floor_2d),
            text_anchor="middle",
            alignment_baseline="middle",
            font_size="14px",
            fill="darkblue",
            font_weight="bold"
        ))
        
        # Calculate roof center
        center_roof_3d = (rx + w / 2, ry + h / 2, building_elevation)
        center_roof_rot = rotate_z(center_roof_3d, rotation_angle)
        center_roof_2d = perspective_project(center_roof_rot, vantage_point)
        room_centers_roof[rm.get("label", "Room")] = center_roof_2d
    
    # Draw room connections on floor
    for conn in connections:
        label_from = conn.get("from")
        label_to = conn.get("to")
        pt_from = room_centers_floor.get(label_from)
        pt_to = room_centers_floor.get(label_to)
        
        if pt_from and pt_to:
            g.add(dwg.line(
                start=shift(pt_from),
                end=shift(pt_to),
                stroke="green",
                stroke_width=1,
                stroke_dasharray="5,5"
            ))
    
    # Draw roof structure
    for rm in rooms:
        rm_poly = transform_room_polygon(rm, rotation_angle)
        n = len(rm_poly)
        
        for i in range(n):
            p1 = rm_poly[i]
            p2 = rm_poly[(i + 1) % n]
            
            # Roof edges
            p1_roof = (p1[0], p1[1], building_elevation)
            p2_roof = (p2[0], p2[1], building_elevation)
            p1_roof_proj = perspective_project(p1_roof, vantage_point)
            p2_roof_proj = perspective_project(p2_roof, vantage_point)
            
            g.add(dwg.line(
                start=shift(p1_roof_proj),
                end=shift(p2_roof_proj),
                stroke="gray",
                stroke_width=1
            ))
    
    # Draw vertical columns
    for pt in all_room_vertices:
        floor_proj_pt = perspective_project(pt, vantage_point)
        roof_pt = (pt[0], pt[1], building_elevation)
        roof_proj_pt = perspective_project(roof_pt, vantage_point)
        
        g.add(dwg.line(
            start=shift(floor_proj_pt),
            end=shift(roof_proj_pt),
            stroke="brown",
            stroke_width=2
        ))
        
        g.add(dwg.circle(
            center=shift(floor_proj_pt),
            r=3,
            fill="brown"
        ))
        
        g.add(dwg.circle(
            center=shift(roof_proj_pt),
            r=3,
            fill="brown"
        ))
    
    # Add title
    g.add(dwg.text(
        "Building Blueprint - 3D Perspective View",
        insert=(canvas_w / 2, 20),
        text_anchor="middle",
        font_size="18px",
        fill="black",
        font_weight="bold"
    ))
    
    dwg.add(g)
    dwg.save()
    
    return filename

