"""
Complete Integrated Steel Structure Design System (v3.0)
Integrates Task 3.1 (Building Design) + Task 3.2 (Steel Strength) + Task 3.3 (Structural Analysis)
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional

from openai import OpenAI
from dotenv import load_dotenv

# Task 3.1: Building Design
from building_design import (
    parse_building_description,
    generate_blueprint,
    calculate_all_column_loads,
    optimize_column_section
)

# Task 3.2: Steel Strength Calculation
from agent.agent import SteelDesignAgent

# Task 3.3: Structural Analysis
from openSeesIntegrate.opensees_integration import OpenSeesIntegrationSystem

load_dotenv()


class CompleteIntegratedSystem:
    """
    Complete integrated system combining all three tasks:
    - Task 3.1: Building geometry and layout generation
    - Task 3.2: Steel member strength calculation (PINN)
    - Task 3.3: Structural analysis automation (OpenSeesPy)
    """

    def __init__(self):
        """Initialize complete integrated system"""
        print("\n" + "=" * 70)
        print("COMPLETE INTEGRATED STEEL STRUCTURE DESIGN SYSTEM v3.0")
        print("=" * 70)

        # Initialize OpenAI client
        api_key = os.getenv('DASHSCOPE_API_KEY') or os.getenv('OPENAI_API_KEY')
        base_url = os.getenv('LLM_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
        self.client = OpenAI(api_key=api_key, base_url=base_url)

        # Initialize Task 3.2: Steel Strength Agent
        model_path = "PINN model/normal/model_20250123_165719.pth"
        if os.path.exists(model_path):
            self.steel_agent = SteelDesignAgent(model_path=model_path)
            print("✓ Task 3.2: Steel strength agent initialized (PINN model loaded)")
        else:
            self.steel_agent = SteelDesignAgent()
            print("⚠ Task 3.2: Steel strength agent initialized (no PINN model)")

        # Initialize Task 3.3: OpenSees Integration
        self.opensees_system = OpenSeesIntegrationSystem(client=self.client)
        print("✓ Task 3.3: OpenSees integration system initialized")

        print("\n✓ Complete system ready")
        print("=" * 70)

    def complete_design_workflow(
        self,
        description: str,
        dead_load_psf: float = 50,
        live_load_psf: float = 40,
        num_floors: int = 1,
        lateral_load_kip: Optional[float] = None,
        run_structural_analysis: bool = True,
        output_dir: str = "output"
    ) -> Dict:
        """
        Complete end-to-end design workflow integrating all three tasks

        Args:
            description: Natural language building description
            dead_load_psf: Dead load (psf)
            live_load_psf: Live load (psf)
            num_floors: Number of floors
            lateral_load_kip: Optional lateral load (kip)
            run_structural_analysis: Whether to run OpenSeesPy analysis
            output_dir: Output directory

        Returns:
            Complete design report
        """
        print("\n" + "=" * 70)
        print("COMPLETE DESIGN WORKFLOW: Task 3.1 → 3.3 → 3.2")
        print("=" * 70)

        os.makedirs(output_dir, exist_ok=True)
        final_report = {}

        # ===== TASK 3.1: BUILDING DESIGN =====
        print("\n" + "-" * 70)
        print("TASK 3.1: BUILDING GEOMETRY & LAYOUT GENERATION")
        print("-" * 70)

        # Step 1: Parse building description
        print("\n[3.1.1] Parsing building description...")
        try:
            blueprint_params = parse_building_description(description, self.client)
            final_report['building_design'] = blueprint_params
            print(f"✓ Parsed {len(blueprint_params.get('rooms', []))} rooms")
        except Exception as e:
            final_report['error'] = f"Building parsing failed: {e}"
            return final_report

        # Step 2: Generate blueprint
        print("\n[3.1.2] Generating 3D blueprint...")
        try:
            blueprint_file = os.path.join(output_dir, "blueprint.svg")
            generate_blueprint(blueprint_params, blueprint_file)
            final_report['blueprint_file'] = blueprint_file
            print(f"✓ Blueprint: {blueprint_file}")
        except Exception as e:
            print(f"⚠ Blueprint generation warning: {e}")

        # Step 3: Column design (preliminary sizing)
        print("\n[3.1.3] Preliminary column design...")
        try:
            column_report = generate_column_design_report(
                blueprint_params,
                dead_load_psf,
                live_load_psf,
                num_floors
            )
            final_report['preliminary_column_design'] = column_report
            print(f"✓ Designed {column_report['summary']['total_columns']} columns")
            print(f"  Total load: {column_report['summary']['total_load']:,.0f} lbs")
        except Exception as e:
            print(f"⚠ Column design warning: {e}")
            column_report = {}

        # ===== TASK 3.3: STRUCTURAL ANALYSIS =====
        if run_structural_analysis:
            print("\n" + "-" * 70)
            print("TASK 3.3: STRUCTURAL ANALYSIS (OpenSeesPy)")
            print("-" * 70)

            try:
                print("\n[3.3.1] Converting building to structural model...")
                print("[3.3.2] Generating OpenSeesPy code...")
                print("[3.3.3] Running analysis...")

                analysis_results = self.opensees_system.analyze_from_building(
                    blueprint_params,
                    dead_load_psf=dead_load_psf,
                    live_load_psf=live_load_psf,
                    num_floors=num_floors,
                    lateral_load_kip=lateral_load_kip,
                    output_dir=os.path.join(output_dir, "opensees_analysis")
                )

                final_report['structural_analysis'] = analysis_results

                if 'error' in analysis_results:
                    print(f"⚠ Analysis warning: {analysis_results['error']}")
                else:
                    print("✓ Structural analysis complete")

                    # Extract actual forces from analysis
                    if 'analysis_results' in analysis_results:
                        element_forces = analysis_results['analysis_results'].get('element_forces', {})
                        final_report['actual_forces'] = element_forces

            except Exception as e:
                print(f"⚠ Structural analysis error: {e}")
                final_report['analysis_error'] = str(e)

        # ===== TASK 3.2: STEEL STRENGTH VERIFICATION =====
        print("\n" + "-" * 70)
        print("TASK 3.2: STEEL MEMBER STRENGTH VERIFICATION (PINN)")
        print("-" * 70)

        design_checks = []

        # Get columns to check
        if 'preliminary_column_design' in final_report:
            column_designs = final_report['preliminary_column_design'].get('column_designs', {})

            print(f"\n[3.2.1] Verifying {len(column_designs)} columns...")

            for col_name, design in list(column_designs.items())[:5]:  # Check first 5
                try:
                    # Extract parameters for PINN
                    A = design.get('area', 10)
                    section_name = design.get('type', 'W14X90')

                    # Estimate other parameters
                    from openSeesIntegrate.models.wsection_database import get_section_properties
                    section_props = get_section_properties(section_name)

                    if section_props:
                        A = section_props.A
                        I = section_props.Ix
                        c = section_props.d / 2
                    else:
                        # Fallback estimates
                        I = A * 10  # Rough estimate
                        c = (A ** 0.5)  # Rough estimate

                    # Column parameters
                    L = blueprint_params.get('building_elevation', 12) * 12  # ft to inches
                    fy = 50.0  # ksi
                    delta_o = 0.1  # inches

                    # Get actual force from analysis (if available)
                    actual_force = None
                    if 'actual_forces' in final_report:
                        # Find corresponding element
                        elem_id = int(col_name.split('_')[1]) if '_' in col_name else 1
                        forces = final_report['actual_forces'].get(elem_id, {})
                        actual_force = abs(forces.get('N1', 0))  # Axial force

                    # Calculate strength using PINN
                    query = f"Calculate column strength with A={A}, I={I}, c={c}, L={L}, fy={fy}, delta_o={delta_o}"
                    response = self.steel_agent.chat(query)

                    # Extract nominal strength from response
                    # (This is a simplified extraction - in production, parse more carefully)
                    import re
                    pn_match = re.search(r'Pn[:\s=]+([0-9.]+)', response)
                    nominal_strength = float(pn_match.group(1)) if pn_match else None

                    check = {
                        'column': col_name,
                        'section': section_name,
                        'parameters': {
                            'A': A,
                            'I': I,
                            'L': L,
                            'fy': fy
                        },
                        'nominal_strength_kip': nominal_strength,
                        'actual_force_kip': actual_force,
                        'pinn_response': response
                    }

                    # Check adequacy
                    if nominal_strength and actual_force:
                        utilization = actual_force / nominal_strength
                        check['utilization_ratio'] = utilization
                        check['is_adequate'] = utilization < 1.0

                        status = "✓ ADEQUATE" if utilization < 1.0 else "✗ INADEQUATE"
                        print(f"  {col_name} ({section_name}): {status} (D/C = {utilization:.2f})")
                    else:
                        print(f"  {col_name} ({section_name}): Calculated (Pn = {nominal_strength:.1f} kip)")

                    design_checks.append(check)

                except Exception as e:
                    print(f"  ⚠ {col_name}: Could not verify ({e})")

        final_report['steel_strength_checks'] = design_checks

        # ===== FINAL REPORT GENERATION =====
        print("\n" + "-" * 70)
        print("GENERATING FINAL REPORT")
        print("-" * 70)

        # Generate summary
        summary = self._generate_integrated_summary(final_report)
        final_report['summary'] = summary

        # Save complete report
        report_file = os.path.join(output_dir, "complete_design_report.json")
        with open(report_file, 'w') as f:
            json.dump(final_report, f, indent=2, default=str)

        print(f"\n✓ Complete report saved: {report_file}")

        # Print summary
        print("\n" + "=" * 70)
        print("DESIGN SUMMARY")
        print("=" * 70)
        print(summary)
        print("=" * 70)

        return final_report

    def _generate_integrated_summary(self, report: Dict) -> str:
        """Generate integrated summary"""
        lines = []

        # Building summary
        if 'building_design' in report:
            building = report['building_design']
            rooms = building.get('rooms', [])
            columns = building.get('columns', [])
            lines.append(f"BUILDING: {len(rooms)} rooms, {len(columns)} columns")

        # Analysis summary
        if 'structural_analysis' in report and 'error' not in report['structural_analysis']:
            analysis = report['structural_analysis']
            if 'analysis_results' in analysis:
                results = analysis['analysis_results']
                max_disp = results.get('max_displacement', {})
                lines.append(f"ANALYSIS: Max displacement = {abs(max_disp.get('value', 0)):.4f} in at Node {max_disp.get('node', 0)}")

        # Strength checks summary
        if 'steel_strength_checks' in report:
            checks = report['steel_strength_checks']
            adequate = sum(1 for c in checks if c.get('is_adequate', False))
            total = len([c for c in checks if 'is_adequate' in c])
            if total > 0:
                lines.append(f"STRENGTH: {adequate}/{total} columns adequate")

        return "\n".join(lines) if lines else "Summary not available"

    def interactive_mode(self):
        """Run in interactive mode"""
        print("\n" + "=" * 70)
        print("INTERACTIVE MODE")
        print("=" * 70)
        print("\nCommands:")
        print("  'design' - Complete design workflow (3.1 → 3.3 → 3.2)")
        print("  'example' - Show usage examples")
        print("  'quit' - Exit")
        print("-" * 70)
        print("\n💡 Tip: Type 'example' to see sample building descriptions")
        print("-" * 70)

        while True:
            try:
                command = input("\nCommand: ").strip().lower()

                if command in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break

                elif command == 'example':
                    print("\n" + "=" * 70)
                    print("USAGE EXAMPLES")
                    print("=" * 70)
                    print("\n📋 Example 1: Simple Office Building")
                    print("   Description: 'A 2-story office building with 4 rooms per floor,")
                    print("                each room 20x15 feet with central corridor'")
                    print("   Dead load: 50 psf")
                    print("   Live load: 40 psf")
                    print("   Floors: 2")
                    print()
                    print("📋 Example 2: Warehouse")
                    print("   Description: 'Simple warehouse 60x40 feet with columns every 20 feet'")
                    print("   Dead load: 30 psf (lighter roof)")
                    print("   Live load: 20 psf")
                    print("   Floors: 1")
                    print()
                    print("📋 Example 3: Residential Building")
                    print("   Description: 'Three-story apartment building, 6 units, each 25x18 feet'")
                    print("   Dead load: 60 psf")
                    print("   Live load: 50 psf")
                    print("   Floors: 3")
                    print()
                    print("💡 Tips:")
                    print("   • Describe room sizes, layout, and number of floors")
                    print("   • Mention if you want specific column spacing")
                    print("   • System will automatically select steel sections (W-shapes)")
                    print("   • Results include: blueprint, analysis, and strength verification")
                    print("=" * 70)

                elif command == 'design':
                    print("\n--- Complete Design Workflow ---")
                    print("\n📝 Example building descriptions:")
                    print("  • 'A 2-story office building with 4 rooms per floor, each 20x15 feet'")
                    print("  • 'Simple warehouse 50x30 feet with columns every 10 feet'")
                    print("  • 'Three-story residential building with 6 apartments'")
                    print()
                    description = input("Describe your building: ").strip()

                    if not description:
                        print("Please provide a building description.")
                        continue

                    # Get parameters
                    try:
                        dead_load = float(input("Dead load (psf) [default: 50]: ") or "50")
                        live_load = float(input("Live load (psf) [default: 40]: ") or "40")
                        num_floors = int(input("Number of floors [default: 1]: ") or "1")
                        run_analysis = input("Run structural analysis? (y/n) [default: y]: ").strip().lower()
                        run_analysis = run_analysis != 'n'
                    except ValueError:
                        print("Invalid input, using defaults.")
                        dead_load, live_load, num_floors, run_analysis = 50, 40, 1, True

                    # Run workflow
                    self.complete_design_workflow(
                        description,
                        dead_load_psf=dead_load,
                        live_load_psf=live_load,
                        num_floors=num_floors,
                        run_structural_analysis=run_analysis
                    )

                else:
                    print("Unknown command. Type 'design' or 'quit'.")

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Complete Integrated Steel Structure Design System v3.0"
    )
    parser.add_argument(
        '--mode',
        choices=['interactive', 'design'],
        default='interactive',
        help='Operation mode'
    )
    parser.add_argument(
        '--description',
        type=str,
        help='Building description (for design mode)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='output',
        help='Output directory'
    )
    parser.add_argument(
        '--no-analysis',
        action='store_true',
        help='Skip structural analysis (Task 3.3)'
    )

    args = parser.parse_args()

    # Initialize system
    system = CompleteIntegratedSystem()

    if args.mode == 'interactive':
        system.interactive_mode()
    elif args.mode == 'design':
        if not args.description:
            print("Error: --description required for design mode")
            return

        system.complete_design_workflow(
            args.description,
            output_dir=args.output,
            run_structural_analysis=not args.no_analysis
        )


if __name__ == "__main__":
    main()
