"""
Building Description Parser
Uses LLM to parse natural language building descriptions into structured data
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def parse_building_description(text: str, client: OpenAI = None) -> dict:
    """
    Use LLM to parse building description and extract blueprint parameters.
    
    Args:
        text: Natural language building description
        client: OpenAI client (optional, will create if not provided)
    
    Returns:
        Dictionary with rooms, connections, and building dimensions
    """
    if client is None:
        api_key = os.getenv('DASHSCOPE_API_KEY') or os.getenv('OPENAI_API_KEY')
        base_url = os.getenv('LLM_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
        client = OpenAI(api_key=api_key, base_url=base_url)
    
    system_message = {
        "role": "system",
        "content": (
            "You are a building layout parser. Extract structured blueprint parameters from "
            "natural language descriptions. Return ONLY a valid JSON object."
        )
    }
    
    user_message = {
        "role": "user",
        "content": (
            f"Building description: \"{text}\"\n\n"
            "Extract blueprint parameters and return a JSON object with:\n"
            "- \"rooms\": list of room objects with:\n"
            "  - \"label\": string (room name)\n"
            "  - \"width\": number (in feet, default 20)\n"
            "  - \"height\": number (in feet, default 15)\n"
            "  - \"x\": number (x coordinate)\n"
            "  - \"y\": number (y coordinate)\n"
            "  - \"shape\": string (default \"rectangle\")\n"
            "- \"connections\": list of connection objects with:\n"
            "  - \"from\": string (room label)\n"
            "  - \"to\": string (room label)\n"
            "- \"building_elevation\": number (building height in feet, default 10)\n"
            "- \"rotation_angle\": number (degrees, default 30)\n"
            "- \"vantage_point\": [x, y, z] (camera position, default [300, 1000, 600])\n\n"
            "Rules:\n"
            "- Rooms must NOT overlap\n"
            "- All rooms must be connected via corridors or direct connections\n"
            "- Arrange rooms logically based on description\n"
            "- Return ONLY valid JSON, no markdown or explanations"
        )
    }
    
    try:
        response = client.chat.completions.create(
            model=os.getenv('LLM_MODEL', 'qwen-max'),
            messages=[system_message, user_message],
            temperature=0.7
        )
        
        answer = response.choices[0].message.content.strip()
        
        # Extract JSON from response
        answer = answer.replace("```json", "").replace("```", "").strip()
        start = answer.find("{")
        end = answer.rfind("}") + 1
        if start != -1 and end > start:
            answer = answer[start:end]
        
        import json
        blueprint_params = json.loads(answer)
        
        # Validate and fix parameters
        blueprint_params = _fix_blueprint_params(blueprint_params)
        
        return blueprint_params
        
    except Exception as e:
        print(f"Error parsing building description: {e}")
        # Return default layout
        return {
            "rooms": [
                {"label": "Room 1", "width": 20, "height": 15, "x": 0, "y": 0, "shape": "rectangle"},
                {"label": "Room 2", "width": 20, "height": 15, "x": 0, "y": 15, "shape": "rectangle"}
            ],
            "connections": [{"from": "Room 1", "to": "Room 2"}],
            "building_elevation": 10,
            "rotation_angle": 30,
            "vantage_point": [300, 1000, 600]
        }


def _fix_blueprint_params(blueprint: dict) -> dict:
    """
    Validate and fix blueprint parameters to ensure no overlaps and proper connections.
    
    Args:
        blueprint: Raw blueprint parameters
    
    Returns:
        Fixed blueprint parameters
    """
    rooms = blueprint.get("rooms", [])
    
    # Set defaults
    for room in rooms:
        room.setdefault("width", 20)
        room.setdefault("height", 15)
        room.setdefault("x", 0)
        room.setdefault("y", 0)
        room.setdefault("shape", "rectangle")
    
    # Fix overlaps using simple grid layout
    arranged_rooms = []
    spacing = 2  # 2 feet spacing between rooms
    current_x, current_y = 0, 0
    row_height = 0
    max_row_width = 100  # Maximum width before wrapping to next row
    
    for room in rooms:
        # Check if need to wrap to next row
        if current_x > 0 and current_x + room["width"] > max_row_width:
            current_x = 0
            current_y += row_height + spacing
            row_height = 0
        
        # Set position
        room["x"] = current_x
        room["y"] = current_y
        
        # Check for overlaps with already placed rooms
        while any(_is_overlap(room, placed) for placed in arranged_rooms):
            room["x"] += room["width"] + spacing
            current_x = room["x"]
        
        arranged_rooms.append(room)
        
        # Update grid position
        row_height = max(row_height, room["height"])
        current_x = room["x"] + room["width"] + spacing
    
    blueprint["rooms"] = arranged_rooms
    
    # Calculate building dimensions
    if arranged_rooms:
        max_x = max(r["x"] + r["width"] for r in arranged_rooms)
        max_y = max(r["y"] + r["height"] for r in arranged_rooms)
        blueprint["total_building_width"] = max_x
        blueprint["total_building_height"] = max_y
    
    # Ensure default values for visualization
    blueprint.setdefault("building_elevation", 10)
    blueprint.setdefault("rotation_angle", 30)
    blueprint.setdefault("vantage_point", [300, 1000, 600])
    blueprint.setdefault("margin", 50)
    blueprint.setdefault("connections", [])
    
    return blueprint


def _is_overlap(room1: dict, room2: dict) -> bool:
    """Check if two rooms overlap."""
    x1, y1, w1, h1 = room1["x"], room1["y"], room1["width"], room1["height"]
    x2, y2, w2, h2 = room2["x"], room2["y"], room2["width"], room2["height"]
    return (x1 < x2 + w2 and x1 + w1 > x2 and
            y1 < y2 + h2 and y1 + h1 > y2)

