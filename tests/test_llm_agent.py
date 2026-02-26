"""
测试LLM Agent功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from agent import SteelDesignAgent


class TestSteelDesignAgent:
    """LLM Agent测试类"""
    
    @pytest.fixture
    def agent_without_model(self):
        """创建不带模型的Agent"""
        return SteelDesignAgent()
    
    @pytest.fixture
    def agent_with_model(self):
        """创建带模型的Agent"""
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "PINN model/normal/model_20250123_165719.pth"
        )
        if os.path.exists(model_path):
            return SteelDesignAgent(model_path=model_path)
        else:
            return SteelDesignAgent()
    
    def test_agent_initialization(self, agent_without_model):
        """Test Agent初始化"""
        assert agent_without_model is not None
        assert hasattr(agent_without_model, 'calculator')
        assert hasattr(agent_without_model, 'conversation_history')
        assert hasattr(agent_without_model, 'system_prompt')
    
    def test_agent_configuration(self, agent_without_model):
        """Test Agent配置"""
        assert agent_without_model.base_url is not None
        assert agent_without_model.model_name is not None
        assert isinstance(agent_without_model.conversation_history, list)
    
    def test_agent_with_custom_config(self):
        """测试自定义配置的Agent"""
        agent = SteelDesignAgent(
            api_key="test-key",
            base_url="https://test.com",
            model_name="test-model"
        )
        
        assert agent.api_key == "test-key"
        assert agent.base_url == "https://test.com"
        assert agent.model_name == "test-model"
    
    def test_reset_conversation(self, agent_without_model):
        """测试重置对话"""
        # 添加一些对话历史
        agent_without_model.conversation_history.append({
            "role": "user",
            "content": "test"
        })
        
        assert len(agent_without_model.conversation_history) > 0
        
        # 重置
        agent_without_model.reset_conversation()
        
        assert len(agent_without_model.conversation_history) == 0
    
    def test_get_conversation_history(self, agent_without_model):
        """测试获取对话历史"""
        history = agent_without_model.get_conversation_history()
        
        assert isinstance(history, list)
        assert len(history) == 0  # 初始应该为空
    
    def test_load_model(self, agent_without_model):
        """测试加载模型"""
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "PINN model/normal/model_20250123_165719.pth"
        )
        
        if not os.path.exists(model_path):
            pytest.skip("Model file does not exist")
        
        agent_without_model.load_model(model_path)
        
        # 验证模型Loaded到calculator
        assert agent_without_model.calculator.predictor.model is not None
    
    def test_system_prompt(self, agent_without_model):
        """测试系统Tip词"""
        assert agent_without_model.system_prompt is not None
        assert len(agent_without_model.system_prompt) > 0
        assert '钢柱' in agent_without_model.system_prompt or 'column' in agent_without_model.system_prompt.lower()
    
    def test_chat_without_api_key(self, agent_without_model):
        """测试没有API密钥时的对话"""
        # 临时移除API密钥
        original_client = agent_without_model.client
        agent_without_model.client = None
        
        response = agent_without_model.chat("测试消息")
        
        assert "Error" in response or "API" in response
        
        # 恢复
        agent_without_model.client = original_client
    
    def test_calculator_integration(self, agent_with_model):
        """测试Calculate器集成"""
        assert agent_with_model.calculator is not None
        
        # 测试直接调用Calculate器
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        result = agent_with_model.calculator.calculate_column_strength(params)
        
        # 如果模型加载Success，应该能Calculate
        if agent_with_model.calculator.model_loaded:
            assert result['success'] == True


class TestAgentTools:
    """Test Agent工具定义"""
    
    def test_steel_strength_tools_definition(self):
        """Test tool定义格式"""
        from agent.tools.steel_strength_tools import STEEL_STRENGTH_TOOLS
        
        assert isinstance(STEEL_STRENGTH_TOOLS, list)
        assert len(STEEL_STRENGTH_TOOLS) > 0
        
        # 检查第一个工具的格式
        tool = STEEL_STRENGTH_TOOLS[0]
        assert 'type' in tool
        assert tool['type'] == 'function'
        assert 'function' in tool
        assert 'name' in tool['function']
        assert 'description' in tool['function']
        assert 'parameters' in tool['function']
    
    def test_calculate_column_strength_tool_definition(self):
        """测试钢柱强度Calculate工具定义"""
        from agent.tools.steel_strength_tools import STEEL_STRENGTH_TOOLS
        
        # 找到calculate_column_strength工具
        column_tool = None
        for tool in STEEL_STRENGTH_TOOLS:
            if tool['function']['name'] == 'calculate_column_strength':
                column_tool = tool
                break
        
        assert column_tool is not None, "应该有calculate_column_strength工具"
        
        # 检查参数定义
        params = column_tool['function']['parameters']
        assert 'properties' in params
        assert 'A' in params['properties']
        assert 'I' in params['properties']
        assert 'L' in params['properties']
        assert 'fy' in params['properties']
        
        # 检查Required parameters
        assert 'required' in params
        assert 'A' in params['required']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

