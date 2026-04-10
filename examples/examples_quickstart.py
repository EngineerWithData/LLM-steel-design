"""
Quick-start examples for the integrated system.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integrated_design import CompleteIntegratedSystem


def example_1_simple_office():
    """Example 1: Simple office building"""
    print("\n" + "=" * 70)
    print("Example 1: Simple office building")
    print("=" * 70)

    system = CompleteIntegratedSystem()

    description = """
    Design a small office building with the following:
    - Single story
    - 4 rooms arranged in a 2x2 grid
    - Each room is 20 feet x 15 feet
    - Central corridor connecting rooms
    - Standard office loads
    """

    result = system.complete_design_workflow(
        description=description,
        dead_load_psf=50,
        live_load_psf=40,
        num_floors=1,
        run_structural_analysis=True,
        output_dir="output/example_1_office"
    )

    if 'error' not in result:
        print("\nExample 1 completed.")
        print(f"Output directory: output/example_1_office/")
    else:
        print(f"\nExample 1 failed: {result['error']}")


def example_2_multi_story_frame():
    """Example 2: Multi-story steel frame"""
    print("\n" + "=" * 70)
    print("Example 2: Multi-story steel frame")
    print("=" * 70)

    system = CompleteIntegratedSystem()

    description = """
    Create a 2-story commercial building:
    - 2 stories, each 12 feet high
    - 3 bays, each 25 feet wide
    - Use W14X90 columns on exterior
    - Use W14X120 columns in interior
    - W24X68 beams
    - Fixed base connections
    - Include lateral load capacity
    """

    result = system.complete_design_workflow(
        description=description,
        dead_load_psf=60,
        live_load_psf=50,
        num_floors=2,
        lateral_load_kip=15.0,  # 15 kip lateral load
        run_structural_analysis=True,
        output_dir="output/example_2_multistory"
    )

    if 'error' not in result:
        print("\nExample 2 completed.")
        print(f"Output directory: output/example_2_multistory/")
    else:
        print(f"\nExample 2 failed: {result['error']}")


def example_3_opensees_only():
    """Example 3: Direct OpenSeesPy analysis (Task 3.3 only)"""
    print("\n" + "=" * 70)
    print("Example 3: Direct structural analysis")
    print("=" * 70)

    from openSeesIntegrate.opensees_integration import OpenSeesIntegrationSystem

    system = OpenSeesIntegrationSystem()

    description = """
    Analyze a simple portal frame:
    - 1 bay, 20 feet wide
    - 1 story, 12 feet tall
    - W14X90 columns
    - W21X50 beam
    - Fixed supports at base
    - 10 kip downward load at each top node
    - Static analysis
    """

    result = system.analyze_from_description(
        description=description,
        output_dir="output/example_3_portal"
    )

    if 'error' not in result:
        print("\nExample 3 completed.")
        print(f"Output directory: output/example_3_portal/")

        # Print key results
        if 'analysis_results' in result:
            max_disp = result['analysis_results'].get('max_displacement', {})
            print(f"\nKey results:")
            print(f"  Max displacement: {abs(max_disp.get('value', 0)):.6f} in")
            print(f"  At node: {max_disp.get('node', 0)}")
    else:
        print(f"\nExample 3 failed: {result['error']}")


def run_all_examples():
    """Run all examples"""
    print("Running all examples")
    print("This demonstrates the integrated system.")

    try:
        # Example 1: Simple office
        example_1_simple_office()

        # Example 2: Multi-story
        # example_2_multi_story_frame()  # Commented out - takes longer

        # Example 3: Direct analysis
        example_3_opensees_only()

        print("\n" + "=" * 70)
        print("All examples completed.")
        print("=" * 70)
        print("\nGenerated outputs:")
        print("  - output/example_1_office/")
        print("  - output/example_3_portal/")
        print("\nEach directory contains:")
        print("  - complete_design_report.json - Complete results")
        print("  - blueprint.svg - Building visualization")
        print("  - opensees_analysis/ - Analysis files and results")
        print("  - generated_model.py - OpenSeesPy code")

    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import sys

    print("\n" + "=" * 70)
    print("Integrated system quick-start examples")
    print("=" * 70)
    print("\nThis script demonstrates the integrated system:")
    print("  Task 3.1: Building Design")
    print("  Task 3.2: Steel Strength Calculation (PINN)")
    print("  Task 3.3: Structural Analysis (OpenSeesPy)")
    print("\n" + "=" * 70)

    # Check if user wants to run a specific example
    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        if example_num == "1":
            example_1_simple_office()
        elif example_num == "2":
            example_2_multi_story_frame()
        elif example_num == "3":
            example_3_opensees_only()
        else:
            print(f"Unknown example: {example_num}")
            print("Usage: python examples_quickstart.py [1|2|3]")
    else:
        # Run selected examples
        run_all_examples()

    print("\n" + "=" * 70)
    print("To run a specific example:")
    print("  python examples_quickstart.py 1  # Simple office")
    print("  python examples_quickstart.py 2  # Multi-story")
    print("  python examples_quickstart.py 3  # Direct analysis")
    print("=" * 70)
