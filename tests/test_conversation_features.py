"""
简单的多轮对话功能验证
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import SteelDesignAgent


def test_conversation_history():
    """测试对话历史功能"""
    print("测试1: 对话历史记录")
    print("-" * 60)
    
    agent = SteelDesignAgent()
    
    # 添加几条消息
    agent.conversation_history.append({"role": "user", "content": "测试1"})
    agent.conversation_history.append({"role": "assistant", "content": "回复1"})
    agent.conversation_history.append({"role": "user", "content": "测试2"})
    
    # 验证历史
    history = agent.get_conversation_history()
    assert len(history) == 3, "对话历史应该有3条记录"
    assert history[0]["content"] == "测试1"
    assert history[1]["content"] == "回复1"
    
    print("✓ 对话历史记录功能正常")
    print()


def test_reset_conversation():
    """测试重置对话功能"""
    print("测试2: 重置对话")
    print("-" * 60)
    
    agent = SteelDesignAgent()
    
    # 添加消息
    agent.conversation_history.append({"role": "user", "content": "测试"})
    assert len(agent.conversation_history) > 0
    
    # 重置
    agent.reset_conversation()
    assert len(agent.conversation_history) == 0, "重置后对话历史应该为空"
    
    print("✓ 重置对话功能正常")
    print()


def test_system_prompt():
    """测试系统提示词"""
    print("测试3: 系统提示词")
    print("-" * 60)
    
    agent = SteelDesignAgent()
    
    # 验证系统提示词包含关键信息
    assert agent.system_prompt is not None
    assert len(agent.system_prompt) > 0
    assert "多轮对话" in agent.system_prompt
    assert "参数不完整" in agent.system_prompt
    assert "无关" in agent.system_prompt
    
    print("✓ 系统提示词包含多轮对话相关指令")
    print()


def test_enhanced_prompt_content():
    """测试增强的提示词内容"""
    print("测试4: 增强的提示词内容")
    print("-" * 60)
    
    agent = SteelDesignAgent()
    
    # 检查关键功能描述
    prompt = agent.system_prompt
    
    checks = [
        ("上下文记忆", "上下文" in prompt or "记忆" in prompt),
        ("参数补全", "参数" in prompt and "完整" in prompt),
        ("无关问题处理", "无关" in prompt),
        ("参数说明", "A" in prompt and "截面积" in prompt),
        ("典型范围", "典型" in prompt or "范围" in prompt),
    ]
    
    for name, result in checks:
        status = "✓" if result else "✗"
        print(f"  {status} {name}")
    
    all_passed = all(result for _, result in checks)
    assert all_passed, "提示词应该包含所有关键功能描述"
    
    print("\n✓ 提示词内容完整")
    print()


def main():
    """运行所有验证测试"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "多轮对话功能验证" + " " * 28 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    try:
        test_conversation_history()
        test_reset_conversation()
        test_system_prompt()
        test_enhanced_prompt_content()
        
        print("=" * 60)
        print("所有验证测试通过！")
        print("=" * 60)
        print()
        print("注意: 实际的多轮对话功能需要配置LLM API才能测试")
        print("请运行以下命令进行完整测试:")
        print("  python tests/test_multi_turn_dialogue.py")
        print("  python examples/multi_turn_demo.py")
        print()
        
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}\n")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

