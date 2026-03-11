"""
Geometry Agent
Converts natural language structural descriptions to structured JSON
"""

import json
import re
from typing import Dict, Optional, List
from openai import OpenAI
from ..models.structural_json import (
    StructuralModel, Node, Element, Material, Section,
    Load, GeometricTransformation, AnalysisSettings
)
from ..models.wsection_database import get_section_properties, recommend_section_for_column, recommend_section_for_beam


class GeometryAgent:
    """
    Agent that processes natural language descriptions of structural systems
    and outputs structured JSON representations
    """

    def __init__(self, client: Optional[OpenAI] = None, model: str = "qwen-max"):
        """
        Initialize Geometry Agent

        Args:
            client: OpenAI client (if None, will create new one from env)
            model: LLM model to use
        """
        self.client = client
        self.model = model

        # System prompt for geometry extraction
        self.system_prompt = """You are a structural engineering expert specialized in converting natural language descriptions of steel frame structures into precise JSON representations.

Your task is to extract the following information from structural descriptions:
1. **Nodes**: Identify all node locations with coordinates (x, y)
2. **Elements**: Identify all structural members (beams, columns) connecting nodes
3. **Sections**: Extract or infer W-section designations
4. **Materials**: Identify material properties (typically steel with E=29000 ksi, fy=50 ksi)
5. **Boundary Conditions**: Identify fixed/pinned/roller supports
6. **Loads**: Extract applied loads (point loads, distributed loads)
7. **Analysis Type**: Determine analysis type (static, eigenvalue, etc.)

**IMPORTANT RULES**:
- Use a consistent coordinate system (typically X=horizontal, Y=vertical)
- Node numbering starts from 1
- Element numbering starts from 1
- For fixed supports at base: constraints=[1,1,1]
- For free nodes: constraints=[0,0,0]
- Units: length in feet, forces in kips unless otherwise specified

**Response Format**:
You must respond with ONLY a valid JSON object matching this structure:
```json
{
  "structure_type": "2D_frame",
  "units": {"length": "ft", "force": "kip"},
  "ndm": 2,
  "ndf": 3,
  "nodes": [
    {"id": 1, "x": 0, "y": 0, "constraints": [1,1,1]},
    ...
  ],
  "elements": [
    {"id": 1, "type": "elasticBeamColumn", "nodes": [1, 2], "section": "W14X90", "orientation": "vertical"},
    ...
  ],
  "materials": [
    {"id": 1, "type": "steel", "E": 29000, "fy": 50}
  ],
  "sections": [
    {"name": "W14X90", "A": 26.5, "I": 999},
    ...
  ],
  "loads": [
    {"type": "point", "node": 4, "direction": "Y", "magnitude": -10.0},
    ...
  ],
  "transformations": [
    {"tag": 1, "type": "Linear"}
  ],
  "analysis": {
    "type": "static",
    "steps": 1,
    "constraints": "Plain",
    "numberer": "RCM",
    "system": "BandGeneral",
    "test": "NormDispIncr",
    "algorithm": "Newton",
    "integrator": "LoadControl",
    "tol": 1e-6,
    "max_iter": 100
  }
}
```

**DO NOT** include any explanatory text before or after the JSON. Output ONLY the JSON object."""

    def process(self, description: str, building_geometry: Optional[Dict] = None) -> StructuralModel:
        """
        Convert natural language description to structural model

        Args:
            description: Natural language structural description
            building_geometry: Optional building geometry from Task 3.1 module

        Returns:
            StructuralModel object
        """
        # If building geometry is provided, enhance the description
        if building_geometry:
            description = self._enhance_description_with_building(description, building_geometry)

        # Call LLM to extract geometry
        json_response = self._call_llm(description)

        # Parse JSON response
        try:
            model_dict = json.loads(json_response)
        except json.JSONDecodeError as e:
            # Try to extract JSON from response if LLM added extra text
            json_match = re.search(r'\{.*\}', json_response, re.DOTALL)
            if json_match:
                model_dict = json.loads(json_match.group())
            else:
                raise ValueError(f"Failed to parse JSON from LLM response: {e}")

        # Enrich sections with database properties
        model_dict = self._enrich_sections(model_dict)

        # Validate and create StructuralModel
        structural_model = StructuralModel(**model_dict)

        return structural_model

    def _enhance_description_with_building(self, description: str, building_geometry: Dict) -> str:
        """
        Enhance natural language description with building geometry from Task 3.1

        Args:
            description: Original description
            building_geometry: Building geometry dict from building_design module

        Returns:
            Enhanced description
        """
        enhancement = f"\n\nBuilding Geometry Information:\n"

        if 'rooms' in building_geometry:
            rooms = building_geometry['rooms']
            enhancement += f"- Number of rooms: {len(rooms)}\n"

            # Extract building dimensions
            max_x = max(r['x'] + r['width'] for r in rooms)
            max_y = max(r['y'] + r['height'] for r in rooms)
            enhancement += f"- Building footprint: {max_x} ft × {max_y} ft\n"

        if 'building_elevation' in building_geometry:
            elevation = building_geometry['building_elevation']
            enhancement += f"- Floor height: {elevation} ft\n"

        if 'columns' in building_geometry:
            columns = building_geometry['columns']
            enhancement += f"- Number of columns: {len(columns)}\n"
            enhancement += "- Column locations (x, y):\n"
            for col in columns:
                enhancement += f"  * ({col['x']}, {col['y']})\n"

        return description + enhancement

    def _call_llm(self, description: str) -> str:
        """
        Call LLM to extract structural geometry

        Args:
            description: Natural language description

        Returns:
            JSON string from LLM
        """
        if not self.client:
            raise ValueError("OpenAI client not initialized")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": description}
                ],
                temperature=0.1,  # Low temperature for more consistent output
            )

            return response.choices[0].message.content

        except Exception as e:
            raise RuntimeError(f"LLM call failed: {e}")

    def _enrich_sections(self, model_dict: Dict) -> Dict:
        """
        Enrich section definitions with properties from database

        Args:
            model_dict: Model dictionary from LLM

        Returns:
            Enhanced model dictionary
        """
        if 'sections' not in model_dict:
            return model_dict

        enriched_sections = []

        for section in model_dict['sections']:
            section_name = section.get('name')
            if not section_name:
                enriched_sections.append(section)
                continue

            # Look up in database
            db_props = get_section_properties(section_name)

            if db_props:
                # Use database properties
                enriched_section = {
                    'name': db_props.name,
                    'A': db_props.A,
                    'I': db_props.Ix,  # Use Ix as the primary moment of inertia
                    'Iz': db_props.Iy,
                    'J': db_props.J,
                    'd': db_props.d,
                    'bf': db_props.bf,
                    'tw': db_props.tw,
                    'tf': db_props.tf
                }
            else:
                # Keep original (possibly incomplete) properties
                enriched_section = section
                # Ensure minimum required properties
                if 'A' not in enriched_section:
                    enriched_section['A'] = 10.0  # Default fallback
                if 'I' not in enriched_section:
                    enriched_section['I'] = 100.0  # Default fallback

            enriched_sections.append(enriched_section)

        model_dict['sections'] = enriched_sections
        return model_dict

    def process_from_building_design(
        self,
        building_params: Dict,
        dead_load_psf: float = 50,
        live_load_psf: float = 40,
        num_floors: int = 1,
        lateral_load_kip: Optional[float] = None
    ) -> StructuralModel:
        """
        Create structural model directly from building design output (Task 3.1)

        Args:
            building_params: Building parameters from building_design module
            dead_load_psf: Dead load (psf)
            live_load_psf: Live load (psf)
            num_floors: Number of floors
            lateral_load_kip: Optional lateral load (kip) at top

        Returns:
            StructuralModel
        """
        # Extract building dimensions
        rooms = building_params.get('rooms', [])
        if not rooms:
            raise ValueError("No rooms found in building parameters")

        # Get building extent
        max_x = max(r['x'] + r['width'] for r in rooms)
        max_y = max(r['y'] + r['height'] for r in rooms)
        floor_height = building_params.get('building_elevation', 12)  # feet

        # Get column locations
        columns = building_params.get('columns', [])
        if not columns:
            raise ValueError("No columns found in building parameters")

        # Create nodes
        nodes = []
        node_id = 1

        # Create nodes for each column at each level
        for floor in range(num_floors + 1):
            y_coord = floor * floor_height
            for col in columns:
                x_coord = col['x']
                # Base nodes are fixed, others are free
                constraints = [1, 1, 1] if floor == 0 else [0, 0, 0]
                nodes.append({
                    'id': node_id,
                    'x': x_coord,
                    'y': y_coord,
                    'constraints': constraints
                })
                node_id += 1

        # Create column elements (vertical)
        elements = []
        elem_id = 1
        num_cols = len(columns)

        for floor in range(num_floors):
            for col_idx in range(num_cols):
                i_node = floor * num_cols + col_idx + 1
                j_node = (floor + 1) * num_cols + col_idx + 1

                # Use recommended section from column design
                col_design = building_params.get('column_designs', {}).get(f"Column_{col_idx+1}", {})
                section_name = col_design.get('type', 'W14X90')

                elements.append({
                    'id': elem_id,
                    'type': 'elasticBeamColumn',
                    'nodes': [i_node, j_node],
                    'section': section_name,
                    'orientation': 'vertical',
                    'transf_tag': 1
                })
                elem_id += 1

        # Create beam elements (horizontal) connecting columns on each floor
        for floor in range(1, num_floors + 1):
            for col_idx in range(num_cols - 1):
                i_node = floor * num_cols + col_idx + 1
                j_node = floor * num_cols + col_idx + 2

                # Use beam section (typically lighter than columns)
                beam_section = 'W21X50'  # Default beam section

                elements.append({
                    'id': elem_id,
                    'type': 'elasticBeamColumn',
                    'nodes': [i_node, j_node],
                    'section': beam_section,
                    'orientation': 'horizontal',
                    'transf_tag': 1
                })
                elem_id += 1

        # Create loads (gravity loads on each floor node)
        loads = []
        tributary_area = (max_x * max_y) / num_cols  # Approximate tributary area per column

        for floor in range(1, num_floors + 1):
            for col_idx in range(num_cols):
                node = floor * num_cols + col_idx + 1
                # Total gravity load = (DL + LL) * tributary area
                gravity_load = -(dead_load_psf + live_load_psf) * tributary_area / 1000  # Convert to kips

                loads.append({
                    'type': 'point',
                    'node': node,
                    'direction': 'Y',
                    'magnitude': gravity_load
                })

        # Add lateral load if specified
        if lateral_load_kip:
            # Apply to top corner node
            top_node = num_floors * num_cols + 1
            loads.append({
                'type': 'point',
                'node': top_node,
                'direction': 'X',
                'magnitude': lateral_load_kip
            })

        # Extract unique sections
        unique_sections = set(elem['section'] for elem in elements)
        sections = []
        for section_name in unique_sections:
            db_props = get_section_properties(section_name)
            if db_props:
                sections.append({
                    'name': db_props.name,
                    'A': db_props.A,
                    'I': db_props.Ix,
                    'Iz': db_props.Iy,
                    'J': db_props.J,
                    'd': db_props.d,
                    'bf': db_props.bf,
                    'tw': db_props.tw,
                    'tf': db_props.tf
                })

        # Create complete model dictionary
        model_dict = {
            'structure_type': '2D_frame',
            'units': {'length': 'ft', 'force': 'kip'},
            'ndm': 2,
            'ndf': 3,
            'nodes': nodes,
            'elements': elements,
            'materials': [
                {'id': 1, 'type': 'steel', 'E': 29000, 'fy': 50, 'nu': 0.3}
            ],
            'sections': sections,
            'loads': loads,
            'transformations': [
                {'tag': 1, 'type': 'Linear'}
            ],
            'analysis': {
                'type': 'static',
                'steps': 1,
                'constraints': 'Plain',
                'numberer': 'RCM',
                'system': 'BandGeneral',
                'test': 'NormDispIncr',
                'algorithm': 'Newton',
                'integrator': 'LoadControl',
                'tol': 1e-6,
                'max_iter': 100
            }
        }

        # Create and validate structural model
        structural_model = StructuralModel(**model_dict)

        return structural_model


