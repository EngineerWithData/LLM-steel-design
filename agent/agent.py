"""
LLM Agent主程序
集成OpenAI API和钢构件强度计算工具
"""

import os
import json
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
from .tools.steel_strength_tools import SteelStrengthCalculator, STEEL_STRENGTH_TOOLS

# 加载环境变量
load_dotenv()


class SteelDesignAgent:
    """钢结构设计LLM Agent"""
    
    def __init__(self, model_path: str = None, api_key: str = None, base_url: str = None, model_name: str = None):
        """
        初始化Agent
        
        Args:
            model_path: PINN模型路径
            api_key: API密钥（优先使用此参数，否则从环境变量读取）
            base_url: API基础URL（优先使用此参数，否则从环境变量读取）
            model_name: 模型名称（默认使用qwen-max）
        """
        # 初始化API配置
        self.api_key = api_key or os.getenv('DASHSCOPE_API_KEY') or os.getenv('OPENAI_API_KEY')
        self.base_url = base_url or os.getenv('LLM_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
        self.model_name = model_name or os.getenv('LLM_MODEL', 'qwen-max')
        
        if not self.api_key:
            print("警告: 未设置API密钥，请在.env文件中设置DASHSCOPE_API_KEY")
        
        # 初始化OpenAI客户端（兼容阿里云DashScope）
        try:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            ) if self.api_key else None
            
            if self.client:
                print(f"✓ LLM客户端已初始化")
                print(f"  - Base URL: {self.base_url}")
                print(f"  - Model: {self.model_name}")
        except Exception as e:
            print(f"✗ LLM客户端初始化失败: {e}")
            self.client = None
        
        # 初始化工具
        self.calculator = SteelStrengthCalculator(model_path=model_path)
        
        # 对话历史
        self.conversation_history = []
        
        # 系统提示词
        self.system_prompt = """你是一个专业的结构钢设计助手，名叫"钢构助手"。你具备以下能力：

## 核心功能

1. **钢柱强度计算**: 使用先进的PINN（物理信息神经网络）模型计算钢柱的抗压强度
2. **参数解释**: 帮助用户理解各种钢结构参数的含义
3. **设计建议**: 基于AISC规范提供专业的设计建议
4. **多轮对话**: 能够记住上下文，进行连贯的多轮对话

## 工作流程

### 当用户询问钢柱强度计算时：

1. **检查参数完整性**
   - 仔细检查用户是否提供了所有必需的参数
   - 必需参数：A（截面积）、I（惯性矩）、c（距离）、L（长度）、fy（屈服强度）、delta_o（初始缺陷）

2. **参数不完整时**
   - 友好地告诉用户缺少哪些参数
   - 清楚地说明每个参数的含义和单位
   - 可以提供典型值作为参考
   - 等待用户补充信息，不要调用工具

3. **参数完整时**
   - 调用calculate_column_strength工具进行计算
   - 用清晰、专业的语言解释结果
   - 提供设计建议

### 当用户询问与钢结构设计无关的问题时：

- 礼貌地回答用户的问题
- 如果是一般性问题（如问候、闲聊），友好地回应
- 如果是其他专业领域的问题，诚实地说明你的专长是钢结构设计
- 适时引导用户回到钢结构设计话题

### 多轮对话处理：

- 记住之前对话中提到的参数和信息
- 如果用户在后续对话中补充参数，将其与之前的信息结合
- 保持对话的连贯性和上下文理解

## 参数说明

| 参数 | 符号 | 单位 | 说明 | 典型范围 |
|------|------|------|------|----------|
| 截面积 | A | in² | 钢柱横截面积 | 5-50 |
| 惯性矩 | I | in⁴ | 截面惯性矩 | 50-500 |
| 距离 | c | in | 截面中心到边缘距离 | 2-10 |
| 长度 | L | in | 柱的有效长度 | 60-300 |
| 屈服强度 | fy | ksi | 钢材屈服强度 | 36-70 |
| 初始缺陷 | delta_o | in | 初始几何缺陷 | 0.05-0.5 |

## 回答风格

- 使用中文回答
- 保持专业但友好的语气
- 对于专业术语，适当解释
- 对于不确定的问题，诚实说明
- 鼓励用户提问和讨论

## 示例对话

**用户**: 我想计算钢柱强度
**你**: 好的！我可以帮您计算钢柱的抗压强度。请提供以下参数：
- A（截面积，单位in²）
- I（惯性矩，单位in⁴）
- c（截面中心到边缘距离，单位in）
- L（柱长度，单位in）
- fy（屈服强度，单位ksi）
- delta_o（初始缺陷，单位in）

您可以一次性提供所有参数，或者逐个告诉我。

**用户**: A=10, I=100
**你**: 好的，我已经记录了：
- 截面积 A = 10 in²
- 惯性矩 I = 100 in⁴

还需要以下参数：
- c（截面中心到边缘距离）- 通常在2-10 in之间
- L（柱长度）- 例如120 in（10英尺）
- fy（屈服强度）- 常用值为50 ksi（A992钢）
- delta_o（初始缺陷）- 通常取0.1 in

请继续提供这些参数。

记住：你的目标是帮助用户完成钢结构设计，同时保持对话的自然和友好。"""
    
    def chat(self, user_message: str) -> str:
        """
        与Agent对话
        
        Args:
            user_message: 用户消息
        
        Returns:
            Agent回复
        """
        if not self.client:
            return "错误: OpenAI API未配置，请设置OPENAI_API_KEY环境变量"
        
        # 添加用户消息到历史
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # 构建消息列表
        messages = [
            {"role": "system", "content": self.system_prompt}
        ] + self.conversation_history
        
        try:
            # 调用LLM API（兼容OpenAI和阿里云DashScope）
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=STEEL_STRENGTH_TOOLS,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            
            # 如果需要调用工具
            if tool_calls:
                # 添加助手的响应到历史
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
                
                # 执行工具调用
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # 调用相应的工具
                    if function_name == "calculate_column_strength":
                        function_response = self.calculator.calculate_column_strength(function_args)
                    elif function_name == "calculate_beam_strength":
                        function_response = self.calculator.calculate_beam_strength(function_args)
                    else:
                        function_response = {"error": "未知的工具"}
                    
                    # 添加工具响应到历史
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": json.dumps(function_response, ensure_ascii=False)
                    })
                
                # 再次调用API获取最终响应
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
                # 没有工具调用，直接返回响应
                assistant_message = response_message.content
                self.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_message
                })
                
                return assistant_message
        
        except Exception as e:
            error_msg = f"发生错误: {str(e)}"
            print(error_msg)
            return error_msg
    
    def reset_conversation(self):
        """重置对话历史"""
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """获取对话历史"""
        return self.conversation_history
    
    def load_model(self, model_path: str):
        """
        加载PINN模型
        
        Args:
            model_path: 模型路径
        """
        self.calculator = SteelStrengthCalculator(model_path=model_path)
        print(f"模型已加载: {model_path}")


