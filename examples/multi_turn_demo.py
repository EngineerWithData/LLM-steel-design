"""
Multi-turn Dialogue Demo Script
Demonstrates how Agent handles incomplete information and unrelated questions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import SteelDesignAgent
import time


def print_separator():
    """Print separator line"""
    print("\n" + "=" * 80 + "\n")


def simulate_typing(text, delay=0.03):
    """Simulate typing effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def demo_scenario_1():
    """Demo Scenario 1: Gradually provide parameters"""
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "Scenario 1: Gradually Provide Parameters" + " " * 16 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    model_path = "PINN model/normal/model_20250123_165719.pth"
    if not os.path.exists(model_path):
        print("⚠ Model file does not exist")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("⚠ API key configuration required to run this demo")
        print("Please set DASHSCOPE_API_KEY in .env file")
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
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "Scenario 2: Handle Unrelated Questions" + " " * 18 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    model_path = "PINN model/normal/model_20250123_165719.pth"
    if not os.path.exists(model_path):
        print("⚠ Model file does not exist")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("⚠ API key configuration required")
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
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "Scenario 3: Proactively Ask for Missing Parameters" + " " * 6 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    model_path = "PINN model/normal/model_20250123_165719.pth"
    if not os.path.exists(model_path):
        print("⚠ Model file does not exist")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("⚠ API key configuration required")
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
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "Scenario 4: Context Memory Capability" + " " * 19 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    model_path = "PINN model/normal/model_20250123_165719.pth"
    if not os.path.exists(model_path):
        print("⚠ Model file does not exist")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("⚠ API key configuration required")
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
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "Interactive Demo Mode" + " " * 36 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    model_path = "PINN model/normal/model_20250123_165719.pth"
    if not os.path.exists(model_path):
        print("⚠ Model file does not exist")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("⚠ API key configuration required")
        return
    
    print("Now you can freely chat with Agent")
    print("Type 'quit' to exit, type 'reset' to reset conversation")
    print_separator()
    
    while True:
        try:
            user_input = input("User: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit']:
                print("Demo ended!")
                break
            
            if user_input.lower() == 'reset':
                agent.reset_conversation()
                print("Conversation reset")
                continue
            
            response = agent.chat(user_input)
            print(f"\nAgent: {response}")
            print_separator()
            
        except KeyboardInterrupt:
            print("\n\nDemo ended!")
            break


def main():
    """Main function"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "Steel Structure Design Agent - Multi-turn Dialogue Demo" + " " * 6 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    print("This demo showcases Agent's multi-turn dialogue capabilities:")
    print("  1. Gradually provide parameters")
    print("  2. Handle unrelated questions")
    print("  3. Proactively ask for missing parameters")
    print("  4. Context memory capability")
    print("  5. Interactive demo")
    print()
    
    print("Note: LLM API key configuration required to run demo")
    print()
    
    while True:
        print("Please select demo scenario:")
        print("  1 - Scenario 1: Gradually provide parameters")
        print("  2 - Scenario 2: Handle unrelated questions")
        print("  3 - Scenario 3: Proactively ask for missing parameters")
        print("  4 - Scenario 4: Context memory capability")
        print("  5 - Interactive demo")
        print("  0 - Exit")
        print()
        
        choice = input("Please enter option (0-5): ").strip()
        
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
            print("Invalid option, please select again")
        
        print()


if __name__ == "__main__":
    main()
