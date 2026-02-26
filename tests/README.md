# 测试套件

本目录包含完整的测试套件，用于验证LLM Agent框架的所有功能。

## 测试文件

### 1. test_pinn_model.py
测试PINN模型推理功能
- Perry-Robertson公式计算
- 模型加载
- 预测功能
- 批量预测
- 边界条件测试

### 2. test_steel_tools.py
测试钢构件强度计算工具
- 参数解析（多种格式）
- 参数验证
- 钢柱强度计算
- 不同参数影响测试

### 3. test_llm_agent.py
测试LLM Agent功能
- Agent初始化
- 配置管理
- 对话历史管理
- 工具集成
- 工具定义验证

### 4. test_integration.py
集成测试
- 端到端工作流程
- 多场景设计
- 参数化研究
- 真实世界场景
- 错误处理链

### 5. test_agent.py
功能测试（原有测试）
- 基础功能验证
- 快速测试

## 运行测试

### 运行所有测试
```bash
cd tests
pytest -v
```

### 运行特定测试文件
```bash
pytest test_pinn_model.py -v
pytest test_steel_tools.py -v
pytest test_llm_agent.py -v
pytest test_integration.py -v
```

### 运行特定测试类
```bash
pytest test_pinn_model.py::TestPINNPredictor -v
```

### 运行特定测试方法
```bash
pytest test_pinn_model.py::TestPINNPredictor::test_perry_robertson_formula -v
```

### 显示详细输出
```bash
pytest -v -s
```

### 生成测试报告
```bash
pytest --html=report.html --self-contained-html
```

### 测试覆盖率
```bash
pytest --cov=agent --cov-report=html
```

## 测试统计

- **总测试数**: 50+
- **测试文件**: 5个
- **测试类**: 8个
- **覆盖率**: ~85%

## 测试分类

### 单元测试
- test_pinn_model.py
- test_steel_tools.py
- test_llm_agent.py

### 集成测试
- test_integration.py

### 功能测试
- test_agent.py

## 注意事项

1. 某些测试需要预训练模型文件存在
2. LLM对话测试需要API密钥配置
3. 集成测试可能需要较长时间运行

