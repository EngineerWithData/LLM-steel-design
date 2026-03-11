"""
Structural Model JSON Schema
Defines the intermediate representation between natural language and OpenSeesPy code
"""

from typing import List, Dict, Optional, Literal
from pydantic import BaseModel, Field, field_validator, model_validator


class Node(BaseModel):
    """Node definition"""
    id: int = Field(..., description="Node ID (must be unique)")
    x: float = Field(..., description="X coordinate")
    y: float = Field(..., description="Y coordinate")
    z: Optional[float] = Field(0.0, description="Z coordinate (for 3D models)")
    constraints: List[int] = Field(default_factory=list, description="DOF constraints [1=fixed, 0=free]")
    mass: Optional[List[float]] = Field(None, description="Nodal mass [mx, my, mz, ...]")


class Section(BaseModel):
    """Section properties"""
    name: str = Field(..., description="Section name (e.g., W14x90)")
    A: float = Field(..., description="Cross-sectional area (in²)")
    I: float = Field(..., description="Moment of inertia (in⁴)")
    Iz: Optional[float] = Field(None, description="Moment of inertia about z-axis (in⁴)")
    J: Optional[float] = Field(None, description="Torsional constant (in⁴)")
    d: Optional[float] = Field(None, description="Depth (in)")
    bf: Optional[float] = Field(None, description="Flange width (in)")
    tw: Optional[float] = Field(None, description="Web thickness (in)")
    tf: Optional[float] = Field(None, description="Flange thickness (in)")


class Material(BaseModel):
    """Material properties"""
    id: int = Field(..., description="Material ID")
    type: Literal["steel", "concrete", "elastic"] = Field(..., description="Material type")
    E: float = Field(..., description="Young's modulus (ksi)")
    fy: Optional[float] = Field(None, description="Yield strength (ksi)")
    nu: Optional[float] = Field(0.3, description="Poisson's ratio")
    G: Optional[float] = Field(None, description="Shear modulus (ksi)")


class Element(BaseModel):
    """Element definition"""
    id: int = Field(..., description="Element ID")
    type: str = Field(..., description="Element type (e.g., elasticBeamColumn, forceBeamColumn)")
    nodes: List[int] = Field(..., description="Connected node IDs [iNode, jNode]")
    section: str = Field(..., description="Section name")
    material_id: Optional[int] = Field(None, description="Material ID")
    orientation: Optional[str] = Field(None, description="Element orientation (vertical, horizontal)")
    transf_tag: Optional[int] = Field(1, description="Geometric transformation tag")

    @field_validator('nodes')
    @classmethod
    def validate_node_count(cls, v, info):
        elem_type = info.data.get('type', '')
        if 'beam' in elem_type.lower() or 'truss' in elem_type.lower():
            if len(v) != 2:
                raise ValueError(f"Beam/Truss elements require exactly 2 nodes, got {len(v)}")
        return v


class Load(BaseModel):
    """Load definition"""
    type: Literal["point", "distributed", "pattern"] = Field(..., description="Load type")
    node: Optional[int] = Field(None, description="Node ID (for point loads)")
    element: Optional[int] = Field(None, description="Element ID (for distributed loads)")
    direction: str = Field(..., description="Load direction (X, Y, Z, or 1, 2, 3)")
    magnitude: float = Field(..., description="Load magnitude (kip or kip/ft)")
    pattern_type: Optional[str] = Field("Plain", description="Load pattern type")


class GeometricTransformation(BaseModel):
    """Geometric transformation definition"""
    tag: int = Field(..., description="Transformation tag")
    type: Literal["Linear", "PDelta", "Corotational"] = Field(..., description="Transformation type")
    vector: Optional[List[float]] = Field(None, description="Local x-axis vector for 3D")


class AnalysisSettings(BaseModel):
    """Analysis configuration"""
    type: Literal["static", "eigenvalue", "transient", "pushover"] = Field(..., description="Analysis type")
    num_modes: Optional[int] = Field(10, description="Number of modes (for eigenvalue analysis)")
    steps: int = Field(1, description="Number of analysis steps")
    dt: Optional[float] = Field(None, description="Time step (for transient analysis)")
    constraints: str = Field("Plain", description="Constraint handler")
    numberer: str = Field("RCM", description="DOF numberer")
    system: str = Field("BandGeneral", description="System of equations")
    test: str = Field("NormDispIncr", description="Convergence test")
    algorithm: str = Field("Newton", description="Solution algorithm")
    integrator: str = Field("LoadControl", description="Integrator type")
    tol: float = Field(1e-6, description="Convergence tolerance")
    max_iter: int = Field(100, description="Maximum iterations")


