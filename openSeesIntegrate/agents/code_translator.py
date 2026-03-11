"""
Code Translation Agent
Converts structured JSON to executable OpenSeesPy code
"""

from typing import Dict, List
from ..models.structural_json import StructuralModel


class CodeTranslationAgent:
    """
    Agent that converts structured JSON representations to valid OpenSeesPy code
    """

    def __init__(self):
        """Initialize Code Translation Agent"""
        self.indent = "    "  # 4 spaces for indentation

    def translate(self, model: StructuralModel) -> str:
        """
        Convert StructuralModel to OpenSeesPy code

        Args:
            model: Structural model object

        Returns:
            Python code string for OpenSeesPy
        """
        code_sections = []

        # Header and imports
        code_sections.append(self._generate_header(model))

        # Model initialization
        code_sections.append(self._generate_model_init(model))

        # Materials
        code_sections.append(self._generate_materials(model))

        # Nodes
        code_sections.append(self._generate_nodes(model))

        # Geometric transformations
        code_sections.append(self._generate_transformations(model))

        # Elements
        code_sections.append(self._generate_elements(model))

        # Loads
        code_sections.append(self._generate_loads(model))

        # Recorders
        code_sections.append(self._generate_recorders(model))

        # Analysis
        code_sections.append(self._generate_analysis(model))

        # Output
        code_sections.append(self._generate_output_commands(model))

        # Join all sections
        full_code = "\n\n".join(code_sections)

        return full_code

    def _generate_header(self, model: StructuralModel) -> str:
        """Generate file header and imports"""
        code = f'''"""
Auto-generated OpenSeesPy Model
Structure Type: {model.structure_type}
Units: {model.units.get('length', 'unknown')} (length), {model.units.get('force', 'unknown')} (force)
"""

from openseespy.opensees import *
import numpy as np

# Clear any existing model
wipe()

print("=" * 60)
print("OpenSeesPy Structural Analysis")
print("=" * 60)
print(f"Structure: {model.structure_type}")
print(f"Nodes: {len(model.nodes)}")
print(f"Elements: {len(model.elements)}")
print("=" * 60)'''
        return code

    def _generate_model_init(self, model: StructuralModel) -> str:
        """Generate model initialization"""
        code = f'''# Model initialization
model('basic', '-ndm', {model.ndm}, '-ndf', {model.ndf})
print("\\n[1/7] Model initialized")'''
        return code

    def _generate_materials(self, model: StructuralModel) -> str:
        """Generate material definitions"""
        if not model.materials:
            return "# No materials defined"

        lines = ["# Material definitions"]

        for mat in model.materials:
            if mat.type == "steel":
                # Use Steel02 material for more realistic behavior
                # Steel02: uniaxialMaterial('Steel02', matTag, Fy, E0, b, *params)
                # Simplified: use elastic-perfectly plastic
                lines.append(
                    f"uniaxialMaterial('Elastic', {mat.id}, {mat.E * 1000})  "
                    f"# Material {mat.id}: {mat.type.upper()}, E={mat.E} ksi"
                )
            elif mat.type == "elastic":
                lines.append(
                    f"uniaxialMaterial('Elastic', {mat.id}, {mat.E * 1000})  "
                    f"# Material {mat.id}: Elastic, E={mat.E} ksi"
                )

        lines.append('print("[2/7] Materials defined")')
        return "\n".join(lines)

    def _generate_nodes(self, model: StructuralModel) -> str:
        """Generate node definitions and boundary conditions"""
        lines = ["# Node definitions"]

        # Convert units if needed (feet to inches for OpenSees)
        unit_factor = 12.0 if model.units.get('length') == 'ft' else 1.0

        for node in model.nodes:
            x = node.x * unit_factor
            y = node.y * unit_factor
            z = node.z * unit_factor if model.ndm == 3 else 0

            if model.ndm == 2:
                lines.append(f"node({node.id}, {x:.2f}, {y:.2f})")
            else:
                lines.append(f"node({node.id}, {x:.2f}, {y:.2f}, {z:.2f})")

        lines.append("")
        lines.append("# Boundary conditions")

        for node in model.nodes:
            if node.constraints and any(c == 1 for c in node.constraints):
                # Node has constraints
                constraints_str = ", ".join(str(c) for c in node.constraints)
                lines.append(f"fix({node.id}, {constraints_str})  # Node {node.id}")

        lines.append('print("[3/7] Nodes and boundary conditions defined")')
        return "\n".join(lines)

    def _generate_transformations(self, model: StructuralModel) -> str:
        """Generate geometric transformations"""
        lines = ["# Geometric transformations"]

        for transf in model.transformations:
            lines.append(
                f"geomTransf('{transf.type}', {transf.tag})  "
                f"# {transf.type} transformation"
            )

        lines.append('print("[4/7] Geometric transformations defined")')
        return "\n".join(lines)

    def _generate_elements(self, model: StructuralModel) -> str:
        """Generate element definitions"""
        lines = ["# Element definitions"]

        # Create section lookup
        section_dict = {s.name: s for s in model.sections}

        # Convert units (ksi to psf for E modulus)
        E_factor = 1000.0  # ksi to kips/in²
        unit_factor = 12.0 if model.units.get('length') == 'ft' else 1.0

        # Get material E (assume first material)
        E = model.materials[0].E * E_factor if model.materials else 29000 * E_factor

        for elem in model.elements:
            section = section_dict.get(elem.section)
            if not section:
                lines.append(f"# Warning: Section {elem.section} not found for element {elem.id}")
                continue

            i_node, j_node = elem.nodes[0], elem.nodes[1]
            A = section.A
            I = section.I

            transf_tag = elem.transf_tag or 1

            if elem.type == "elasticBeamColumn" or "beam" in elem.type.lower():
                lines.append(
                    f"element('elasticBeamColumn', {elem.id}, {i_node}, {j_node}, "
                    f"{A:.3f}, {E:.1f}, {I:.1f}, {transf_tag})  "
                    f"# {elem.section}, {elem.orientation or 'N/A'}"
                )
            elif elem.type == "truss" or "truss" in elem.type.lower():
                lines.append(
                    f"element('Truss', {elem.id}, {i_node}, {j_node}, "
                    f"{A:.3f}, 1)  # {elem.section}"
                )

        lines.append('print("[5/7] Elements defined")')
        return "\n".join(lines)

    def _generate_loads(self, model: StructuralModel) -> str:
        """Generate load definitions"""
        if not model.loads:
            return "# No loads defined"

        lines = ["# Load definitions"]
        lines.append("timeSeries('Linear', 1)")
        lines.append("pattern('Plain', 1, 1)")

        # Convert force units if needed
        force_factor = 1.0  # Assume already in kips

        for load in model.loads:
            if load.type == "point":
                # Determine direction DOF
                direction_map = {'X': 1, 'Y': 2, 'Z': 3, '1': 1, '2': 2, '3': 3}
                dof = direction_map.get(load.direction.upper(), 2)

                magnitude = load.magnitude * force_factor

                if dof == 1:
                    load_cmd = f"load({load.node}, {magnitude:.2f}, 0.0, 0.0)  # Node {load.node}, DOF {dof}"
                else:
                    load_cmd = f"load({load.node}, 0.0, {magnitude:.2f}, 0.0)  # Node {load.node}, DOF {dof}"
                lines.append(load_cmd)

        lines.append('print("[6/7] Loads defined")')
        return "\n".join(lines)

    def _generate_recorders(self, model: StructuralModel) -> str:
        """Generate recorder commands for output"""
        lines = ["# Recorders for results"]
        lines.append("recorder('Node', '-file', 'node_displacements.txt', '-time', '-node', *range(1, {}), '-dof', 1, 2, 3, 'disp')".format(len(model.nodes) + 1))
        lines.append("recorder('Node', '-file', 'node_reactions.txt', '-time', '-node', *range(1, {}), '-dof', 1, 2, 3, 'reaction')".format(len(model.nodes) + 1))
        lines.append("recorder('Element', '-file', 'element_forces.txt', '-time', '-ele', *range(1, {}), 'forces')".format(len(model.elements) + 1))
        return "\n".join(lines)

    def _generate_analysis(self, model: StructuralModel) -> str:
        """Generate analysis commands"""
        analysis = model.analysis

        lines = ["# Analysis setup"]

        # Analysis parameters
        lines.append(f"constraints('{analysis.constraints}')")
        lines.append(f"numberer('{analysis.numberer}')")
        lines.append(f"system('{analysis.system}')")
        lines.append(f"test('{analysis.test}', {analysis.tol}, {analysis.max_iter})")
        lines.append(f"algorithm('{analysis.algorithm}')")

        if analysis.type == "static":
            lines.append(f"integrator('{analysis.integrator}', 1.0)")
            lines.append("analysis('Static')")
            lines.append("")
            lines.append("# Perform analysis")
            lines.append('print("[7/7] Running static analysis...")')
            lines.append(f"ok = analyze({analysis.steps})")
            lines.append("")
            lines.append("if ok == 0:")
            lines.append(f"{self.indent}print('✓ Analysis completed successfully')")
            lines.append("else:")
            lines.append(f"{self.indent}print('✗ Analysis failed')")

        elif analysis.type == "eigenvalue":
            lines.append(f"integrator('Newmark', 0.5, 0.25)")
            lines.append("analysis('Transient')")
            lines.append("")
            lines.append("# Eigenvalue analysis")
            lines.append('print("[7/7] Running eigenvalue analysis...")')
            lines.append(f"num_modes = {analysis.num_modes}")
            lines.append("eigenValues = eigen(num_modes)")
            lines.append("")
            lines.append("# Calculate periods")
            lines.append("import math")
            lines.append("periods = [2 * math.pi / math.sqrt(lam) if lam > 0 else 0 for lam in eigenValues]")
            lines.append("")
            lines.append('print("\\nModal Analysis Results:")')
            lines.append("for i, (lam, T) in enumerate(zip(eigenValues, periods), 1):")
            lines.append(f"{self.indent}print(f'  Mode {{i}}: λ = {{lam:.4f}}, T = {{T:.4f}} sec')")

        return "\n".join(lines)

    def _generate_output_commands(self, model: StructuralModel) -> str:
        """Generate commands to display results"""
        lines = ["", "# Output results"]
        lines.append('print("\\n" + "=" * 60)')
        lines.append('print("Analysis Results")')
        lines.append('print("=" * 60)')
        lines.append("")

        # Get max displacement
        lines.append("# Maximum displacements")
        lines.append("max_disp_x = 0.0")
        lines.append("max_disp_y = 0.0")
        lines.append("max_disp_node = 0")
        lines.append("")
        lines.append(f"for node_id in range(1, {len(model.nodes) + 1}):")
        lines.append(f"{self.indent}disp = nodeDisp(node_id)")
        lines.append(f"{self.indent}if abs(disp[0]) > abs(max_disp_x):")
        lines.append(f"{self.indent}{self.indent}max_disp_x = disp[0]")
        lines.append(f"{self.indent}if abs(disp[1]) > abs(max_disp_y):")
        lines.append(f"{self.indent}{self.indent}max_disp_y = disp[1]")
        lines.append(f"{self.indent}{self.indent}max_disp_node = node_id")
        lines.append("")
        lines.append('print(f"Max displacement X: {max_disp_x:.6f} in")')
        lines.append('print(f"Max displacement Y: {max_disp_y:.6f} in")')
        lines.append('print(f"At node: {max_disp_node}")')
        lines.append("")

        # Get reactions
        lines.append("# Reactions at supports")
        lines.append('print("\\nSupport Reactions:")')
        lines.append("for node in [" + ", ".join(str(n.id) for n in model.nodes if any(c == 1 for c in n.constraints)) + "]:")
        lines.append(f"{self.indent}reactions = nodeReaction(node)")
        lines.append(f"{self.indent}print(f'  Node {{node}}: Fx={{reactions[0]:.2f}} kip, Fy={{reactions[1]:.2f}} kip, M={{reactions[2]:.2f}} kip-ft')")

        lines.append("")
        lines.append('print("\\n✓ Analysis complete. Results saved to output files.")')
        lines.append('print("=" * 60)')

        return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    from ..models.structural_json import StructuralModel, Node, Element, Material, Section, Load
    import json

    print("=" * 60)
    print("Code Translation Agent Demo")
    print("=" * 60)

    # Create a simple example model
    model = StructuralModel(
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
        materials=[
            Material(id=1, type="steel", E=29000, fy=50)
        ],
        sections=[
            Section(name="W14X90", A=26.5, I=999),
            Section(name="W21X50", A=14.7, I=984),
        ],
        elements=[
            Element(id=1, type="elasticBeamColumn", nodes=[1, 3], section="W14X90", orientation="vertical"),
            Element(id=2, type="elasticBeamColumn", nodes=[2, 4], section="W14X90", orientation="vertical"),
            Element(id=3, type="elasticBeamColumn", nodes=[3, 4], section="W21X50", orientation="horizontal"),
        ],
        loads=[
            Load(type="point", node=3, direction="Y", magnitude=-10.0),
            Load(type="point", node=4, direction="Y", magnitude=-10.0),
        ],
        analysis={
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
    )

    # Translate to OpenSeesPy code
    translator = CodeTranslationAgent()
    opensees_code = translator.translate(model)

    print("\n" + "=" * 60)
    print("Generated OpenSeesPy Code:")
    print("=" * 60)
    print(opensees_code)

    # Save to file
    output_file = "/tmp/generated_opensees_model.py"
    with open(output_file, 'w') as f:
        f.write(opensees_code)

    print("\n" + "=" * 60)
    print(f"✓ Code saved to: {output_file}")
    print("=" * 60)
