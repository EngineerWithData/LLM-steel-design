"""
Complete Integrated Steel Design System (v3.0)
Combines Building Design (Task 3.1), Steel Strength (Task 3.2), and Structural Analysis (Task 3.3)

This is the main entry point for the complete integrated system.
"""

import os
import sys
import json
import argparse
from typing import Dict, Any, Optional
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from building_design import (
        parse_building_description,
        generate_blueprint,
        calculate_all_column_loads,
        optimize_column_section
    )
    BUILDING_DESIGN_AVAILABLE = True
except ImportError as e:
    BUILDING_DESIGN_AVAILABLE = False
    print(f"⚠ Building design module not available: {e}")

try:
    from openSeesIntegrate.opensees_integration import OpenSeesIntegrationSystem
    OPENSEES_AVAILABLE = True
except ImportError as e:
    OPENSEES_AVAILABLE = False
    print(f"⚠ OpenSees integration module not available: {e}")

try:
    from agent.agent import SteelDesignAgent
    PINN_AGENT_AVAILABLE = True
except ImportError as e:
    PINN_AGENT_AVAILABLE = False
    print(f"⚠ PINN Agent module not available: {e}")


class CompleteIntegratedSystem:
    """Complete integrated steel design system"""

    def __init__(self, pinn_model_path: str = None):
        """
        Initialize the complete integrated system

        Args:
            pinn_model_path: Path to PINN model (default: PINN model/normal/model_20250123_165719.pth)
        """
        self.pinn_model_path = pinn_model_path or "PINN model/normal/model_20250123_165719.pth"

        # Initialize subsystems
        if OPENSEES_AVAILABLE:
            self.opensees_system = OpenSeesIntegrationSystem()
        else:
            self.opensees_system = None

        if PINN_AGENT_AVAILABLE and os.path.exists(self.pinn_model_path):
            self.pinn_agent = SteelDesignAgent(model_path=self.pinn_model_path)
        else:
            self.pinn_agent = None

    def complete_design_workflow(
        self,
        description: str,
        dead_load_psf: float = 50,
        live_load_psf: float = 40,
        num_floors: int = 1,
        lateral_load_kip: float = 0.0,
        run_structural_analysis: bool = True,
        output_dir: str = "output"
    ) -> Dict[str, Any]:
        """
        Complete design workflow from description to analysis

        Args:
            description: Building description in natural language
            dead_load_psf: Dead load in psf
            live_load_psf: Live load in psf
            num_floors: Number of floors
            lateral_load_kip: Lateral load in kip
            run_structural_analysis: Whether to run structural analysis
            output_dir: Output directory

        Returns:
            Complete design results
        """
        result = {
            'success': False,
            'building_design': None,
            'structural_analysis': None,
            'strength_verification': None
        }

        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Step 1: Building Design (Task 3.1)
        if BUILDING_DESIGN_AVAILABLE:
            print("\n" + "=" * 60)
            print("STEP 1: Building Design (Task 3.1)")
            print("=" * 60)

            try:
                # Parse building description
                building = parse_building_description(description)
                print(f"✓ Building layout generated: {len(building.floors)} floors, {len(building.rooms)} rooms")

                # Generate blueprint
                blueprint_path = os.path.join(output_dir, "blueprint.svg")
                generate_blueprint(building, save_path=blueprint_path)
                print(f"✓ Blueprint saved to: {blueprint_path}")

                # Calculate column loads
                column_loads = calculate_all_column_loads(
                    building,
                    dead_load_psf=dead_load_psf,
                    live_load_psf=live_load_psf,
                    num_floors=num_floors
                )
                print(f"✓ Column loads calculated for {len(column_loads)} columns")

                # Optimize column sections
                column_sections = {}
                for col_id, col_load in column_loads.items():
                    section = optimize_column_section(col_load)
                    column_sections[col_id] = {
                        'section': section,
                        'load': col_load
                    }
                print(f"✓ Column sections optimized")

                result['building_design'] = {
                    'building': building.dict() if hasattr(building, 'dict') else str(building),
                    'column_loads': column_loads,
                    'column_sections': column_sections,
                    'blueprint_path': blueprint_path
                }

            except Exception as e:
                print(f"✗ Building design failed: {e}")
                result['error'] = f"Building design error: {e}"
                return result

        # Step 2: Structural Analysis (Task 3.3)
        if run_structural_analysis and OPENSEES_AVAILABLE and self.opensees_system:
            print("\n" + "=" * 60)
            print("STEP 2: Structural Analysis (Task 3.3)")
            print("=" * 60)

            try:
                analysis_result = self.opensees_system.analyze_from_description(
                    description=description,
                    output_dir=os.path.join(output_dir, "opensees_analysis")
                )

                if 'error' not in analysis_result:
                    print("✓ Structural analysis completed")
                    result['structural_analysis'] = analysis_result
                else:
                    print(f"✗ Structural analysis failed: {analysis_result['error']}")
                    result['structural_analysis'] = {'error': analysis_result['error']}

            except Exception as e:
                print(f"✗ Structural analysis error: {e}")
                result['structural_analysis'] = {'error': str(e)}

        # Step 3: Strength Verification (Task 3.2)
        # This would be called for specific members identified in the analysis
        # For now, we'll skip this step in automated workflow

        # Save complete results
        result['success'] = True
        report_path = os.path.join(output_dir, "complete_design_report.json")
        with open(report_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"\n✓ Complete design report saved to: {report_path}")

        return result


