"""
Steel Component Strength Calculation Tools
Tool functions provided for LLM Agent
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.pinn_predictor import PINNPredictor
from typing import Dict, Any, List
import json

# Import building design modules
try:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from building_design import (
        parse_building_description,
        generate_blueprint,
        calculate_all_column_loads,
        optimize_column_section,
        generate_column_design_report
    )
    BUILDING_DESIGN_AVAILABLE = True
except ImportError:
    BUILDING_DESIGN_AVAILABLE = False
    print("Warning: Building design module not available")


class SteelStrengthCalculator:
    """Steel Component Strength Calculator Tool Class"""
    
    def __init__(self, model_path: str = None):
        """
        Initialize calculator
        
        Args:
            model_path: PINN model path
        """
        self.predictor = PINNPredictor(model_path=model_path)
        self.model_loaded = model_path is not None
    
    def calculate_column_strength(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate steel column compressive strength
        
        Args:
            params: Steel column parameter dictionary
        
        Returns:
            Calculation result
        """
        if not self.model_loaded:
            return {
                'success': False,
                'error': 'Model not loaded, please load PINN model first'
            }
        
        # Parameter mapping and unit conversion
        input_params = self._parse_column_params(params)
        
        if 'error' in input_params:
            return {
                'success': False,
                'error': input_params['error']
            }
        
        # Call PINN model for prediction
        result = self.predictor.predict(input_params)
        
        if result['status'] == 'success':
            return {
                'success': True,
                'component_type': 'column',
                'nominal_strength_Pn': result['Pn'],
                'theoretical_strength': result['Pn_theory'],
                'prediction_ratio': result['ratio'],
                'unit': 'kip',
                'input_parameters': input_params,
                'message': 'Steel column strength calculation successful'
            }
        else:
            return {
                'success': False,
                'error': result['message']
            }
    
    def calculate_beam_strength(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate steel beam flexural strength（Reserved interface）
        
        Args:
            params: Steel beam parameter dictionary
        
        Returns:
            Calculation result
        """
        return {
            'success': False,
            'error': 'Steel beam strength calculation feature is under development, stay tuned'
        }
    
    def _parse_column_params(self, params: Dict[str, Any]) -> Dict[str, float]:
        """
        Parse and validate steel column parameters
        
        Args:
            params: Original parameter dictionary
        
        Returns:
            Standardized parameter dictionary
        """
        try:
            # Required parameters
            required_params = {
                'A': ['A', 'area', 'Cross-sectional area', 'cross_sectional_area'],
                'I': ['I', 'inertia', 'Moment of inertia', 'moment_of_inertia'],
                'c': ['c', 'distance', 'Distance', 'distance_to_edge'],
                'L': ['L', 'length', 'Length', 'column_length'],
                'fy': ['fy', 'yield_strength', 'Yield strength', 'yield_stress'],
                'delta_o': ['delta_o', 'delta', 'imperfection', 'Initial imperfection', 'initial_imperfection']
            }
            
            parsed = {}
            
            for standard_key, possible_keys in required_params.items():
                value = None
                for key in possible_keys:
                    if key in params:
                        value = float(params[key])
                        break
                
                if value is None:
                    return {'error': f'Missing required parameter: {standard_key} (Available key names: {", ".join(possible_keys)})'}
                
                parsed[standard_key] = value
            
            # Parameter validation
            if parsed['A'] <= 0:
                return {'error': 'Cross-sectional area must be greater than 0'}
            if parsed['I'] <= 0:
                return {'error': 'Moment of inertia must be greater than 0'}
            if parsed['L'] <= 0:
                return {'error': 'Column length must be greater than 0'}
            if parsed['fy'] <= 0:
                return {'error': 'Yield strength must be greater than 0'}
            
            return parsed
            
        except ValueError as e:
            return {'error': f'Parameter type error: {str(e)}'}
        except Exception as e:
            return {'error': f'Parameter parsing failed: {str(e)}'}
    
    def design_building(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Design complete building from natural language description
        
        Args:
            params: Building design parameters
                - description: Natural language building description
                - dead_load_psf: Dead load in psf (default: 50)
                - live_load_psf: Live load in psf (default: 40)
                - num_floors: Number of floors (default: 1)
                - output_file: Blueprint output filename (optional)
        
        Returns:
            Complete design report including layout, blueprint, and column analysis
        """
        if not BUILDING_DESIGN_AVAILABLE:
            return {
                'success': False,
                'error': 'Building design module not available. Please install required dependencies.'
            }
        
        try:
            description = params.get('description', '')
            if not description:
                return {
                    'success': False,
                    'error': 'Building description is required'
                }
            
            dead_load_psf = params.get('dead_load_psf', 50)
            live_load_psf = params.get('live_load_psf', 40)
            num_floors = params.get('num_floors', 1)
            output_file = params.get('output_file', 'output/blueprint.svg')
            
            # Step 1: Parse building description
            from openai import OpenAI
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv('DASHSCOPE_API_KEY') or os.getenv('OPENAI_API_KEY')
            base_url = os.getenv('LLM_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
            client = OpenAI(api_key=api_key, base_url=base_url)
            
            blueprint_params = parse_building_description(description, client)
            
            # Step 2: Generate blueprint
            os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else 'output', exist_ok=True)
            generate_blueprint(blueprint_params, output_file)
            
            # Step 3: Analyze columns
            column_report = generate_column_design_report(
                blueprint_params,
                dead_load_psf,
                live_load_psf,
                num_floors
            )
            
            return {
                'success': True,
                'building_description': description,
                'blueprint_file': output_file,
                'num_rooms': len(blueprint_params.get('rooms', [])),
                'num_columns': column_report['summary']['total_columns'],
                'total_load': column_report['summary']['total_load'],
                'total_steel_weight': column_report['summary']['total_steel_weight'],
                'column_designs': column_report['column_designs'],
                'warnings': column_report.get('warnings', []),
                'message': f'Building design completed. Blueprint saved to {output_file}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Building design failed: {str(e)}'
            }
    
    def get_tool_description(self) -> str:
        """Get tool description (for LLM understanding)"""
        building_tools = ""
        if BUILDING_DESIGN_AVAILABLE:
            building_tools = """
3. Design complete building from description (design_building)
   - Input: Natural language building description
   - Output: Building layout, 3D blueprint, column analysis
"""
        
        return f"""
Steel Component Strength Calculation Tools

Features:
1. Calculate steel column compressive strength (calculate_column_strength)
2. Calculate steel beam flexural strength (calculate_beam_strength) - Under development{building_tools}

Steel column parameter description:
- A (area): Cross-sectional area, unit in²
- I (inertia): Moment of inertia, unit in⁴
- c (distance): Distance from section center to edge, unit in
- L (length): Column length, unit in
- fy (yield_strength): Yield strength, unit ksi
- delta_o (imperfection): Initial imperfection, unit in

Return result:
- nominal_strength_Pn: Nominal compressive strength, unit kip
- theoretical_strength: Theoretical strength (Perry-Robertson formula), unit kip
- prediction_ratio: Ratio of predicted to theoretical value

Example call:
{{
    "A": 10.0,
    "I": 100.0,
    "c": 5.0,
    "L": 120.0,
    "fy": 50.0,
    "delta_o": 0.1
}}
"""


# For LangChain/OpenAI Function Calling tool definition
STEEL_STRENGTH_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate_column_strength",
            "description": "Calculate steel column compressive strength. Use pre-trained PINN (Physics-Informed Neural Network) model for prediction.",
            "parameters": {
                "type": "object",
                "properties": {
                    "A": {
                        "type": "number",
                        "description": "Cross-sectional area, unit: in² (square inches)"
                    },
                    "I": {
                        "type": "number",
                        "description": "Moment of inertia, unit: in⁴ (inches to the fourth power)"
                    },
                    "c": {
                        "type": "number",
                        "description": "Distance from section center to edge, unit: in (inches)"
                    },
                    "L": {
                        "type": "number",
                        "description": "Column length, unit: in (inches)"
                    },
                    "fy": {
                        "type": "number",
                        "description": "Yield strength, unit: ksi (kips per square inch)"
                    },
                    "delta_o": {
                        "type": "number",
                        "description": "Initial imperfection, unit: in (inches)"
                    }
                },
                "required": ["A", "I", "c", "L", "fy", "delta_o"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_beam_strength",
            "description": "Calculate steel beam flexural strength (feature under development)",
            "parameters": {
                "type": "object",
                "properties": {
                    "section": {
                        "type": "string",
                        "description": "Section type"
                    }
                },
                "required": ["section"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "design_building",
            "description": "Design a complete building from natural language description. Generates room layout, 3D blueprint visualization, calculates column loads, and recommends steel sections. Perfect for initial building design and structural planning.",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Natural language description of the building. Example: 'I need an office building with 4 rooms, each 20x15 feet, with a corridor connecting all rooms'"
                    },
                    "dead_load_psf": {
                        "type": "number",
                        "description": "Dead load in pounds per square foot (psf). Typical values: 40-80 psf. Default: 50 psf"
                    },
                    "live_load_psf": {
                        "type": "number",
                        "description": "Live load in pounds per square foot (psf). Typical values: 40-100 psf (residential: 40, office: 50, classroom: 100). Default: 40 psf"
                    },
                    "num_floors": {
                        "type": "integer",
                        "description": "Number of floors. Default: 1"
                    },
                    "output_file": {
                        "type": "string",
                        "description": "Output filename for the blueprint SVG. Default: 'output/blueprint.svg'"
                    }
                },
                "required": ["description"]
            }
        }
    }
]


if __name__ == "__main__":
    # Test tool
    calculator = SteelStrengthCalculator()
    
    # Test steel column calculation
    test_params = {
        'A': 10.0,
        'I': 100.0,
        'c': 5.0,
        'L': 120.0,
        'fy': 50.0,
        'delta_o': 0.1
    }
    
    result = calculator.calculate_column_strength(test_params)
    print("Steel column strength calculation result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