# Example usage
if __name__ == "__main__":
    from openai import OpenAI
    import os

    print("=" * 60)
    print("Geometry Agent Demo")
    print("=" * 60)

    # Example 1: Natural language description
    description1 = """
    Create a 2-story steel frame building with 2 bays. Each bay is 20 feet wide.
    The first story height is 12 feet, and the second story height is 10 feet.
    Use W14X90 sections for all columns and W21X50 sections for all beams.
    The base is fixed. Apply a 10 kip downward load at each node on the top floor.
    Perform a static analysis.
    """

    # Initialize agent
    client = OpenAI(
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        base_url=os.getenv('LLM_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
    )

    agent = GeometryAgent(client=client)

    try:
        print("\nProcessing natural language description...")
        model = agent.process(description1)

        print(f"\n✓ Structural model created successfully!")
        print(f"  - Structure type: {model.structure_type}")
        print(f"  - Nodes: {len(model.nodes)}")
        print(f"  - Elements: {len(model.elements)}")
        print(f"  - Sections: {len(model.sections)}")
        print(f"  - Loads: {len(model.loads)}")

        # Save to JSON
        output_file = "/tmp/structural_model_example.json"
        with open(output_file, 'w') as f:
            json.dump(model.model_dump(), f, indent=2)
        print(f"\n✓ Model saved to: {output_file}")

    except Exception as e:
        print(f"\n✗ Error: {e}")
