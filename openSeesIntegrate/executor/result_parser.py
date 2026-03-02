"""
Result Parser
Parses and interprets OpenSeesPy analysis results
"""

import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class AnalysisResults:
    """Structured analysis results"""
    displacements: Dict[int, Dict[str, float]]  # node_id -> {dx, dy, dz, rx, ry, rz}
    reactions: Dict[int, Dict[str, float]]  # node_id -> {Fx, Fy, Fz, Mx, My, Mz}
    element_forces: Dict[int, Dict[str, float]]  # elem_id -> forces
    max_displacement: Tuple[int, float, str]  # (node_id, value, direction)
    max_reaction: Tuple[int, float, str]  # (node_id, value, direction)
    summary: Dict[str, any]


class ResultParser:
    """
    Parser for OpenSeesPy output files and results
    """

    def __init__(self):
        """Initialize result parser"""
        pass

    def parse_from_files(
        self,
        output_files: Dict[str, Path],
        model_info: Optional[Dict] = None
    ) -> AnalysisResults:
        """
        Parse results from output files

        Args:
            output_files: Dictionary of output file paths
            model_info: Optional model information for context

        Returns:
            AnalysisResults object
        """
        displacements = {}
        reactions = {}
        element_forces = {}

        # Parse node displacements
        if 'node_displacements' in output_files:
            displacements = self._parse_node_displacements(
                output_files['node_displacements']
            )

        # Parse node reactions
        if 'node_reactions' in output_files:
            reactions = self._parse_node_reactions(
                output_files['node_reactions']
            )

        # Parse element forces
        if 'element_forces' in output_files:
            element_forces = self._parse_element_forces(
                output_files['element_forces']
            )

        # Find maximum values
        max_displacement = self._find_max_displacement(displacements)
        max_reaction = self._find_max_reaction(reactions)

        # Generate summary
        summary = self._generate_summary(
            displacements, reactions, element_forces, model_info
        )

        return AnalysisResults(
            displacements=displacements,
            reactions=reactions,
            element_forces=element_forces,
            max_displacement=max_displacement,
            max_reaction=max_reaction,
            summary=summary
        )

    def _parse_node_displacements(self, file_path: Path) -> Dict[int, Dict[str, float]]:
        """Parse node displacement file"""
        displacements = {}

        try:
            data = np.loadtxt(file_path)

            if data.ndim == 1:
                data = data.reshape(1, -1)

            # Last row has final displacements
            # Format: time, node1_dof1, node1_dof2, ..., node2_dof1, ...
            if len(data) > 0:
                last_row = data[-1]
                time = last_row[0]

                # Group by node (assuming 3 DOFs per node)
                values = last_row[1:]
                num_dofs = 3

                for i in range(0, len(values), num_dofs):
                    node_id = i // num_dofs + 1
                    displacements[node_id] = {
                        'dx': values[i] if i < len(values) else 0.0,
                        'dy': values[i+1] if i+1 < len(values) else 0.0,
                        'rz': values[i+2] if i+2 < len(values) else 0.0
                    }

        except Exception as e:
            print(f"Warning: Could not parse displacements: {e}")

        return displacements

    def _parse_node_reactions(self, file_path: Path) -> Dict[int, Dict[str, float]]:
        """Parse node reaction file"""
        reactions = {}

        try:
            data = np.loadtxt(file_path)

            if data.ndim == 1:
                data = data.reshape(1, -1)

            # Last row has final reactions
            if len(data) > 0:
                last_row = data[-1]
                values = last_row[1:]
                num_dofs = 3

                for i in range(0, len(values), num_dofs):
                    node_id = i // num_dofs + 1
                    reactions[node_id] = {
                        'Fx': values[i] if i < len(values) else 0.0,
                        'Fy': values[i+1] if i+1 < len(values) else 0.0,
                        'Mz': values[i+2] if i+2 < len(values) else 0.0
                    }

        except Exception as e:
            print(f"Warning: Could not parse reactions: {e}")

        return reactions

    def _parse_element_forces(self, file_path: Path) -> Dict[int, Dict[str, float]]:
        """Parse element force file"""
        element_forces = {}

        try:
            data = np.loadtxt(file_path)

            if data.ndim == 1:
                data = data.reshape(1, -1)

            # Last row has final forces
            if len(data) > 0:
                last_row = data[-1]
                values = last_row[1:]

                # For beam-column elements: 6 forces per element (N1, V1, M1, N2, V2, M2)
                num_forces = 6

                for i in range(0, len(values), num_forces):
                    elem_id = i // num_forces + 1
                    element_forces[elem_id] = {
                        'N1': values[i] if i < len(values) else 0.0,
                        'V1': values[i+1] if i+1 < len(values) else 0.0,
                        'M1': values[i+2] if i+2 < len(values) else 0.0,
                        'N2': values[i+3] if i+3 < len(values) else 0.0,
                        'V2': values[i+4] if i+4 < len(values) else 0.0,
                        'M2': values[i+5] if i+5 < len(values) else 0.0,
                    }

        except Exception as e:
            print(f"Warning: Could not parse element forces: {e}")

        return element_forces

    def _find_max_displacement(
        self,
        displacements: Dict[int, Dict[str, float]]
    ) -> Tuple[int, float, str]:
        """Find maximum displacement"""
        max_val = 0.0
        max_node = 0
        max_dir = ''

        for node_id, disp in displacements.items():
            for direction, value in disp.items():
                if abs(value) > abs(max_val):
                    max_val = value
                    max_node = node_id
                    max_dir = direction

        return (max_node, max_val, max_dir)

    def _find_max_reaction(
        self,
        reactions: Dict[int, Dict[str, float]]
    ) -> Tuple[int, float, str]:
        """Find maximum reaction"""
        max_val = 0.0
        max_node = 0
        max_dir = ''

        for node_id, react in reactions.items():
            for direction, value in react.items():
                if abs(value) > abs(max_val):
                    max_val = value
                    max_node = node_id
                    max_dir = direction

        return (max_node, max_val, max_dir)

    def _generate_summary(
        self,
        displacements: Dict,
        reactions: Dict,
        element_forces: Dict,
        model_info: Optional[Dict]
    ) -> Dict:
        """Generate analysis summary"""
        summary = {
            'num_nodes_analyzed': len(displacements),
            'num_supports': len(reactions),
            'num_elements_analyzed': len(element_forces)
        }

        # Calculate total reactions
        if reactions:
            total_fx = sum(r.get('Fx', 0) for r in reactions.values())
            total_fy = sum(r.get('Fy', 0) for r in reactions.values())
            total_mz = sum(r.get('Mz', 0) for r in reactions.values())

            summary['total_reactions'] = {
                'Fx': total_fx,
                'Fy': total_fy,
                'Mz': total_mz
            }

        # Calculate displacement statistics
        if displacements:
            all_disp_x = [d.get('dx', 0) for d in displacements.values()]
            all_disp_y = [d.get('dy', 0) for d in displacements.values()]

            summary['displacement_stats'] = {
                'max_horizontal': max(abs(d) for d in all_disp_x),
                'max_vertical': max(abs(d) for d in all_disp_y),
                'rms_horizontal': np.sqrt(np.mean(np.array(all_disp_x)**2)),
                'rms_vertical': np.sqrt(np.mean(np.array(all_disp_y)**2))
            }

        return summary

    def generate_natural_language_summary(
        self,
        results: AnalysisResults,
        model_info: Optional[Dict] = None
    ) -> str:
        """
        Generate natural language summary of results

        Args:
            results: Analysis results
            model_info: Optional model information

        Returns:
            Human-readable summary string
        """
        lines = []
        lines.append("=" * 60)
        lines.append("STRUCTURAL ANALYSIS RESULTS SUMMARY")
        lines.append("=" * 60)

        # Displacement summary
        if results.displacements:
            lines.append(f"\n📊 Displacements Analyzed: {len(results.displacements)} nodes")

            node_id, max_val, direction = results.max_displacement
            lines.append(f"\n   Maximum Displacement:")
            lines.append(f"   • Location: Node {node_id}")
            lines.append(f"   • Direction: {direction}")
            lines.append(f"   • Magnitude: {abs(max_val):.6f} in")

            # Drift check (if vertical displacement)
            if direction == 'dx' and model_info:
                height = model_info.get('height', 144)  # inches
                drift_ratio = abs(max_val) / height
                lines.append(f"   • Drift ratio: {drift_ratio:.4f} ({drift_ratio*100:.2f}%)")

                # ASCE 7 drift limit is typically h/400 for steel
                drift_limit = height / 400
                if abs(max_val) > drift_limit:
                    lines.append(f"   ⚠️  Exceeds drift limit ({drift_limit:.6f} in)")
                else:
                    lines.append(f"   ✓ Within drift limit ({drift_limit:.6f} in)")

        # Reaction summary
        if results.reactions:
            lines.append(f"\n⚓ Support Reactions: {len(results.reactions)} supports")

            node_id, max_val, direction = results.max_reaction
            lines.append(f"\n   Maximum Reaction:")
            lines.append(f"   • Location: Node {node_id}")
            lines.append(f"   • Component: {direction}")
            lines.append(f"   • Magnitude: {abs(max_val):.2f} {'kip' if direction.startswith('F') else 'kip-in'}")

            # Total reactions
            if 'total_reactions' in results.summary:
                total = results.summary['total_reactions']
                lines.append(f"\n   Total Reactions:")
                lines.append(f"   • ΣFx = {total['Fx']:.2f} kip (should be ≈0)")
                lines.append(f"   • ΣFy = {total['Fy']:.2f} kip")
                lines.append(f"   • ΣMz = {total['Mz']:.2f} kip-in")

        # Element forces summary
        if results.element_forces:
            lines.append(f"\n🔧 Element Forces: {len(results.element_forces)} elements analyzed")

            # Find maximum forces
            max_axial = max(
                (abs(f.get('N1', 0)), elem_id, 'N1')
                for elem_id, f in results.element_forces.items()
            )
            max_shear = max(
                (abs(f.get('V1', 0)), elem_id, 'V1')
                for elem_id, f in results.element_forces.items()
            )
            max_moment = max(
                (abs(f.get('M1', 0)), elem_id, 'M1')
                for elem_id, f in results.element_forces.items()
            )

            lines.append(f"\n   Critical Forces:")
            lines.append(f"   • Max axial: {max_axial[0]:.2f} kip (Element {max_axial[1]})")
            lines.append(f"   • Max shear: {max_shear[0]:.2f} kip (Element {max_shear[1]})")
            lines.append(f"   • Max moment: {max_moment[0]:.2f} kip-in (Element {max_moment[1]})")

        lines.append("\n" + "=" * 60)
        lines.append("✓ Analysis Summary Complete")
        lines.append("=" * 60)

        return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    import tempfile

    print("=" * 60)
    print("Result Parser Demo")
    print("=" * 60)

    # Create sample output files
    temp_dir = Path(tempfile.mkdtemp())

    # Sample displacement data (time, node1_dx, node1_dy, node1_rz, node2_dx, node2_dy, node2_rz)
    disp_data = np.array([
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.156, -0.234, 0.001]
    ])
    np.savetxt(temp_dir / 'node_displacements.txt', disp_data)

    # Sample reaction data
    react_data = np.array([
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [1.0, 0.0, 10.5, -123.4, 0.0, 9.5, 98.7]
    ])
    np.savetxt(temp_dir / 'node_reactions.txt', react_data)

    # Parse results
    parser = ResultParser()
    output_files = {
        'node_displacements': temp_dir / 'node_displacements.txt',
        'node_reactions': temp_dir / 'node_reactions.txt'
    }

    results = parser.parse_from_files(output_files)

    # Print summary
    print("\nParsed Results:")
    print(f"  Nodes with displacements: {len(results.displacements)}")
    print(f"  Support nodes: {len(results.reactions)}")
    print(f"\n  Max displacement: Node {results.max_displacement[0]}, "
          f"{results.max_displacement[2]} = {results.max_displacement[1]:.6f} in")
    print(f"  Max reaction: Node {results.max_reaction[0]}, "
          f"{results.max_reaction[2]} = {results.max_reaction[1]:.2f} kip")

    # Generate natural language summary
    print("\n" + parser.generate_natural_language_summary(results))

    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)
    print("\n✓ Demo complete")
