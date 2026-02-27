"""
Integrated Steel Structure Design System
Combines building layout generation, blueprint visualization, column analysis, and steel strength calculation
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.agent import SteelDesignAgent
from building_design import (
    parse_building_description,
    generate_blueprint,
    calculate_all_column_loads,
    optimize_column_section,
    generate_column_design_report
)
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class IntegratedDesignSystem:
    """Integrated system for complete building and steel structure design."""
    
    def __init__(self):
        """Initialize the integrated design system."""
        # Initialize steel design agent
        model_path = "PINN model/normal/model_20250123_165719.pth"
        if os.path.exists(model_path):
            self.steel_agent = SteelDesignAgent(model_path=model_path)
            print("✓ Steel design agent initialized")
        else:
            self.steel_agent = SteelDesignAgent()
            print("⚠ Steel design agent initialized without PINN model")
        
        # Initialize OpenAI client for building parser
        api_key = os.getenv('DASHSCOPE_API_KEY') or os.getenv('OPENAI_API_KEY')
        base_url = os.getenv('LLM_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        
        print("✓ Integrated design system ready")
    
    def design_building(
        self,
        description: str,
        dead_load_psf: float = 50,
        live_load_psf: float = 40,
        num_floors: int = 1,
        output_dir: str = "output"
    ) -> dict:
        """
        Complete building design workflow.
        
        Args:
            description: Natural language building description
            dead_load_psf: Dead load in pounds per square foot
            live_load_psf: Live load in pounds per square foot
            num_floors: Number of floors
            output_dir: Output directory for generated files
        
        Returns:
            Complete design report
        """
        print("\n" + "="*60)
        print("INTEGRATED STEEL STRUCTURE DESIGN SYSTEM")
        print("="*60)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Step 1: Parse building description
        print("\n[Step 1/4] Parsing building description...")
        try:
            blueprint_params = parse_building_description(description, self.client)
            print(f"✓ Parsed {len(blueprint_params.get('rooms', []))} rooms")
        except Exception as e:
            print(f"✗ Error parsing description: {e}")
            return {"error": str(e)}
        
        # Step 2: Generate blueprint visualization
        print("\n[Step 2/4] Generating 3D blueprint...")
        try:
            blueprint_file = os.path.join(output_dir, "blueprint.svg")
            generate_blueprint(blueprint_params, blueprint_file)
            print(f"✓ Blueprint saved to: {blueprint_file}")
        except Exception as e:
            print(f"⚠ Warning: Could not generate blueprint: {e}")
            blueprint_file = None
        
        # Step 3: Analyze column loads and design
        print("\n[Step 3/4] Analyzing column loads and designing sections...")
        try:
            column_report = generate_column_design_report(
                blueprint_params,
                dead_load_psf,
                live_load_psf,
                num_floors
            )
            print(f"✓ Analyzed {column_report['summary']['total_columns']} columns")
            print(f"  Total load: {column_report['summary']['total_load']:,.0f} lbs")
            print(f"  Total steel weight: {column_report['summary']['total_steel_weight']:,.0f} lbs")
        except Exception as e:
            print(f"✗ Error in column analysis: {e}")
            column_report = {"error": str(e)}
        
        # Step 4: Detailed steel member strength calculation (using PINN model)
        print("\n[Step 4/4] Calculating detailed steel member strengths...")
        steel_calculations = []
        
        if 'column_designs' in column_report:
            for col_name, design in list(column_report['column_designs'].items())[:3]:  # Sample first 3
                try:
                    # Extract parameters for PINN model
                    area = design.get('area', 10)  # in²
                    
                    # Estimate other parameters based on W-section
                    # For W-sections, typical I ≈ A * d²/12 where d ≈ sqrt(A)*2
                    estimated_depth = (area ** 0.5) * 2
                    I = area * (estimated_depth ** 2) / 12
                    c = estimated_depth / 2
                    L = blueprint_params.get('building_elevation', 10) * 12  # Convert ft to inches
                    fy = design.get('fy', 50)  # ksi
                    delta_o = 0.1  # inches (typical initial imperfection)
                    
                    print(f"\n  Calculating strength for {col_name} ({design['type']})...")
                    print(f"    Parameters: A={area:.1f} in², I={I:.1f} in⁴, L={L:.1f} in")
                    
                    # Use steel agent to calculate strength
                    query = f"Calculate column strength with A={area}, I={I}, c={c}, L={L}, fy={fy}, delta_o={delta_o}"
                    response = self.steel_agent.chat(query)
                    
                    steel_calculations.append({
                        "column": col_name,
                        "section": design['type'],
                        "parameters": {
                            "A": area,
                            "I": I,
                            "c": c,
                            "L": L,
                            "fy": fy,
                            "delta_o": delta_o
                        },
                        "pinn_analysis": response
                    })
                    
                except Exception as e:
                    print(f"  ⚠ Could not calculate for {col_name}: {e}")
        
        # Compile final report
        final_report = {
            "building_description": description,
            "blueprint_params": blueprint_params,
            "blueprint_file": blueprint_file,
            "column_analysis": column_report,
            "steel_strength_calculations": steel_calculations,
            "design_parameters": {
                "dead_load_psf": dead_load_psf,
                "live_load_psf": live_load_psf,
                "num_floors": num_floors
            }
        }
        
        # Save report to file
        import json
        report_file = os.path.join(output_dir, "design_report.json")
        with open(report_file, 'w') as f:
            json.dump(final_report, f, indent=2, default=str)
        print(f"\n✓ Complete design report saved to: {report_file}")
        
        return final_report
    
    def interactive_mode(self):
        """Run in interactive mode."""
        print("\n" + "="*60)
        print("INTEGRATED STEEL STRUCTURE DESIGN SYSTEM")
        print("Interactive Mode")
        print("="*60)
        print("\nCommands:")
        print("  'design' - Start building design workflow")
        print("  'steel' - Steel column strength calculation")
        print("  'quit' - Exit")
        print("-"*60)
        
        while True:
            try:
                command = input("\nCommand: ").strip().lower()
                
                if command in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                elif command == 'design':
                    print("\n--- Building Design Workflow ---")
                    description = input("Describe your building: ").strip()
                    
                    if not description:
                        print("Please provide a building description.")
                        continue
                    
                    # Get optional parameters
                    try:
                        dead_load = float(input("Dead load (psf) [default: 50]: ") or "50")
                        live_load = float(input("Live load (psf) [default: 40]: ") or "40")
                        num_floors = int(input("Number of floors [default: 1]: ") or "1")
                    except ValueError:
                        print("Invalid input, using defaults.")
                        dead_load, live_load, num_floors = 50, 40, 1
                    
                    # Run design
                    self.design_building(
                        description,
                        dead_load_psf=dead_load,
                        live_load_psf=live_load,
                        num_floors=num_floors
                    )
                
                elif command == 'steel':
                    print("\n--- Steel Column Strength Calculation ---")
                    print("Enter parameters or type 'help' for guidance.")
                    
                    query = input("Your query: ").strip()
                    
                    if query.lower() == 'help':
                        print("\nExample queries:")
                        print("  - Calculate column strength with A=10, I=100, c=5, L=120, fy=50, delta_o=0.1")
                        print("  - I have a W8x31 column, what's its strength?")
                        print("  - What parameters do I need?")
                        continue
                    
                    response = self.steel_agent.chat(query)
                    print(f"\nAgent: {response}")
                
                else:
                    print("Unknown command. Type 'design', 'steel', or 'quit'.")
            
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Integrated Steel Structure Design System"
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
    
    args = parser.parse_args()
    
    # Initialize system
    system = IntegratedDesignSystem()
    
    if args.mode == 'interactive':
        system.interactive_mode()
    elif args.mode == 'design':
        if not args.description:
            print("Error: --description required for design mode")
            return
        
        system.design_building(args.description, output_dir=args.output)


if __name__ == "__main__":
    main()

