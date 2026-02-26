"""
测试多轮对话功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import SteelDesignAgent


def test_multi_turn_conversation():
    """测试多轮对话场景"""
    print("=" * 80)
    print("测试场景1: 多轮对话 - 逐步提供参数")
    print("=" * 80)
    
    # 初始化Agent
    model_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "PINN model/normal/model_20250123_165719.pth"
    )
    
    if not os.path.exists(model_path):
        print("⚠ Model file does not exist，Skip this test")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("⚠ LLM客户端Not initialized，Skip this test")
        return
    
    # 模拟多轮对话
    conversations = [
        "你好，我想Calculate钢柱强度",
        "Cross-sectional area是10square inches，Moment of inertia是100",
        "c是5inches，Length120inches",
        "Yield strength50ksi，Initial imperfection0.1inches",
    ]
    
    print("\n开始多轮对话测试:\n")
    
    for i, user_msg in enumerate(conversations, 1):
        print(f"第{i}轮对话:")
        print(f"用户: {user_msg}")
        
        response = agent.chat(user_msg)
        print(f"Agent: {response}")
        print("-" * 80)
        print()
    
    print("✓ 多轮对话测试完成\n")


def test_unrelated_questions():
    """测试无关问题处理"""
    print("=" * 80)
    print("测试场景2: 处理无关问题")
    print("=" * 80)
    
    model_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "PINN model/normal/model_20250123_165719.pth"
    )
    
    if not os.path.exists(model_path):
        print("⚠ Model file does not exist，Skip this test")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("⚠ LLM客户端Not initialized，Skip this test")
        return
    
    # 测试各种类型的问题
    test_questions = [
        "你好，你是谁？",
        "今天天气怎么样？",
        "你能帮我做数学题吗？",
        "回到正题，我需要Calculate钢柱强度",
    ]
    
    print("\n开始无关问题测试:\n")
    
    for i, question in enumerate(test_questions, 1):
        print(f"问题{i}: {question}")
        response = agent.chat(question)
        print(f"Agent: {response}")
        print("-" * 80)
        print()
    
    print("✓ 无关问题处理测试完成\n")


def test_incomplete_parameters():
    """测试参数不完整的处理"""
    print("=" * 80)
    print("测试场景3: 参数不完整时的引导")
    print("=" * 80)
    
    model_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "PINN model/normal/model_20250123_165719.pth"
    )
    
    if not os.path.exists(model_path):
        print("⚠ Model file does not exist，Skip this test")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("⚠ LLM客户端Not initialized，Skip this test")
        return
    
    # 测试参数逐步补充
    conversations = [
        "Calculate钢柱强度，A=10",
        "I=100, c=5",
        "还需要什么参数？",
        "L=120, fy=50, delta_o=0.1",
    ]
    
    print("\n开始参数补充测试:\n")
    
    for i, msg in enumerate(conversations, 1):
        print(f"第{i}轮:")
        print(f"用户: {msg}")
        response = agent.chat(msg)
        print(f"Agent: {response}")
        print("-" * 80)
        print()
    
    print("✓ 参数补充测试完成\n")


def test_context_memory():
    """测试上下文记忆"""
    print("=" * 80)
    print("测试场景4: 上下文记忆")
    print("=" * 80)
    
    model_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "PINN model/normal/model_20250123_165719.pth"
    )
    
    if not os.path.exists(model_path):
        print("⚠ Model file does not exist，Skip this test")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("⚠ LLM客户端Not initialized，Skip this test")
        return
    
    # Test Agent是否记住之前的信息
    conversations = [
        "我有一个钢柱，Cross-sectional area10square inches",
        "Moment of inertia是100",
        "你记得我刚才说的Cross-sectional area是多少吗？",
        "好的，继续。c=5, L=120, fy=50, delta_o=0.1",
    ]
    
    print("\n开始上下文记忆测试:\n")
    
    for i, msg in enumerate(conversations, 1):
        print(f"第{i}轮:")
        print(f"用户: {msg}")
        response = agent.chat(msg)
        print(f"Agent: {response}")
        print("-" * 80)
        print()
    
    print("✓ 上下文记忆测试完成\n")


def test_mixed_conversation():
    """测试混合对话（专业+闲聊）"""
    print("=" * 80)
    print("测试场景5: 混合对话")
    print("=" * 80)
    
    model_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "PINN model/normal/model_20250123_165719.pth"
    )
    
    if not os.path.exists(model_path):
        print("⚠ Model file does not exist，Skip this test")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("⚠ LLM客户端Not initialized，Skip this test")
        return
    
    # 混合专业和闲聊
    conversations = [
        "你好！",
        "我需要设计一个钢柱",
        "等等，你能解释一下什么是Moment of inertia吗？",
        "明白了。那我的参数是：A=10, I=100, c=5, L=120, fy=50, delta_o=0.1",
        "谢谢！这个结果可靠吗？",
    ]
    
    print("\n开始混合对话测试:\n")
    
    for i, msg in enumerate(conversations, 1):
        print(f"第{i}轮:")
        print(f"用户: {msg}")
        response = agent.chat(msg)
        print(f"Agent: {response}")
        print("-" * 80)
        print()
    
    print("✓ 混合对话测试完成\n")


def main():
    """运行所有多轮对话测试"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "多轮对话功能测试" + " " * 38 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")
    
    print("注意: 这些测试需要配置LLM API密钥才能运行")
    print("如果未配置API，测试将被跳过")
    print()
    
    try:
        test_multi_turn_conversation()
        input("按Enter继续下一个测试...")
        
        test_unrelated_questions()
        input("按Enter继续下一个测试...")
        
        test_incomplete_parameters()
        input("按Enter继续下一个测试...")
        
        test_context_memory()
        input("按Enter继续下一个测试...")
        
        test_mixed_conversation()
        
        print("=" * 80)
        print("所有多轮对话测试完成！")
        print("=" * 80)
        print()
        
    except KeyboardInterrupt:
        print("\n\n测试已中断")
    except Exception as e:
        print(f"\n✗ Error occurred during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

