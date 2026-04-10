"""
Multi-turn dialogue demo for the steel design agent.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import SteelDesignAgent
import time


def print_separator():
    """Print separator line"""
    print("\n" + "=" * 80 + "\n")


def demo_scenario_1():
    """Demo Scenario 1: Gradually provide parameters"""
    print("Scenario 1: Gradually provide parameters")
    print_separator()
    
    model_path = "PINN model/normal/model_20250123_165719.pth"
    if not os.path.exists(model_path):
        print("Model file not found.")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("API key configuration is required to run this demo.")
        print("Set DASHSCOPE_API_KEY in .env.")
        return
    
    print("This scenario demonstrates how Agent guides users to gradually provide complete parameters\n")
    
    conversations = [
        ("User", "Hello, I want to calculate steel column strength"),
        ("User", "Cross-sectional area is 10 square inches"),
        ("User", "Moment of inertia 100, c is 5 inches"),
        ("User", "Length 120 inches, yield strength 50 ksi, initial imperfection 0.1 inches"),
    ]
    
    for role, message in conversations:
        print(f"{role}: {message}")
        if role == "User":
            response = agent.chat(message)
            print(f"\nAgent: {response}")
            print_separator()
            time.sleep(1)


def demo_scenario_2():
    """Demo Scenario 2: Handle unrelated questions"""
    print("Scenario 2: Handle unrelated questions")
    print_separator()
    
    model_path = "PINN model/normal/model_20250123_165719.pth"
    if not os.path.exists(model_path):
        print("Model file not found.")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("API key configuration is required.")
        return
    
    print("This scenario demonstrates how Agent handles questions unrelated to steel structure design\n")
    
    conversations = [
        ("User", "Hello, who are you?"),
        ("User", "How's the weather today?"),
        ("User", "OK, back to the topic. I need to calculate steel column strength"),
        ("User", "A=10, I=100, c=5, L=120, fy=50, delta_o=0.1"),
    ]
    
    for role, message in conversations:
        print(f"{role}: {message}")
        if role == "User":
            response = agent.chat(message)
            print(f"\nAgent: {response}")
            print_separator()
            time.sleep(1)


def demo_scenario_3():
    """Demo Scenario 3: Ask for missing parameters"""
    print("Scenario 3: Ask for missing parameters")
    print_separator()
    
    model_path = "PINN model/normal/model_20250123_165719.pth"
    if not os.path.exists(model_path):
        print("Model file not found.")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("API key configuration is required.")
        return
    
    print("This scenario demonstrates how Agent identifies missing parameters and proactively asks\n")
    
    conversations = [
        ("User", "Calculate steel column strength: A=10, I=100"),
        ("User", "What other parameters do I need?"),
        ("User", "c=5, L=120"),
        ("User", "fy=50, delta_o=0.1"),
    ]
    
    for role, message in conversations:
        print(f"{role}: {message}")
        if role == "User":
            response = agent.chat(message)
            print(f"\nAgent: {response}")
            print_separator()
            time.sleep(1)


def demo_scenario_4():
    """Demo Scenario 4: Context memory"""
    print("Scenario 4: Context memory")
    print_separator()
    
    model_path = "PINN model/normal/model_20250123_165719.pth"
    if not os.path.exists(model_path):
        print("Model file not found.")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("API key configuration is required.")
        return
    
    print("This scenario demonstrates how Agent remembers information from previous conversations\n")
    
    conversations = [
        ("User", "I have a W8x31 steel column, cross-sectional area 9.13 square inches"),
        ("User", "Do you remember what cross-sectional area I just mentioned?"),
        ("User", "OK, continue. I=110, c=4, L=120, fy=50, delta_o=0.1"),
    ]
    
    for role, message in conversations:
        print(f"{role}: {message}")
        if role == "User":
            response = agent.chat(message)
            print(f"\nAgent: {response}")
            print_separator()
            time.sleep(1)


def interactive_demo():
    """Interactive demo"""
    print("Interactive demo")
    print_separator()
    
    model_path = "PINN model/normal/model_20250123_165719.pth"
    if not os.path.exists(model_path):
        print("Model file not found.")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("API key configuration is required.")
        return
    
    print("Chat with the agent.")
    print("Type 'quit' to exit or 'reset' to clear the conversation.")
    print_separator()
    
    while True:
        try:
            user_input = input("User: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit']:
                print("Session ended.")
                break
            
            if user_input.lower() == 'reset':
                agent.reset_conversation()
                print("Conversation reset.")
                continue
            
            response = agent.chat(user_input)
            print(f"\nAgent: {response}")
            print_separator()
            
        except KeyboardInterrupt:
            print("\n\nSession ended.")
            break


def main():
    """Main function"""
    print("Steel Structure Design Agent - Multi-turn Dialogue Demo")
    print_separator()
    
    print("This demo includes:")
    print("  1. Gradually provide parameters")
    print("  2. Handle unrelated questions")
    print("  3. Proactively ask for missing parameters")
    print("  4. Context memory capability")
    print("  5. Interactive demo")
    print()
    
    print("LLM API key configuration is required to run this demo.")
    print()
    
    while True:
        print("Select a demo scenario:")
        print("  1 - Scenario 1: Gradually provide parameters")
        print("  2 - Scenario 2: Handle unrelated questions")
        print("  3 - Scenario 3: Proactively ask for missing parameters")
        print("  4 - Scenario 4: Context memory capability")
        print("  5 - Interactive demo")
        print("  0 - Exit")
        print()
        
        choice = input("Enter an option (0-5): ").strip()
        
        if choice == '0':
            print("Goodbye!")
            break
        elif choice == '1':
            demo_scenario_1()
        elif choice == '2':
            demo_scenario_2()
        elif choice == '3':
            demo_scenario_3()
        elif choice == '4':
            demo_scenario_4()
        elif choice == '5':
            interactive_demo()
        else:
            print("Invalid option. Please try again.")
        
        print()


if __name__ == "__main__":
    main()