class StructuralModel(BaseModel):
    """Complete structural model definition"""
    structure_type: Literal["2D_frame", "3D_frame", "truss", "shell"] = Field(..., description="Structure type")
    units: Dict[str, str] = Field(
        default_factory=lambda: {"length": "ft", "force": "kip"},
        description="Unit system"
    )
    ndm: int = Field(2, description="Number of dimensions (2 or 3)")
    ndf: int = Field(3, description="Number of DOFs per node")

    nodes: List[Node] = Field(..., description="List of nodes")
    elements: List[Element] = Field(..., description="List of elements")
    materials: List[Material] = Field(..., description="List of materials")
    sections: List[Section] = Field(..., description="List of sections")
    loads: List[Load] = Field(default_factory=list, description="List of loads")
    transformations: List[GeometricTransformation] = Field(
        default_factory=lambda: [GeometricTransformation(tag=1, type="Linear")],
        description="Geometric transformations"
    )
    analysis: AnalysisSettings = Field(..., description="Analysis settings")

    @field_validator('nodes')
    @classmethod
    def validate_unique_node_ids(cls, v):
        ids = [node.id for node in v]
        if len(ids) != len(set(ids)):
            raise ValueError("Node IDs must be unique")
        return v

    @field_validator('elements')
    @classmethod
    def validate_unique_element_ids(cls, v):
        ids = [elem.id for elem in v]
        if len(ids) != len(set(ids)):
            raise ValueError("Element IDs must be unique")
        return v

    @model_validator(mode='after')
    def validate_element_nodes_exist(self):
        node_ids = {node.id for node in self.nodes}
        for elem in self.elements:
            for node_id in elem.nodes:
                if node_id not in node_ids:
                    raise ValueError(f"Element {elem.id} references non-existent node {node_id}")
        return self

    def to_dict(self) -> dict:
        """Convert model to dictionary"""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict):
        """Create model from dictionary"""
        return cls(**data)


# Example usage and validation
if __name__ == "__main__":
    # Example: Simple 2-bay frame
    example_model = StructuralModel(
        structure_type="2D_frame",
        units={"length": "ft", "force": "kip"},
        ndm=2,
        ndf=3,
        nodes=[
            Node(id=1, x=0, y=0, constraints=[1, 1, 1]),
            Node(id=2, x=20, y=0, constraints=[1, 1, 1]),
            Node(id=3, x=40, y=0, constraints=[1, 1, 1]),
            Node(id=4, x=0, y=12, constraints=[0, 0, 0]),
            Node(id=5, x=20, y=12, constraints=[0, 0, 0]),
            Node(id=6, x=40, y=12, constraints=[0, 0, 0]),
        ],
        materials=[
            Material(id=1, type="steel", E=29000, fy=50)
        ],
        sections=[
            Section(name="W14x90", A=26.5, I=999, d=14.02, bf=14.52),
            Section(name="W21x50", A=14.7, I=984, d=20.83, bf=6.53),
        ],
        elements=[
            Element(id=1, type="elasticBeamColumn", nodes=[1, 4], section="W14x90", orientation="vertical"),
            Element(id=2, type="elasticBeamColumn", nodes=[2, 5], section="W14x90", orientation="vertical"),
            Element(id=3, type="elasticBeamColumn", nodes=[3, 6], section="W14x90", orientation="vertical"),
            Element(id=4, type="elasticBeamColumn", nodes=[4, 5], section="W21x50", orientation="horizontal"),
            Element(id=5, type="elasticBeamColumn", nodes=[5, 6], section="W21x50", orientation="horizontal"),
        ],
        transformations=[
            GeometricTransformation(tag=1, type="Linear")
        ],
        loads=[
            Load(type="point", node=4, direction="Y", magnitude=-10.0),
            Load(type="point", node=5, direction="Y", magnitude=-10.0),
            Load(type="point", node=6, direction="Y", magnitude=-10.0),
        ],
        analysis=AnalysisSettings(
            type="static",
            steps=1,
            constraints="Plain",
            numberer="RCM",
            system="BandGeneral",
            test="NormDispIncr",
            algorithm="Newton",
            integrator="LoadControl",
            tol=1e-6,
            max_iter=100
        )
    )

    # Validate and display
    print("✓ Model validation passed")
    print(f"  Nodes: {len(example_model.nodes)}")
    print(f"  Elements: {len(example_model.elements)}")
    print(f"  Loads: {len(example_model.loads)}")

    # Export to JSON
    import json
    json_str = example_model.model_dump_json(indent=2)
    print("\nJSON representation:")
    print(json_str[:500] + "...")
