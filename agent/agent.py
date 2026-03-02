"""
LLM Agent Main Program
Integrating OpenAI API and Steel Component Strength Calculation Tools
"""

import os
import json
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
from .tools.steel_strength_tools import SteelStrengthCalculator, STEEL_STRENGTH_TOOLS

# Load environment variables
load_dotenv()


class SteelDesignAgent:
    """Steel Structure Design LLM Agent"""
    
    def __init__(self, model_path: str = None, api_key: str = None, base_url: str = None, model_name: str = None):
        """
        Initialize Agent
        
        Args:
            model_path: PINN model path
            api_key: API key (use this parameter first, otherwise read from environment variables)
            base_url: API base URL (use this parameter first, otherwise read from environment variables)
            model_name: Model name (default: qwen-max)
        """
        # Initialize API configuration
        self.api_key = api_key or os.getenv('DASHSCOPE_API_KEY') or os.getenv('OPENAI_API_KEY')
        self.base_url = base_url or os.getenv('LLM_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
        self.model_name = model_name or os.getenv('LLM_MODEL', 'qwen-max')
        
        if not self.api_key:
            print("Warning: API key not set. Please set DASHSCOPE_API_KEY in .env file")
        
        # Initialize OpenAI client (compatible with Alibaba Cloud DashScope)
        try:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            ) if self.api_key else None
            
            if self.client:
                print(f"✓ LLM client initialized")
                print(f"  - Base URL: {self.base_url}")
                print(f"  - Model: {self.model_name}")
        except Exception as e:
            print(f"✗ LLM client initialization failed: {e}")
            self.client = None
        
        # Initialize tools
        self.calculator = SteelStrengthCalculator(model_path=model_path)
        
        # Conversation history
        self.conversation_history = []
        
        # System prompt
        self.system_prompt = """You are a professional structural steel design assistant named "Steel Design Assistant". You have the following capabilities:

## Core Functions

1. **Steel Column Strength Calculation**: Use advanced PINN (Physics-Informed Neural Network) models to calculate the compressive strength of steel columns
2. **Building Layout Design**: Design complete buildings from natural language descriptions, generate 3D blueprints, analyze column loads, and recommend steel sections
3. **Structural Analysis**: Perform automated FEA (Finite Element Analysis) using OpenSeesPy to analyze structures, calculate displacements, forces, and perform design checks
4. **Parameter Explanation**: Help users understand the meaning of various steel structure parameters
5. **Design Recommendations**: Provide professional design recommendations based on AISC specifications
6. **Multi-turn Dialogue**: Remember context and conduct coherent multi-turn conversations

## Available Tools

1. **design_building**: For initial building design - creates layout, blueprints, and recommends column sections
2. **analyze_structure**: For detailed structural analysis - runs FEA, calculates forces/displacements, performs design checks
3. **calculate_column_strength**: For verifying specific steel column strength using PINN models

## Workflow

### When users ask about building design:

1. **Understand Requirements**
   - Ask about the building type and purpose
   - Understand room requirements and layout preferences
   - Clarify load requirements (dead load, live load, number of floors)

2. **Call design_building Tool**
   - Use the natural language description provided by the user
   - Set appropriate load values based on building type
   - Generate complete design including layout, blueprint, and column analysis

3. **Present Results**
   - Summarize the building layout (number of rooms, total area)
   - Explain the column design (number of columns, loads, recommended sections)
   - Mention the blueprint file location
   - Provide any warnings or recommendations

### When users ask about structural analysis:

1. **Understand the Structure**
   - What type of structure (frame, truss, etc.)
   - Geometry and member sizes
   - Loading conditions

2. **Call analyze_structure Tool**
   - Provide clear structural description
   - Specify loads (dead load, live load)
   - Choose analysis type (static, modal)

3. **Present Analysis Results**
   - Maximum displacements and locations
   - Critical member forces
   - Design check results (pass/fail)
   - Safety recommendations

### When users ask about steel column strength calculation:

1. **Check Parameter Completeness**
   - Carefully check if the user has provided all required parameters
   - Required parameters: A (cross-sectional area), I (moment of inertia), c (distance), L (length), fy (yield strength), delta_o (initial imperfection)

2. **When Parameters are Incomplete**
   - Kindly tell the user which parameters are missing
   - Clearly explain the meaning and unit of each parameter
   - Provide typical values as reference
   - Wait for the user to supplement information, do not call tools

3. **When Parameters are Complete**
   - Call the calculate_column_strength tool for calculation
   - Explain results in clear, professional language
   - Provide design recommendations

### When users ask questions unrelated to steel structure design:

- Politely answer the user's questions
- If it's a general question (such as greetings, small talk), respond friendly
- If it's a question from another professional field, honestly explain that your expertise is in steel structure design
- Guide users back to steel structure design topics when appropriate

### Multi-turn Dialogue Handling:

- Remember parameters and information mentioned in previous conversations
- If the user supplements parameters in subsequent conversations, combine them with previous information
- Maintain conversation coherence and context understanding

## Parameter Description

| Parameter | Symbol | Unit | Description | Typical Range |
|-----------|--------|------|-------------|---------------|
| Cross-sectional Area | A | in² | Steel column cross-sectional area | 5-50 |
| Moment of Inertia | I | in⁴ | Section moment of inertia | 50-500 |
| Distance | c | in | Distance from section center to edge | 2-10 |
| Length | L | in | Effective length of column | 60-300 |
| Yield Strength | fy | ksi | Steel yield strength | 36-70 |
| Initial Imperfection | delta_o | in | Initial geometric imperfection | 0.05-0.5 |

## Response Style

- Respond in English
- Maintain a professional but friendly tone
- Explain technical terms appropriately
- Be honest about uncertain questions
- Encourage users to ask questions and discuss

## Example Dialogue

**User**: I want to calculate steel column strength
**You**: Great! I can help you calculate the compressive strength of a steel column. Please provide the following parameters:
- A (cross-sectional area, unit: in²)
- I (moment of inertia, unit: in⁴)
- c (distance from section center to edge, unit: in)
- L (column length, unit: in)
- fy (yield strength, unit: ksi)
- delta_o (initial imperfection, unit: in)

You can provide all parameters at once, or tell me one by one.

**User**: A=10, I=100
**You**: Okay, I've recorded:
- Cross-sectional area A = 10 in²
- Moment of inertia I = 100 in⁴

Still need the following parameters:
- c (distance from section center to edge) - typically between 2-10 in
- L (column length) - for example, 120 in (10 feet)
- fy (yield strength) - common value is 50 ksi (A992 steel)
- delta_o (initial imperfection) - typically 0.1 in

Please continue to provide these parameters.

Remember: Your goal is to help users complete steel structure design while keeping the conversation natural and friendly."""
    
    def chat(self, user_message: str) -> str:
        """
        Chat with Agent
        
        Args:
            user_message: User message
        
        Returns:
            Agent response
        """
        if not self.client:
            return "Error: OpenAI API not configured. Please set OPENAI_API_KEY environment variable"
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Build message list
        messages = [
            {"role": "system", "content": self.system_prompt}
        ] + self.conversation_history
        
        try:
            # Call LLM API (compatible with OpenAI and Alibaba Cloud DashScope)
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=STEEL_STRENGTH_TOOLS,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            
            # If tool call is needed
            if tool_calls:
                # Add assistant response to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response_message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": tc.type,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        } for tc in tool_calls
                    ]
                })
                
                # Execute tool call
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Call corresponding tool
                    if function_name == "calculate_column_strength":
                        function_response = self.calculator.calculate_column_strength(function_args)
                    elif function_name == "calculate_beam_strength":
                        function_response = self.calculator.calculate_beam_strength(function_args)
                    elif function_name == "design_building":
                        function_response = self.calculator.design_building(function_args)
                    elif function_name == "analyze_structure":
                        function_response = self.calculator.analyze_structure(function_args)
                    else:
                        function_response = {"error": "Unknown tool"}
                    
                    # Add tool response to history
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": json.dumps(function_response, ensure_ascii=False)
                    })
                
                # Call API again to get final response
                second_response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": self.system_prompt}
                    ] + self.conversation_history
                )
                
                final_message = second_response.choices[0].message.content
                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_message
                })
                
                return final_message
            
            else:
                # No tool call, return response directly
                assistant_message = response_message.content
                self.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_message
                })
                
                return assistant_message
        
        except Exception as e:
            error_msg = f"Error occurred: {str(e)}"
            print(error_msg)
            return error_msg
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history"""
        return self.conversation_history
    
    def load_model(self, model_path: str):
        """
        Load PINN model
        
        Args:
            model_path: Model path
        """
        self.calculator = SteelStrengthCalculator(model_path=model_path)
        print(f"Model loaded: {model_path}")


def main():
    """Main function - Command line interactive interface"""
    print("=" * 60)
    print("Steel Structure Design LLM Agent")
    print("=" * 60)
    print()
    
    # Check model path
    default_model_path = "PINN model/normal/model_20250123_165719.pth"
    if os.path.exists(default_model_path):
        model_path = default_model_path
        print(f"✓ Found pre-trained model: {model_path}")
    else:
        model_path = None
        print("⚠ Pre-trained model not found, some features will be unavailable")
    
    # Initialize Agent
    agent = SteelDesignAgent(model_path=model_path)
    
    print()
    print("Agent started! Enter 'quit' or 'exit' to exit")
    print("Enter 'reset' to reset conversation")
    print("Enter 'help' to view help")
    print("-" * 60)
    print()
    
    while True:
        try:
            user_input = input("User: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
            
            if user_input.lower() == 'reset':
                agent.reset_conversation()
                print("Conversation reset")
                continue
            
            if user_input.lower() == 'help':
                print(agent.calculator.get_tool_description())
                continue
            
            # Get Agent response
            response = agent.chat(user_input)
            print(f"\nAgent: {response}\n")
            print("-" * 60)
            print()
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}\n")


if __name__ == "__main__":
    main()