def interactive_mode():
    """Interactive mode for complete design workflow"""
    print("\n" + "=" * 70)
    print("STEEL DESIGN COMPLETE SYSTEM - INTERACTIVE MODE")
    print("=" * 70)
    print("\nThis system integrates:")
    print("  • Task 3.1: Building Design (natural language → layout)")
    print("  • Task 3.2: Steel Strength Verification (PINN models)")
    print("  • Task 3.3: Structural Analysis (OpenSeesPy integration)")
    print("\n" + "=" * 70)

    system = CompleteIntegratedSystem()

    print("\n📝 Building Description")
    print("-" * 70)
    print("Example: 'A 2-story office with 4 rooms per floor, each 20x15 feet'")
    description = input("\nDescribe your building: ").strip()

    if not description:
        print("❌ No description provided. Exiting.")
        return

    # Get load parameters
    try:
        dead_load = float(input("\nDead load (psf) [default: 50]: ") or "50")
        live_load = float(input("Live load (psf) [default: 40]: ") or "40")
        num_floors = int(input("Number of floors [default: 1]: ") or "1")

        run_analysis = input("\nRun structural analysis? (y/n) [default: y]: ").strip().lower()
        run_analysis = run_analysis != 'n'

    except ValueError as e:
        print(f"❌ Invalid input: {e}")
        return

    # Run complete workflow
    print("\n" + "=" * 70)
    print("RUNNING COMPLETE DESIGN WORKFLOW")
    print("=" * 70)

    result = system.complete_design_workflow(
        description=description,
        dead_load_psf=dead_load,
        live_load_psf=live_load,
        num_floors=num_floors,
        run_structural_analysis=run_analysis,
        output_dir="output"
    )

    print("\n" + "=" * 70)
    if result.get('success'):
        print("✅ DESIGN WORKFLOW COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print("\nGenerated outputs:")
        if result.get('building_design'):
            print(f"  📐 Blueprint: {result['building_design'].get('blueprint_path')}")
        if result.get('structural_analysis'):
            print(f"  📊 Analysis results: output/opensees_analysis/")
        print(f"  📄 Complete report: output/complete_design_report.json")
    else:
        print("❌ DESIGN WORKFLOW FAILED")
        print("=" * 70)
        if 'error' in result:
            print(f"\nError: {result['error']}")

    print("\n" + "=" * 70)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Complete Integrated Steel Design System (v3.0)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (recommended for beginners)
  python integrated_design.py --mode interactive

  # Quick example workflow
  python examples/examples_quickstart.py

  # Chat with design agent
  python -m agent.agent

For more information, see README.md
        """
    )

    parser.add_argument(
        '--mode',
        choices=['interactive', 'agent'],
        default='interactive',
        help='Operating mode (default: interactive)'
    )

    args = parser.parse_args()

    if args.mode == 'interactive':
        interactive_mode()
    elif args.mode == 'agent':
        # Launch the conversational agent
        from agent.agent import main as agent_main
        agent_main()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
