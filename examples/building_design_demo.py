"""
Building Design via Agent Demo
Demonstrates how to use building design features through the steel design agent
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.agent import SteelDesignAgent


def demo_building_design_via_agent():
    """Demonstrate building design through agent conversation"""
    
    print("="*70)
    print("Building Design via Steel Design Agent Demo")
    print("="*70)
    print()
    
    # Initialize agent
    model_path = "PINN model/normal/model_20250123_165719.pth"
    if os.path.exists(model_path):
        agent = SteelDesignAgent(model_path=model_path)
    else:
        agent = SteelDesignAgent()
    
    print("Agent initialized successfully!")
    print()
    
    # Demo conversations
    conversations = [
        {
            "title": "Example 1: Simple Building Design Request",
            "query": "I need to design a small office building with 4 rooms, each 20x15 feet, with a corridor connecting them. Can you help?"
        },
        {
            "title": "Example 2: Detailed Building Design",
            "query": "Design a building with 3 offices (each 20x15 feet), 1 conference room (30x20 feet), and a corridor. The building will be 2 floors, with dead load 60 psf and live load 50 psf."
        },
        {
            "title": "Example 3: Residential Building",
            "query": "I want to design a residential building with a living room (25x20 feet), 3 bedrooms (each 15x12 feet), kitchen (15x12 feet), and 2 bathrooms (each 8x6 feet). Connect them with a corridor."
        }
    ]
    
    for i, conv in enumerate(conversations, 1):
        print(f"\n{'='*70}")
        print(f"{conv['title']}")
        print(f"{'='*70}\n")
        
        print(f"User: {conv['query']}\n")
        
        # Get agent response
        response = agent.chat(conv['query'])
        
        print(f"Agent: {response}\n")
        
        # Reset conversation for next example
        if i < len(conversations):
            agent.reset_conversation()
            print("\n[Conversation reset for next example]\n")
    
    print("\n" + "="*70)
    print("Demo completed!")
    print("="*70)
    print("\nNote: The agent will automatically call the design_building tool")
    print("when it detects building design requests in the conversation.")
    print("\nGenerated files will be saved to the 'output/' directory:")
    print("  - output/blueprint.svg (3D blueprint visualization)")
    print("  - Complete design data in the agent's response")


def demo_mixed_conversation():
    """Demonstrate mixed conversation with both building design and column calculation"""
    
    print("\n\n" + "="*70)
    print("Mixed Conversation Demo")
    print("="*70)
    print()
    
    model_path = "PINN model/normal/model_20250123_165719.pth"
    if os.path.exists(model_path):
        agent = SteelDesignAgent(model_path=model_path)
    else:
        agent = SteelDesignAgent()
    
    # Multi-turn conversation mixing building design and column calculation
    queries = [
        "Hello! I need help with a building project.",
        "First, can you design a building with 4 rooms, each 20x15 feet?",
        "Great! Now I want to verify the strength of one of the columns. Can you calculate the strength for a column with A=17.6, I=341.7, c=4, L=120, fy=50, delta_o=0.1?",
        "Perfect! Can you compare this with a larger section, say A=26.5, I=495, c=5, L=120, fy=50, delta_o=0.1?"
    ]
    
    for query in queries:
        print(f"User: {query}\n")
        response = agent.chat(query)
        print(f"Agent: {response}\n")
        print("-"*70 + "\n")
    
    print("="*70)
    print("Mixed conversation demo completed!")
    print("="*70)


if __name__ == "__main__":
    print("\n" + "🏗️ " * 20)
    print("\nBuilding Design Integration Demo")
    print("Now you can design buildings through the steel design agent!")
    print("\n" + "🏗️ " * 20 + "\n")
    
    # Run demos
    demo_building_design_via_agent()
    
    # Uncomment to run mixed conversation demo
    # demo_mixed_conversation()
    
    print("\n\n" + "="*70)
    print("How to Use in Interactive Mode:")
    print("="*70)
    print("""
1. Start the agent:
   $ ./start_agent.sh
   
2. Ask for building design:
   User: Design a building with 4 rooms, each 20x15 feet
   
3. The agent will automatically:
   - Parse your description
   - Generate room layout
   - Create 3D blueprint (saved to output/blueprint.svg)
   - Analyze column loads
   - Recommend steel sections
   - Return complete design report

4. You can also mix building design with column calculations:
   User: Design a building with 4 rooms
   Agent: [Designs building]
   User: Now calculate the strength of column with A=10, I=100...
   Agent: [Calculates strength]
""")

