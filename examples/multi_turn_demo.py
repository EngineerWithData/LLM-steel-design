"""
多轮对话演示脚本
展示Agent如何处理不完整信息和无关问题
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import SteelDesignAgent
import time


def print_separator():
    """打印分隔线"""
    print("\n" + "=" * 80 + "\n")


def simulate_typing(text, delay=0.03):
    """模拟打字效果"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def demo_scenario_1():
    """演示场景1: 逐步提供参数"""
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "场景1: 逐步提供参数" + " " * 36 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    model_path = "PINN model/normal/model_20250123_165719.pth"
    if not os.path.exists(model_path):
        print("⚠ 模型文件不存在")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("⚠ 需要配置API密钥才能运行此演示")
        print("请在.env文件中设置DASHSCOPE_API_KEY")
        return
    
    print("这个场景展示了Agent如何引导用户逐步提供完整的参数\n")
    
    conversations = [
        ("用户", "你好，我想计算钢柱强度"),
        ("用户", "截面积是10平方英寸"),
        ("用户", "惯性矩100，c是5英寸"),
        ("用户", "长度120英寸，屈服强度50ksi，初始缺陷0.1英寸"),
    ]
    
    for role, message in conversations:
        print(f"{role}: {message}")
        if role == "用户":
            response = agent.chat(message)
            print(f"\nAgent: {response}")
            print_separator()
            time.sleep(1)


def demo_scenario_2():
    """演示场景2: 处理无关问题"""
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "场景2: 处理无关问题" + " " * 36 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    model_path = "PINN model/normal/model_20250123_165719.pth"
    if not os.path.exists(model_path):
        print("⚠ 模型文件不存在")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("⚠ 需要配置API密钥")
        return
    
    print("这个场景展示了Agent如何处理与钢结构设计无关的问题\n")
    
    conversations = [
        ("用户", "你好，你是谁？"),
        ("用户", "今天天气怎么样？"),
        ("用户", "好的，回到正题。我需要计算钢柱强度"),
        ("用户", "A=10, I=100, c=5, L=120, fy=50, delta_o=0.1"),
    ]
    
    for role, message in conversations:
        print(f"{role}: {message}")
        if role == "用户":
            response = agent.chat(message)
            print(f"\nAgent: {response}")
            print_separator()
            time.sleep(1)


def demo_scenario_3():
    """演示场景3: 询问缺失参数"""
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "场景3: 主动询问缺失参数" + " " * 32 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    model_path = "PINN model/normal/model_20250123_165719.pth"
    if not os.path.exists(model_path):
        print("⚠ 模型文件不存在")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("⚠ 需要配置API密钥")
        return
    
    print("这个场景展示了Agent如何识别缺失的参数并主动询问\n")
    
    conversations = [
        ("用户", "计算钢柱强度：A=10, I=100"),
        ("用户", "还需要什么参数？"),
        ("用户", "c=5, L=120"),
        ("用户", "fy=50, delta_o=0.1"),
    ]
    
    for role, message in conversations:
        print(f"{role}: {message}")
        if role == "用户":
            response = agent.chat(message)
            print(f"\nAgent: {response}")
            print_separator()
            time.sleep(1)


def demo_scenario_4():
    """演示场景4: 上下文记忆"""
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "场景4: 上下文记忆能力" + " " * 34 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    model_path = "PINN model/normal/model_20250123_165719.pth"
    if not os.path.exists(model_path):
        print("⚠ 模型文件不存在")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("⚠ 需要配置API密钥")
        return
    
    print("这个场景展示了Agent如何记住之前对话中的信息\n")
    
    conversations = [
        ("用户", "我有一个W8x31的钢柱，截面积9.13平方英寸"),
        ("用户", "你记得我刚才说的截面积是多少吗？"),
        ("用户", "好的，继续。I=110, c=4, L=120, fy=50, delta_o=0.1"),
    ]
    
    for role, message in conversations:
        print(f"{role}: {message}")
        if role == "用户":
            response = agent.chat(message)
            print(f"\nAgent: {response}")
            print_separator()
            time.sleep(1)


def interactive_demo():
    """交互式演示"""
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "交互式演示模式" + " " * 40 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    model_path = "PINN model/normal/model_20250123_165719.pth"
    if not os.path.exists(model_path):
        print("⚠ 模型文件不存在")
        return
    
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("⚠ 需要配置API密钥")
        return
    
    print("现在您可以与Agent自由对话")
    print("输入 'quit' 退出，输入 'reset' 重置对话")
    print_separator()
    
    while True:
        try:
            user_input = input("用户: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("演示结束！")
                break
            
            if user_input.lower() in ['reset', '重置']:
                agent.reset_conversation()
                print("对话已重置")
                continue
            
            response = agent.chat(user_input)
            print(f"\nAgent: {response}")
            print_separator()
            
        except KeyboardInterrupt:
            print("\n\n演示结束！")
            break


def main():
    """主函数"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "钢结构设计Agent - 多轮对话演示" + " " * 28 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    print("本演示展示Agent的多轮对话能力：")
    print("  1. 逐步提供参数")
    print("  2. 处理无关问题")
    print("  3. 主动询问缺失参数")
    print("  4. 上下文记忆能力")
    print("  5. 交互式演示")
    print()
    
    print("注意: 需要配置LLM API密钥才能运行演示")
    print()
    
    while True:
        print("请选择演示场景:")
        print("  1 - 场景1: 逐步提供参数")
        print("  2 - 场景2: 处理无关问题")
        print("  3 - 场景3: 主动询问缺失参数")
        print("  4 - 场景4: 上下文记忆能力")
        print("  5 - 交互式演示")
        print("  0 - 退出")
        print()
        
        choice = input("请输入选项 (0-5): ").strip()
        
        if choice == '0':
            print("再见！")
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
            print("无效选项，请重新选择")
        
        print()


if __name__ == "__main__":
    main()

