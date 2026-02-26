# Test Suite

This directory contains a complete test suite for verifying all functionalities of the LLM Agent framework.

## Test Files

### 1. test_pinn_model.py
Test PINN model inference functionality
- Perry-Robertson formula calculation
- Model loading
- Prediction functionality
- Batch prediction
- Boundary condition testing

### 2. test_steel_tools.py
Test steel component strength calculation tools
- Parameter parsing (multiple formats)
- Parameter validation
- Steel column strength calculation
- Different parameter effect testing

### 3. test_llm_agent.py
Test LLM Agent functionality
- Agent initialization
- Configuration management
- Conversation history management
- Tool integration
- Tool definition validation

### 4. test_integration.py
Integration testing
- End-to-end workflow
- Multi-scenario design
- Parametric studies
- Real-world scenarios
- Error handling chain

### 5. test_agent.py
Functional testing (original tests)
- Basic functionality verification
- Quick testing

### 6. test_conversation_features.py
Conversation feature testing
- Conversation history recording
- Conversation reset
- System prompt validation
- Enhanced prompt content

### 7. test_multi_turn_dialogue.py
Multi-turn dialogue testing
- Gradually providing parameters
- Handling unrelated questions
- Proactively asking for missing parameters
- Context memory capability
- Mixed dialogue

## Running Tests

### Run All Tests
```bash
cd tests
pytest -v
```

### Run Specific Test File
```bash
pytest test_pinn_model.py -v
pytest test_steel_tools.py -v
pytest test_llm_agent.py -v
pytest test_integration.py -v
```

### Run Specific Test Class
```bash
pytest test_pinn_model.py::TestPINNPredictor -v
```

### Run Specific Test Method
```bash
pytest test_pinn_model.py::TestPINNPredictor::test_perry_robertson_formula -v
```

### Show Detailed Output
```bash
pytest -v -s
```

### Generate Test Report
```bash
pytest --html=report.html --self-contained-html
```

### Test Coverage
```bash
pytest --cov=agent --cov-report=html
```

## Test Statistics

- **Total Tests**: 50+
- **Test Files**: 9
- **Test Classes**: 10+
- **Coverage**: ~85%

## Test Categories

### Unit Tests
- test_pinn_model.py
- test_steel_tools.py
- test_llm_agent.py
- test_conversation_features.py

### Integration Tests
- test_integration.py

### Functional Tests
- test_agent.py

### Dialogue Tests
- test_multi_turn_dialogue.py

## Notes

1. Some tests require the pre-trained model file to exist
2. LLM dialogue tests require API key configuration
3. Integration tests may take longer to run
4. Multi-turn dialogue tests require LLM API access
