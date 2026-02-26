"""
Simple multi-turn dialogue functionality verification
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import SteelDesignAgent


def test_conversation_history():
    """Test conversation history functionality"""
    print("Test 1: Conversation history recording")
    print("-" * 60)
    
    agent = SteelDesignAgent()
    
    # Add a few messages
    agent.conversation_history.append({"role": "user", "content": "test1"})
    agent.conversation_history.append({"role": "assistant", "content": "reply1"})
    agent.conversation_history.append({"role": "user", "content": "test2"})
    
    # Verify history
    history = agent.get_conversation_history()
    assert len(history) == 3, "Conversation history should have 3 records"
    assert history[0]["content"] == "test1"
    assert history[1]["content"] == "reply1"
    
    print("✓ Conversation history recording functionality normal")
    print()


def test_reset_conversation():
    """Test reset conversation functionality"""
    print("Test 2: Reset conversation")
    print("-" * 60)
    
    agent = SteelDesignAgent()
    
    # Add message
    agent.conversation_history.append({"role": "user", "content": "test"})
    assert len(agent.conversation_history) > 0
    
    # Reset
    agent.reset_conversation()
    assert len(agent.conversation_history) == 0, "Conversation history should be empty after reset"
    
    print("✓ Reset conversation functionality normal")
    print()


def test_system_prompt():
    """Test system prompt"""
    print("Test 3: System prompt")
    print("-" * 60)
    
    agent = SteelDesignAgent()
    
    # Verify system prompt contains key information
    assert agent.system_prompt is not None
    assert len(agent.system_prompt) > 0
    assert "Multi-turn" in agent.system_prompt or "multi-turn" in agent.system_prompt
    assert "incomplete" in agent.system_prompt or "Incomplete" in agent.system_prompt
    assert "unrelated" in agent.system_prompt or "Unrelated" in agent.system_prompt
    
    print("✓ System prompt contains multi-turn dialogue related instructions")
    print()


def test_enhanced_prompt_content():
    """Test enhanced prompt content"""
    print("Test 4: Enhanced prompt content")
    print("-" * 60)
    
    agent = SteelDesignAgent()
    
    # Check key functionality descriptions
    prompt = agent.system_prompt
    
    checks = [
        ("Context memory", "context" in prompt.lower() or "memory" in prompt.lower()),
        ("Parameter completion", "parameter" in prompt.lower() and "complete" in prompt.lower()),
        ("Unrelated question handling", "unrelated" in prompt.lower()),
        ("Parameter description", "A" in prompt and ("Cross-sectional" in prompt or "area" in prompt)),
        ("Typical range", "typical" in prompt.lower() or "range" in prompt.lower()),
    ]
    
    for name, result in checks:
        status = "✓" if result else "✗"
        print(f"  {status} {name}")
    
    all_passed = all(result for _, result in checks)
    assert all_passed, "Prompt should contain all key functionality descriptions"
    
    print("\n✓ Prompt content complete")
    print()


def main():
    """Run all verification tests"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "Multi-turn Dialogue Verification" + " " * 14 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    try:
        test_conversation_history()
        test_reset_conversation()
        test_system_prompt()
        test_enhanced_prompt_content()
        
        print("=" * 60)
        print("All verification tests passed!")
        print("=" * 60)
        print()
        print("Note: Actual multi-turn dialogue functionality requires LLM API configuration")
        print("Please run the following commands for complete testing:")
        print("  python tests/test_multi_turn_dialogue.py")
        print("  python examples/multi_turn_demo.py")
        print()
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
    except Exception as e:
        print(f"\n✗ Error occurred: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
