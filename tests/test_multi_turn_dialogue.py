"""
Test multi-turn dialogue functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import SteelDesignAgent


def test_multi_turn_conversation():
    """Test multi-turn conversation scenario"""
    print("=" * 80)
    print("Test Scenario 1: Multi-turn Dialogue - Gradually Provide Parameters")
    print("=" * 80)
    
    # Initialize Agent
    model_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "PINN model/normal/model_20250123_165719.pth"
    )
    
    if not os.path.exists(model_path):
        print("⚠ Model file does not exist, skip this test")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("⚠ LLM client not initialized, skip this test")
        return
    
    # Simulate multi-turn conversation
    conversations = [
        "Hello, I want to calculate steel column strength",
        "Cross-sectional area is 10 square inches, moment of inertia is 100",
        "c is 5 inches, length 120 inches",
        "Yield strength 50 ksi, initial imperfection 0.1 inches",
    ]
    
    print("\nStart multi-turn conversation test:\n")
    
    for i, user_msg in enumerate(conversations, 1):
        print(f"Round {i}:")
        print(f"User: {user_msg}")
        
        response = agent.chat(user_msg)
        print(f"Agent: {response}")
        print("-" * 80)
        print()
    
    print("✓ Multi-turn conversation test completed\n")


def test_unrelated_questions():
    """Test handling of unrelated questions"""
    print("=" * 80)
    print("Test Scenario 2: Handle Unrelated Questions")
    print("=" * 80)
    
    model_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "PINN model/normal/model_20250123_165719.pth"
    )
    
    if not os.path.exists(model_path):
        print("⚠ Model file does not exist, skip this test")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("⚠ LLM client not initialized, skip this test")
        return
    
    # Test various types of questions
    test_questions = [
        "Hello, who are you?",
        "How's the weather today?",
        "Can you help me with math homework?",
        "Back to the topic, I need to calculate steel column strength",
    ]
    
    print("\nStart unrelated question test:\n")
    
    for i, question in enumerate(test_questions, 1):
        print(f"Question {i}: {question}")
        response = agent.chat(question)
        print(f"Agent: {response}")
        print("-" * 80)
        print()
    
    print("✓ Unrelated question handling test completed\n")


def test_incomplete_parameters():
    """Test handling of incomplete parameters"""
    print("=" * 80)
    print("Test Scenario 3: Guidance When Parameters Are Incomplete")
    print("=" * 80)
    
    model_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "PINN model/normal/model_20250123_165719.pth"
    )
    
    if not os.path.exists(model_path):
        print("⚠ Model file does not exist, skip this test")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("⚠ LLM client not initialized, skip this test")
        return
    
    # Test gradual parameter completion
    conversations = [
        "Calculate steel column strength, A=10",
        "I=100, c=5",
        "What other parameters do I need?",
        "L=120, fy=50, delta_o=0.1",
    ]
    
    print("\nStart parameter completion test:\n")
    
    for i, msg in enumerate(conversations, 1):
        print(f"Round {i}:")
        print(f"User: {msg}")
        response = agent.chat(msg)
        print(f"Agent: {response}")
        print("-" * 80)
        print()
    
    print("✓ Parameter completion test completed\n")


def test_context_memory():
    """Test context memory"""
    print("=" * 80)
    print("Test Scenario 4: Context Memory")
    print("=" * 80)
    
    model_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "PINN model/normal/model_20250123_165719.pth"
    )
    
    if not os.path.exists(model_path):
        print("⚠ Model file does not exist, skip this test")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("⚠ LLM client not initialized, skip this test")
        return
    
    # Test if Agent remembers previous information
    conversations = [
        "I have a steel column, cross-sectional area is 10 square inches",
        "Moment of inertia is 100",
        "Do you remember what cross-sectional area I just mentioned?",
        "OK, continue. c=5, L=120, fy=50, delta_o=0.1",
    ]
    
    print("\nStart context memory test:\n")
    
    for i, msg in enumerate(conversations, 1):
        print(f"Round {i}:")
        print(f"User: {msg}")
        response = agent.chat(msg)
        print(f"Agent: {response}")
        print("-" * 80)
        print()
    
    print("✓ Context memory test completed\n")


def test_mixed_conversation():
    """Test mixed conversation (professional + casual)"""
    print("=" * 80)
    print("Test Scenario 5: Mixed Conversation")
    print("=" * 80)
    
    model_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "PINN model/normal/model_20250123_165719.pth"
    )
    
    if not os.path.exists(model_path):
        print("⚠ Model file does not exist, skip this test")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("⚠ LLM client not initialized, skip this test")
        return
    
    # Mix professional and casual conversation
    conversations = [
        "Hello!",
        "I need to design a steel column",
        "Wait, can you explain what moment of inertia is?",
        "Got it. My parameters are: A=10, I=100, c=5, L=120, fy=50, delta_o=0.1",
        "Thanks! Is this result reliable?",
    ]
    
    print("\nStart mixed conversation test:\n")
    
    for i, msg in enumerate(conversations, 1):
        print(f"Round {i}:")
        print(f"User: {msg}")
        response = agent.chat(msg)
        print(f"Agent: {response}")
        print("-" * 80)
        print()
    
    print("✓ Mixed conversation test completed\n")


def main():
    """Run all multi-turn dialogue tests"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "Multi-turn Dialogue Functionality Test" + " " * 18 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")
    
    print("Note: These tests require LLM API key configuration to run")
    print("If API is not configured, tests will be skipped")
    print()
    
    try:
        test_multi_turn_conversation()
        input("Press Enter to continue to next test...")
        
        test_unrelated_questions()
        input("Press Enter to continue to next test...")
        
        test_incomplete_parameters()
        input("Press Enter to continue to next test...")
        
        test_context_memory()
        input("Press Enter to continue to next test...")
        
        test_mixed_conversation()
        
        print("=" * 80)
        print("All multi-turn dialogue tests completed!")
        print("=" * 80)
        print()
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted")
    except Exception as e:
        print(f"\n✗ Error occurred during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
