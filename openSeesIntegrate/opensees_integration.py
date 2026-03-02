"""
Complete OpenSees Integration System
Integrates all agents for end-to-end structural analysis automation
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv

from .agents import GeometryAgent, CodeTranslationAgent, ModelValidationAgent
from .executor import OpenSeesPyExecutor, ResultParser
from .models import StructuralModel

load_dotenv()


class OpenSeesIntegrationSystem:
    """
    Complete system integrating all agents for automated structural analysis
    """

    def __init__(
        self,
        client: Optional[OpenAI] = None,
        model: str = "qwen-max",
        working_dir: Optional[str] = None
    ):
        """
        Initialize integration system

        Args:
            client: OpenAI client for LLM
            model: LLM model name
            working_dir: Working directory for analysis files
        """
        # Initialize LLM client
        if client is None:
            api_key = os.getenv('DASHSCOPE_API_KEY') or os.getenv('OPENAI_API_KEY')
            base_url = os.getenv('LLM_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = client

        # Initialize agents
        self.geometry_agent = GeometryAgent(client=self.client, model=model)
        self.code_translator = CodeTranslationAgent()
        self.validator = ModelValidationAgent()
        self.executor = OpenSeesPyExecutor(working_dir=working_dir)
        self.result_parser = ResultParser()

        print("✓ OpenSees Integration System initialized")
        print(f"  - LLM Model: {model}")
        print(f"  - Working directory: {self.executor.working_dir}")

    def analyze_from_description(
        self,
        description: str,
        output_dir: Optional[str] = None,
        validate: bool = True
    ) -> Dict:
        """
        Complete workflow: Natural language → Analysis results

        Args:
            description: Natural language structural description
            output_dir: Output directory for results
            validate: Whether to validate model and code

        Returns:
            Complete analysis results dictionary
        """
        print("\n" + "=" * 60)
        print("AUTOMATED STRUCTURAL ANALYSIS WORKFLOW")
        print("=" * 60)

        results = {}

        # Step 1: Geometry Agent - NL to JSON
        print("\n[Step 1/6] Converting description to structural model...")
        try:
            structural_model = self.geometry_agent.process(description)
            results['structural_model'] = structural_model.dict()
            print(f"✓ Model created: {len(structural_model.nodes)} nodes, "
                  f"{len(structural_model.elements)} elements")
        except Exception as e:
            results['error'] = f"Geometry extraction failed: {e}"
            return results

        # Step 2: Model Validation
        if validate:
            print("\n[Step 2/6] Validating structural model...")
            validation = self.validator.validate_model(structural_model)
            results['model_validation'] = {
                'is_valid': validation.is_valid,
                'errors': validation.errors,
                'warnings': validation.warnings
            }

            if not validation.is_valid:
                print("✗ Model validation failed:")
                for error in validation.errors:
                    print(f"  - {error}")
                results['error'] = "Model validation failed"
                return results

            print(f"✓ Model validated ({len(validation.warnings)} warnings)")
            if validation.warnings:
                for warning in validation.warnings[:3]:  # Show first 3
                    print(f"  ⚠ {warning}")

        # Step 3: Code Translation - JSON to OpenSeesPy
        print("\n[Step 3/6] Generating OpenSeesPy code...")
        try:
            opensees_code = self.code_translator.translate(structural_model)
            results['opensees_code'] = opensees_code
            print(f"✓ Code generated ({len(opensees_code.split(chr(10)))} lines)")
        except Exception as e:
            results['error'] = f"Code generation failed: {e}"
            return results

        # Step 4: Code Validation
        if validate:
            print("\n[Step 4/6] Validating generated code...")
            code_validation = self.validator.validate_code(opensees_code, structural_model)
            results['code_validation'] = {
                'is_valid': code_validation.is_valid,
                'errors': code_validation.errors,
                'warnings': code_validation.warnings
            }

            if not code_validation.is_valid:
                print("✗ Code validation failed:")
                for error in code_validation.errors:
                    print(f"  - {error}")
                results['error'] = "Code validation failed"
                return results

            print(f"✓ Code validated ({len(code_validation.warnings)} warnings)")

        # Step 5: Execute Analysis
        print("\n[Step 5/6] Running OpenSeesPy analysis...")
        try:
            exec_result = self.executor.execute(opensees_code)
            results['execution'] = {
                'success': exec_result['success'],
                'execution_time': exec_result['execution_time'],
                'working_dir': exec_result['working_dir']
            }

            if not exec_result['success']:
                print(f"✗ Analysis execution failed")
                print(f"  Error: {exec_result.get('error', 'Unknown')}")
                results['error'] = exec_result.get('error', 'Execution failed')
                results['execution']['stdout'] = exec_result.get('stdout', '')
                results['execution']['stderr'] = exec_result.get('stderr', '')
                return results

            print(f"✓ Analysis completed in {exec_result['execution_time']:.2f}s")

        except Exception as e:
            results['error'] = f"Execution failed: {e}"
            return results

        # Step 6: Parse Results
        print("\n[Step 6/6] Parsing and interpreting results...")
        try:
            if 'output_files' in exec_result:
                parsed_results = self.result_parser.parse_from_files(
                    exec_result['output_files'],
                    model_info={'height': max(n.y for n in structural_model.nodes)}
                )

                # Generate summary
                summary_text = self.result_parser.generate_natural_language_summary(
                    parsed_results
                )

                results['analysis_results'] = {
                    'displacements': parsed_results.displacements,
                    'reactions': parsed_results.reactions,
                    'element_forces': parsed_results.element_forces,
                    'max_displacement': {
                        'node': parsed_results.max_displacement[0],
                        'value': parsed_results.max_displacement[1],
                        'direction': parsed_results.max_displacement[2]
                    },
                    'summary': parsed_results.summary
                }
                results['summary_text'] = summary_text

                print("✓ Results parsed and interpreted")
                print(f"\n{summary_text}")

        except Exception as e:
            print(f"⚠ Warning: Could not parse results: {e}")
            results['warning'] = f"Result parsing incomplete: {e}"

        # Save results
        if output_dir:
            self._save_results(results, output_dir)

        print("\n" + "=" * 60)
        print("✓ WORKFLOW COMPLETE")
        print("=" * 60)

        return results

    def analyze_from_building(
        self,
        building_params: Dict,
        dead_load_psf: float = 50,
        live_load_psf: float = 40,
        num_floors: int = 1,
        lateral_load_kip: Optional[float] = None,
        output_dir: Optional[str] = None
    ) -> Dict:
        """
        Analyze structure from building design (Task 3.1 integration)

        Args:
            building_params: Building parameters from building_design module
            dead_load_psf: Dead load (psf)
            live_load_psf: Live load (psf)
            num_floors: Number of floors
            lateral_load_kip: Optional lateral load
            output_dir: Output directory

        Returns:
            Complete analysis results
        """
        print("\n" + "=" * 60)
        print("BUILDING-TO-ANALYSIS INTEGRATION (Task 3.1 → 3.3)")
        print("=" * 60)

        results = {}

        # Step 1: Convert building to structural model
        print("\n[Step 1/5] Converting building design to structural model...")
        try:
            structural_model = self.geometry_agent.process_from_building_design(
                building_params,
                dead_load_psf=dead_load_psf,
                live_load_psf=live_load_psf,
                num_floors=num_floors,
                lateral_load_kip=lateral_load_kip
            )
            results['structural_model'] = structural_model.dict()
            print(f"✓ Model created from building design")
            print(f"  - {len(structural_model.nodes)} nodes")
            print(f"  - {len(structural_model.elements)} elements")
            print(f"  - {len(structural_model.loads)} loads")
        except Exception as e:
            results['error'] = f"Building conversion failed: {e}"
            return results

        # Steps 2-5: Standard workflow
        return self._continue_analysis_workflow(structural_model, results, output_dir)

    def _continue_analysis_workflow(
        self,
        structural_model: StructuralModel,
        results: Dict,
        output_dir: Optional[str]
    ) -> Dict:
        """Continue analysis workflow from structural model"""

        # Validate model
        print("\n[Step 2/5] Validating model...")
        validation = self.validator.validate_model(structural_model)
        if not validation.is_valid:
            print("✗ Validation failed")
            results['error'] = "Validation failed"
            results['validation_errors'] = validation.errors
            return results
        print("✓ Model validated")

        # Generate code
        print("\n[Step 3/5] Generating OpenSeesPy code...")
        opensees_code = self.code_translator.translate(structural_model)
        results['opensees_code'] = opensees_code
        print("✓ Code generated")

        # Execute
        print("\n[Step 4/5] Running analysis...")
        exec_result = self.executor.execute(opensees_code)

        if not exec_result['success']:
            results['error'] = "Execution failed"
            results['execution'] = exec_result
            return results

        print(f"✓ Analysis completed ({exec_result['execution_time']:.2f}s)")

        # Parse results
        print("\n[Step 5/5] Parsing results...")
        if 'output_files' in exec_result:
            parsed_results = self.result_parser.parse_from_files(
                exec_result['output_files']
            )
            results['analysis_results'] = {
                'displacements': parsed_results.displacements,
                'reactions': parsed_results.reactions,
                'max_displacement': {
                    'node': parsed_results.max_displacement[0],
                    'value': parsed_results.max_displacement[1],
                    'direction': parsed_results.max_displacement[2]
                }
            }
            results['summary_text'] = self.result_parser.generate_natural_language_summary(
                parsed_results
            )
            print("✓ Results parsed")

        # Save
        if output_dir:
            self._save_results(results, output_dir)

        print("\n✓ Analysis complete")
        return results

    def _save_results(self, results: Dict, output_dir: str):
        """Save results to output directory"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save JSON results
        json_file = output_path / "analysis_results.json"
        with open(json_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n✓ Results saved to: {json_file}")

        # Save code
        if 'opensees_code' in results:
            code_file = output_path / "generated_model.py"
            with open(code_file, 'w') as f:
                f.write(results['opensees_code'])
            print(f"✓ Code saved to: {code_file}")

        # Save summary
        if 'summary_text' in results:
            summary_file = output_path / "analysis_summary.txt"
            with open(summary_file, 'w') as f:
                f.write(results['summary_text'])
            print(f"✓ Summary saved to: {summary_file}")


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("OpenSees Integration System Demo")
    print("=" * 60)

    # Example: Natural language analysis
    description = """
    Create a simple 2D steel portal frame with the following:
    - 1 story, 1 bay
    - Bay width: 20 feet
    - Story height: 12 feet
    - Column sections: W14X90
    - Beam section: W21X50
    - Fixed supports at base
    - Apply 10 kip downward load at each top node
    - Perform static analysis
    """

    system = OpenSeesIntegrationSystem()

    try:
        results = system.analyze_from_description(
            description,
            output_dir="output/opensees_analysis"
        )

        if 'error' not in results:
            print("\n✓ Analysis successful!")
        else:
            print(f"\n✗ Analysis failed: {results['error']}")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
