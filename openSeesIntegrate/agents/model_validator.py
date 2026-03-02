"""
Model Validation Agent
Validates generated OpenSeesPy code for syntax, semantic, and structural correctness
"""

import ast
import re
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass
from ..models.structural_json import StructuralModel


@dataclass
class ValidationResult:
    """Result of validation check"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]

    def add_error(self, message: str):
        """Add an error message"""
        self.errors.append(message)
        self.is_valid = False

    def add_warning(self, message: str):
        """Add a warning message"""
        self.warnings.append(message)


class ModelValidationAgent:
    """
    Agent that validates structural models and generated OpenSeesPy code
    """

    def __init__(self):
        """Initialize Model Validation Agent"""
        pass

    def validate_model(self, model: StructuralModel) -> ValidationResult:
        """
        Validate structural model before code generation

        Args:
            model: Structural model to validate

        Returns:
            ValidationResult object
        """
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        # 1. Validate nodes
        self._validate_nodes(model, result)

        # 2. Validate elements
        self._validate_elements(model, result)

        # 3. Validate boundary conditions
        self._validate_boundary_conditions(model, result)

        # 4. Validate loads
        self._validate_loads(model, result)

        # 5. Validate structural stability
        self._validate_stability(model, result)

        return result

    def validate_code(self, code: str, model: Optional[StructuralModel] = None) -> ValidationResult:
        """
        Validate generated OpenSeesPy code

        Args:
            code: Generated Python/OpenSeesPy code
            model: Optional original model for cross-validation

        Returns:
            ValidationResult object
        """
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        # 1. Syntax validation
        self._validate_syntax(code, result)

        # 2. Semantic validation (OpenSees commands)
        self._validate_opensees_commands(code, result)

        # 3. Cross-validation with model (if provided)
        if model and result.is_valid:
            self._cross_validate_code_with_model(code, model, result)

        return result

    def _validate_nodes(self, model: StructuralModel, result: ValidationResult):
        """Validate node definitions"""
        node_ids = set()

        for node in model.nodes:
            # Check for duplicate IDs
            if node.id in node_ids:
                result.add_error(f"Duplicate node ID: {node.id}")
            node_ids.add(node.id)

            # Check for reasonable coordinates
            if abs(node.x) > 10000 or abs(node.y) > 10000:
                result.add_warning(f"Node {node.id} has unusually large coordinates: ({node.x}, {node.y})")

            # Check constraints
            if len(node.constraints) != model.ndf:
                result.add_error(
                    f"Node {node.id} has {len(node.constraints)} constraints but model has {model.ndf} DOFs"
                )

    def _validate_elements(self, model: StructuralModel, result: ValidationResult):
        """Validate element definitions"""
        element_ids = set()
        node_ids = {node.id for node in model.nodes}
        section_names = {section.name for section in model.sections}

        for elem in model.elements:
            # Check for duplicate IDs
            if elem.id in element_ids:
                result.add_error(f"Duplicate element ID: {elem.id}")
            element_ids.add(elem.id)

            # Check node connectivity
            for node_id in elem.nodes:
                if node_id not in node_ids:
                    result.add_error(f"Element {elem.id} references non-existent node {node_id}")

            # Check for same node at both ends
            if len(elem.nodes) == 2 and elem.nodes[0] == elem.nodes[1]:
                result.add_error(f"Element {elem.id} has the same node at both ends: {elem.nodes[0]}")

            # Check section exists
            if elem.section not in section_names:
                result.add_error(f"Element {elem.id} references non-existent section: {elem.section}")

            # Check for zero-length elements
            if len(elem.nodes) == 2:
                node_i = next((n for n in model.nodes if n.id == elem.nodes[0]), None)
                node_j = next((n for n in model.nodes if n.id == elem.nodes[1]), None)

                if node_i and node_j:
                    length = ((node_j.x - node_i.x)**2 + (node_j.y - node_i.y)**2)**0.5
                    if length < 1e-6:
                        result.add_warning(f"Element {elem.id} has near-zero length")

    def _validate_boundary_conditions(self, model: StructuralModel, result: ValidationResult):
        """Validate boundary conditions"""
        # Count total constraints
        total_constraints = sum(
            sum(1 for c in node.constraints if c == 1)
            for node in model.nodes
        )

        # Minimum constraints needed to prevent rigid body motion
        # 2D: need at least 3 constraints (2 translations + 1 rotation)
        # 3D: need at least 6 constraints (3 translations + 3 rotations)
        min_constraints = 3 if model.ndm == 2 else 6

        if total_constraints < min_constraints:
            result.add_error(
                f"Insufficient boundary constraints ({total_constraints}). "
                f"Need at least {min_constraints} to prevent rigid body motion."
            )

        # Check if at least one node is fully fixed
        fully_fixed = any(
            all(c == 1 for c in node.constraints)
            for node in model.nodes
        )

        if not fully_fixed:
            result.add_warning("No fully fixed nodes. Model may be unstable.")

    def _validate_loads(self, model: StructuralModel, result: ValidationResult):
        """Validate load definitions"""
        node_ids = {node.id for node in model.nodes}
        element_ids = {elem.id for elem in model.elements}

        for load in model.loads:
            if load.type == "point":
                if load.node and load.node not in node_ids:
                    result.add_error(f"Load references non-existent node: {load.node}")

            elif load.type == "distributed":
                if load.element and load.element not in element_ids:
                    result.add_error(f"Load references non-existent element: {load.element}")

            # Check for reasonable load magnitudes
            if abs(load.magnitude) > 10000:
                result.add_warning(
                    f"Load has unusually large magnitude: {load.magnitude} "
                    f"(check units)"
                )

    def _validate_stability(self, model: StructuralModel, result: ValidationResult):
        """Validate structural stability"""
        # Build adjacency graph
        node_ids = {node.id for node in model.nodes}
        connections = {node_id: set() for node_id in node_ids}

        for elem in model.elements:
            if len(elem.nodes) == 2:
                i, j = elem.nodes
                connections[i].add(j)
                connections[j].add(i)

        # Check for isolated nodes
        for node in model.nodes:
            if not connections[node.id]:
                # Check if it's a support node (has constraints)
                if not any(c == 1 for c in node.constraints):
                    result.add_error(f"Node {node.id} is isolated (not connected to any elements)")

        # Check connectivity - all free nodes should be reachable from supports
        support_nodes = {
            node.id for node in model.nodes
            if any(c == 1 for c in node.constraints)
        }

        if support_nodes:
            visited = self._dfs_connectivity(connections, next(iter(support_nodes)))
            free_nodes = {
                node.id for node in model.nodes
                if not any(c == 1 for c in node.constraints)
            }

            disconnected = free_nodes - visited
            if disconnected:
                result.add_warning(
                    f"Some nodes are not connected to supports: {disconnected}"
                )

    def _dfs_connectivity(self, graph: Dict[int, Set[int]], start: int) -> Set[int]:
        """Depth-first search to find connected nodes"""
        visited = set()
        stack = [start]

        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            stack.extend(graph[node] - visited)

        return visited

    def _validate_syntax(self, code: str, result: ValidationResult):
        """Validate Python syntax"""
        try:
            ast.parse(code)
        except SyntaxError as e:
            result.add_error(f"Syntax error in generated code: {e}")

    def _validate_opensees_commands(self, code: str, result: ValidationResult):
        """Validate OpenSees-specific commands"""
        # Check for required OpenSees commands
        required_commands = ['model', 'node', 'element', 'analyze']

        for cmd in required_commands:
            pattern = rf'\b{cmd}\s*\('
            if not re.search(pattern, code):
                result.add_warning(f"Missing expected OpenSees command: {cmd}()")

        # Check for proper wipe() call
        if 'wipe()' not in code:
            result.add_warning("Missing wipe() command to clear previous model")

        # Check for analysis setup
        analysis_commands = ['constraints', 'numberer', 'system', 'test', 'algorithm', 'integrator']
        missing_analysis = []

        for cmd in analysis_commands:
            if cmd not in code:
                missing_analysis.append(cmd)

        if missing_analysis:
            result.add_warning(
                f"Missing analysis setup commands: {', '.join(missing_analysis)}"
            )

    def _cross_validate_code_with_model(self, code: str, model: StructuralModel, result: ValidationResult):
        """Cross-validate generated code with original model"""
        # Count nodes in code
        node_pattern = r'node\s*\(\s*(\d+)'
        code_nodes = set(int(m.group(1)) for m in re.finditer(node_pattern, code))
        model_nodes = {node.id for node in model.nodes}

        if code_nodes != model_nodes:
            missing = model_nodes - code_nodes
            extra = code_nodes - model_nodes
            if missing:
                result.add_error(f"Code missing nodes from model: {missing}")
            if extra:
                result.add_error(f"Code has extra nodes not in model: {extra}")

        # Count elements in code
        element_pattern = r'element\s*\(\s*[\'"]?\w+[\'"]?\s*,\s*(\d+)'
        code_elements = set(int(m.group(1)) for m in re.finditer(element_pattern, code))
        model_elements = {elem.id for elem in model.elements}

        if len(code_elements) != len(model_elements):
            result.add_warning(
                f"Element count mismatch: code has {len(code_elements)}, "
                f"model has {len(model_elements)}"
            )

    def validate_results(self, results: Dict) -> ValidationResult:
        """
        Validate analysis results for reasonableness

        Args:
            results: Dictionary of analysis results

        Returns:
            ValidationResult object
        """
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        # Check for NaN or infinite values
        if 'displacements' in results:
            disps = results['displacements']
            if any(abs(d) > 1e6 for d in disps.values()):
                result.add_warning("Some displacements are extremely large (possible instability)")

        if 'reactions' in results:
            reactions = results['reactions']
            if any(abs(r) > 1e6 for r in reactions.values()):
                result.add_warning("Some reactions are extremely large")

        # Check for analysis convergence
        if 'converged' in results and not results['converged']:
            result.add_error("Analysis did not converge")

        return result


# Example usage
if __name__ == "__main__":
    from ..models.structural_json import StructuralModel, Node, Element, Material, Section, Load

    print("=" * 60)
    print("Model Validation Agent Demo")
    print("=" * 60)

    # Test 1: Valid model
    print("\n[Test 1] Validating a correct model...")
    valid_model = StructuralModel(
        structure_type="2D_frame",
        units={"length": "ft", "force": "kip"},
        ndm=2,
        ndf=3,
        nodes=[
            Node(id=1, x=0, y=0, constraints=[1, 1, 1]),
            Node(id=2, x=20, y=0, constraints=[1, 1, 1]),
            Node(id=3, x=0, y=12, constraints=[0, 0, 0]),
            Node(id=4, x=20, y=12, constraints=[0, 0, 0]),
        ],
        materials=[Material(id=1, type="steel", E=29000, fy=50)],
        sections=[
            Section(name="W14X90", A=26.5, I=999),
            Section(name="W21X50", A=14.7, I=984),
        ],
        elements=[
            Element(id=1, type="elasticBeamColumn", nodes=[1, 3], section="W14X90"),
            Element(id=2, type="elasticBeamColumn", nodes=[2, 4], section="W14X90"),
            Element(id=3, type="elasticBeamColumn", nodes=[3, 4], section="W21X50"),
        ],
        loads=[
            Load(type="point", node=3, direction="Y", magnitude=-10.0),
        ],
        analysis={
            "type": "static",
            "steps": 1,
        }
    )

    validator = ModelValidationAgent()
    result = validator.validate_model(valid_model)

    print(f"Validation result: {'✓ PASS' if result.is_valid else '✗ FAIL'}")
    if result.errors:
        print("Errors:")
        for error in result.errors:
            print(f"  - {error}")
    if result.warnings:
        print("Warnings:")
        for warning in result.warnings:
            print(f"  - {warning}")

    # Test 2: Invalid model (duplicate node ID)
    print("\n[Test 2] Validating a model with errors...")
    invalid_model = StructuralModel(
        structure_type="2D_frame",
        units={"length": "ft", "force": "kip"},
        ndm=2,
        ndf=3,
        nodes=[
            Node(id=1, x=0, y=0, constraints=[0, 0, 0]),  # No supports!
            Node(id=2, x=20, y=0, constraints=[0, 0, 0]),
        ],
        materials=[Material(id=1, type="steel", E=29000, fy=50)],
        sections=[Section(name="W14X90", A=26.5, I=999)],
        elements=[
            Element(id=1, type="elasticBeamColumn", nodes=[1, 2], section="W14X90"),
        ],
        loads=[],
        analysis={"type": "static", "steps": 1}
    )

    result = validator.validate_model(invalid_model)

    print(f"Validation result: {'✓ PASS' if result.is_valid else '✗ FAIL'}")
    if result.errors:
        print("Errors:")
        for error in result.errors:
            print(f"  - {error}")
    if result.warnings:
        print("Warnings:")
        for warning in result.warnings:
            print(f"  - {warning}")

    # Test 3: Code validation
    print("\n[Test 3] Validating generated code...")
    sample_code = """
from openseespy.opensees import *

wipe()
model('basic', '-ndm', 2, '-ndf', 3)

node(1, 0.0, 0.0)
node(2, 240.0, 0.0)

fix(1, 1, 1, 1)
fix(2, 1, 1, 1)

element('elasticBeamColumn', 1, 1, 2, 26.5, 29000000, 999, 1)

constraints('Plain')
numberer('RCM')
system('BandGeneral')
test('NormDispIncr', 1e-6, 100)
algorithm('Newton')
integrator('LoadControl', 1.0)
analysis('Static')

analyze(1)
"""

    result = validator.validate_code(sample_code)
    print(f"Code validation: {'✓ PASS' if result.is_valid else '✗ FAIL'}")
    if result.warnings:
        print("Warnings:")
        for warning in result.warnings:
            print(f"  - {warning}")

    print("\n" + "=" * 60)
    print("✓ Validation demos complete")