def main():
    """主函数 - 命令行交互界面"""
    print("=" * 60)
    print("钢结构设计LLM Agent")
    print("=" * 60)
    print()
    
    # 检查模型路径
    default_model_path = "PINN model/normal/model_20250123_165719.pth"
    if os.path.exists(default_model_path):
        model_path = default_model_path
        print(f"✓ 找到预训练模型: {model_path}")
    else:
        model_path = None
        print("⚠ 未找到预训练模型，部分功能将不可用")
    
    # 初始化Agent
    agent = SteelDesignAgent(model_path=model_path)
    
    print()
    print("Agent已启动！输入 'quit' 或 'exit' 退出")
    print("输入 'reset' 重置对话")
    print("输入 'help' 查看帮助")
    print("-" * 60)
    print()
    
    while True:
        try:
            user_input = input("用户: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("再见！")
                break
            
            if user_input.lower() in ['reset', '重置']:
                agent.reset_conversation()
                print("对话已重置")
                continue
            
            if user_input.lower() in ['help', '帮助']:
                print(agent.calculator.get_tool_description())
                continue
            
            # 获取Agent响应
            response = agent.chat(user_input)
            print(f"\nAgent: {response}\n")
            print("-" * 60)
            print()
        
        except KeyboardInterrupt:
            print("\n\n再见！")
            break
        except Exception as e:
            print(f"\n错误: {str(e)}\n")


if __name__ == "__main__":
    main()

