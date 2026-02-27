"""
Test LLM Agent functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from agent import SteelDesignAgent


class TestSteelDesignAgent:
    """LLM Agent test class"""
    
    @pytest.fixture
    def agent_without_model(self):
        """Create Agent without model"""
        return SteelDesignAgent()
    
    @pytest.fixture
    def agent_with_model(self):
        """Create Agent with model"""
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "PINN model/normal/model_20250123_165719.pth"
        )
        if os.path.exists(model_path):
            return SteelDesignAgent(model_path=model_path)
        else:
            return SteelDesignAgent()
    
    def test_agent_initialization(self, agent_without_model):
        """Test Agent initialization"""
        assert agent_without_model is not None
        assert hasattr(agent_without_model, 'calculator')
        assert hasattr(agent_without_model, 'conversation_history')
        assert hasattr(agent_without_model, 'system_prompt')
    
    def test_agent_configuration(self, agent_without_model):
        """Test Agent configuration"""
        assert agent_without_model.base_url is not None
        assert agent_without_model.model_name is not None
        assert isinstance(agent_without_model.conversation_history, list)
    
    def test_agent_with_custom_config(self):
        """Test Agent with custom configuration"""
        agent = SteelDesignAgent(
            api_key="test-key",
            base_url="https://test.com",
            model_name="test-model"
        )
        
        assert agent.api_key == "test-key"
        assert agent.base_url == "https://test.com"
        assert agent.model_name == "test-model"
    
    def test_reset_conversation(self, agent_without_model):
        """Test conversation reset"""
        # Add some conversation history
        agent_without_model.conversation_history.append({
            "role": "user",
            "content": "test"
        })
        
        assert len(agent_without_model.conversation_history) > 0
        
        # Reset
        agent_without_model.reset_conversation()
        
        assert len(agent_without_model.conversation_history) == 0
    
    def test_get_conversation_history(self, agent_without_model):
        """Test getting conversation history"""
        history = agent_without_model.get_conversation_history()
        
        assert isinstance(history, list)
        assert len(history) == 0  # Should be empty initially
    
    def test_load_model(self, agent_without_model):
        """Test model loading"""
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "PINN model/normal/model_20250123_165719.pth"
        )
        
        if not os.path.exists(model_path):
            pytest.skip("Model file does not exist")
        
        agent_without_model.load_model(model_path)
        
        # Verify model loaded to calculator
        assert agent_without_model.calculator.predictor.model is not None
    
    def test_system_prompt(self, agent_without_model):
        """Test system prompt"""
        assert agent_without_model.system_prompt is not None
        assert len(agent_without_model.system_prompt) > 0
        assert 'column' in agent_without_model.system_prompt.lower()
    
    def test_chat_without_api_key(self, agent_without_model):
        """Test chat without API key"""
        # Temporarily remove API key
        original_client = agent_without_model.client
        agent_without_model.client = None
        
        response = agent_without_model.chat("test message")
        
        assert "Error" in response or "API" in response
        
        # Restore
        agent_without_model.client = original_client
    
    def test_calculator_integration(self, agent_with_model):
        """Test calculator integration"""
        assert agent_with_model.calculator is not None
        
        # Test direct calculator call
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        result = agent_with_model.calculator.calculate_column_strength(params)
        
        # If model loaded successfully, should be able to calculate
        if agent_with_model.calculator.model_loaded:
            assert result['success'] == True


class TestAgentTools:
    """Test Agent tool definitions"""
    
    def test_steel_strength_tools_definition(self):
        """Test tool definition format"""
        from agent.tools.steel_strength_tools import STEEL_STRENGTH_TOOLS
        
        assert isinstance(STEEL_STRENGTH_TOOLS, list)
        assert len(STEEL_STRENGTH_TOOLS) > 0
        
        # Check first tool format
        tool = STEEL_STRENGTH_TOOLS[0]
        assert 'type' in tool
        assert tool['type'] == 'function'
        assert 'function' in tool
        assert 'name' in tool['function']
        assert 'description' in tool['function']
        assert 'parameters' in tool['function']
    
    def test_calculate_column_strength_tool_definition(self):
        """Test steel column strength calculation tool definition"""
        from agent.tools.steel_strength_tools import STEEL_STRENGTH_TOOLS
        
        # Find calculate_column_strength tool
        column_tool = None
        for tool in STEEL_STRENGTH_TOOLS:
            if tool['function']['name'] == 'calculate_column_strength':
                column_tool = tool
                break
        
        assert column_tool is not None, "Should have calculate_column_strength tool"
        
        # Check parameter definitions
        params = column_tool['function']['parameters']
        assert 'properties' in params
        assert 'A' in params['properties']
        assert 'I' in params['properties']
        assert 'L' in params['properties']
        assert 'fy' in params['properties']
        
        # Check required parameters
        assert 'required' in params
        assert 'A' in params['required']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
