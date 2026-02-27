# 钢结构设计智能系统 - 完整使用指南

## 📋 目录

1. [系统简介](#系统简介)
2. [快速开始](#快速开始)
3. [安装步骤](#安装步骤)
4. [功能模块](#功能模块)
5. [使用教程](#使用教程)
6. [示例场景](#示例场景)
7. [常见问题](#常见问题)
8. [技术支持](#技术支持)

---

## 🎯 系统简介

这是一个集成的智能钢结构设计系统，结合了人工智能和结构工程专业知识，帮助您完成从建筑布局设计到钢构件强度计算的全流程设计工作。

### 核心功能

✅ **自然语言建筑设计** - 用日常语言描述建筑，系统自动生成布局  
✅ **3D蓝图可视化** - 自动生成建筑的3D透视图  
✅ **柱子荷载分析** - 智能计算每根柱子的受力  
✅ **截面优化选择** - 自动推荐最经济的钢构件截面  
✅ **PINN强度计算** - 使用物理信息神经网络精确计算构件强度  
✅ **多轮对话交互** - 智能助手引导您完成设计  

### 适用人群

- 🏗️ 结构工程师
- 🎓 土木工程专业学生
- 🏢 建筑设计师
- 📐 工程咨询人员
- 💡 对钢结构设计感兴趣的任何人

---

## ⚡ 快速开始

### 最简单的使用方式

1. **打开终端/命令提示符**

2. **进入项目目录**
   ```bash
   cd /path/to/LLM_steel_design
   ```

3. **运行启动脚本**
   
   **Mac/Linux:**
   ```bash
   ./start_agent.sh
   ```
   
   **Windows:**
   ```cmd
   start_agent.bat
   ```

4. **开始对话**
   ```
   User: 你好，我想计算钢柱强度
   Agent: 您好！我可以帮您计算钢柱的抗压强度。请提供以下参数...
   ```

---

## 🔧 安装步骤

### 第一步：检查Python环境

确保您的电脑已安装Python 3.8或更高版本。

**检查方法：**
```bash
python --version
# 或
python3 --version
```

如果没有安装Python，请访问 [python.org](https://www.python.org/downloads/) 下载安装。

### 第二步：下载项目

**方式1：使用Git（推荐）**
```bash
git clone https://github.com/your-repo/LLM_steel_design.git
cd LLM_steel_design
```

**方式2：直接下载**
- 从GitHub下载ZIP文件
- 解压到您选择的目录
- 在终端中进入该目录

### 第三步：安装依赖包

```bash
pip install -r requirements.txt
```

**如果遇到网络问题，可以使用国内镜像：**
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 第四步：配置API密钥

1. **复制配置文件模板**
   ```bash
   cp env.example .env
   ```

2. **编辑.env文件**
   
   使用任何文本编辑器打开`.env`文件，填入您的API密钥：
   
   ```bash
   # 使用阿里云DashScope（推荐国内用户）
   DASHSCOPE_API_KEY=your-dashscope-api-key-here
   LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
   LLM_MODEL=qwen-max
   
   # 或使用OpenAI
   # OPENAI_API_KEY=your-openai-api-key-here
   # LLM_BASE_URL=https://api.openai.com/v1
   # LLM_MODEL=gpt-4
   ```

3. **获取API密钥**
   
   - **阿里云DashScope**: 访问 [dashscope.aliyun.com](https://dashscope.aliyun.com)
   - **OpenAI**: 访问 [platform.openai.com](https://platform.openai.com)

### 第五步：验证安装

```bash
python -m agent.agent
```

如果看到以下信息，说明安装成功：
```
====================================
Steel Structure Design LLM Agent
====================================

✓ LLM client initialized
✓ PINN model loaded
Agent started! Enter 'quit' or 'exit' to exit
```

---

## 🎨 功能模块

### 模块1：钢柱强度计算（基础功能）

**功能描述：** 使用PINN模型计算钢柱的抗压强度

**使用方法：**
```bash
./start_agent.sh
```

**对话示例：**
```
User: 计算钢柱强度，参数：A=10, I=100, c=5, L=120, fy=50, delta_o=0.1

Agent: 好的，我来为您计算这根钢柱的抗压强度。

参数确认：
- 截面积 A = 10 in²
- 惯性矩 I = 100 in⁴
- 距离 c = 5 in
- 长度 L = 120 in
- 屈服强度 fy = 50 ksi
- 初始缺陷 delta_o = 0.1 in

[调用PINN模型计算...]

计算结果：
- 预测抗压强度：450.2 kips
- 长细比：λ = 85.3
- 设计建议：该柱子满足AISC规范要求...
```

### 模块2：建筑布局设计（集成功能）

**功能描述：** 用自然语言描述建筑，自动生成布局和3D蓝图

**使用方法：**
```bash
python integrated_design.py --mode interactive
```

**对话示例：**
```
Command: design

Describe your building: 我需要一个4个房间的办公楼，每个房间20x15英尺，
中间有一个走廊连接所有房间

Dead load (psf) [default: 50]: 60
Live load (psf) [default: 40]: 50
Number of floors [default: 1]: 2

[系统开始处理...]

✓ Parsed 5 rooms (4 rooms + 1 corridor)
✓ Blueprint saved to: output/blueprint.svg
✓ Analyzed 20 columns
  Total load: 156,000 lbs
  Total steel weight: 8,450 lbs
✓ Complete design report saved to: output/design_report.json
```

### 模块3：柱子荷载分析

**功能描述：** 自动计算建筑中每根柱子的荷载并推荐截面

**Python API使用：**
```python
from building_design import (
    parse_building_description,
    calculate_all_column_loads,
    optimize_column_section
)

# 解析建筑描述
blueprint = parse_building_description("4个房间的建筑，每个房间20x15英尺")

# 计算柱子荷载
column_loads = calculate_all_column_loads(
    blueprint,
    dead_load_psf=50,
    live_load_psf=40,
    num_floors=2
)

# 为每根柱子优化截面
for col_name, load in column_loads.items():
    section = optimize_column_section(load)
    print(f"{col_name}: {section['type']} (capacity: {section['capacity']:.0f} lbs)")
```

---

## 📚 使用教程

### 教程1：第一次使用 - 计算单根钢柱强度

**场景：** 您有一根钢柱，需要知道它能承受多大的压力。

**步骤：**

1. **启动系统**
   ```bash
   ./start_agent.sh
   ```

2. **询问需要的参数**
   ```
   User: 我想计算钢柱强度，需要什么参数？
   ```

3. **Agent会回复：**
   ```
   Agent: 我需要以下参数来计算钢柱强度：
   
   1. A (截面积) - 单位：in²，典型值：5-50
   2. I (惯性矩) - 单位：in⁴，典型值：50-500
   3. c (距离) - 从截面中心到边缘，单位：in，典型值：2-10
   4. L (长度) - 柱子有效长度，单位：in，典型值：60-300
   5. fy (屈服强度) - 钢材屈服强度，单位：ksi，典型值：36-70
   6. delta_o (初始缺陷) - 初始几何缺陷，单位：in，典型值：0.05-0.5
   
   您可以一次提供所有参数，也可以逐个告诉我。
   ```

4. **提供参数（方式1：一次性提供）**
   ```
   User: A=10, I=100, c=5, L=120, fy=50, delta_o=0.1
   ```

5. **提供参数（方式2：逐步提供）**
   ```
   User: A=10, I=100
   Agent: 好的，已记录：截面积A=10 in²，惯性矩I=100 in⁴
         还需要：c, L, fy, delta_o
   
   User: c=5, L=120
   Agent: 继续记录：c=5 in, L=120 in
         还需要：fy, delta_o
   
   User: fy=50, delta_o=0.1
   Agent: 参数齐全，开始计算...
   ```

6. **查看结果**
   ```
   Agent: 计算完成！
   
   钢柱强度分析结果：
   - 预测抗压强度：450.2 kips
   - 欧拉临界荷载：523.6 kips
   - 长细比：85.3
   - 利用率：0.86
   
   设计建议：
   ✓ 该柱子满足AISC规范要求
   ✓ 长细比在合理范围内
   ✓ 建议安全系数：1.67
   ```

### 教程2：设计一个完整的建筑

**场景：** 您需要设计一个小型办公楼，包含多个房间。

**步骤：**

1. **启动集成系统**
   ```bash
   python integrated_design.py --mode interactive
   ```

2. **选择设计模式**
   ```
   Command: design
   ```

3. **描述您的建筑**
   ```
   Describe your building: 
   我需要一个办公楼，包含：
   - 4个办公室，每个20x15英尺
   - 1个会议室，30x20英尺
   - 1个走廊连接所有房间
   建筑高度10英尺
   ```

4. **输入荷载参数**
   ```
   Dead load (psf) [default: 50]: 60
   Live load (psf) [default: 40]: 50
   Number of floors [default: 1]: 1
   ```

5. **系统自动处理**
   ```
   [Step 1/4] Parsing building description...
   ✓ Parsed 6 rooms
   
   [Step 2/4] Generating 3D blueprint...
   ✓ Blueprint saved to: output/blueprint.svg
   
   [Step 3/4] Analyzing column loads and designing sections...
   ✓ Analyzed 24 columns
     Total load: 132,000 lbs
     Total steel weight: 6,780 lbs
   
   [Step 4/4] Calculating detailed steel member strengths...
   
   Calculating strength for Column_(0.0,0.0) (W10x60)...
   Parameters: A=17.6 in², I=341.7 in⁴, L=120.0 in
   
   Agent: 根据PINN模型计算，该柱子的抗压强度为792.0 kips...
   ```

6. **查看生成的文件**
   ```
   output/
   ├── blueprint.svg          # 3D蓝图
   └── design_report.json     # 完整设计报告
   ```

7. **打开蓝图查看**
   - 双击`blueprint.svg`文件
   - 或在浏览器中打开
   - 您会看到建筑的3D透视图

### 教程3：使用Python API进行批量设计

**场景：** 您需要对多个建筑方案进行对比分析。

**创建Python脚本：**

```python
# batch_design.py
from integrated_design import IntegratedDesignSystem

# 初始化系统
system = IntegratedDesignSystem()

# 定义多个设计方案
designs = [
    {
        "name": "方案A - 紧凑型",
        "description": "4个房间，每个15x15英尺，中间走廊",
        "dead_load": 50,
        "live_load": 40,
        "floors": 1
    },
    {
        "name": "方案B - 宽敞型",
        "description": "4个房间，每个25x20英尺，中间走廊",
        "dead_load": 50,
        "live_load": 40,
        "floors": 1
    },
    {
        "name": "方案C - 多层型",
        "description": "4个房间，每个20x15英尺，中间走廊",
        "dead_load": 60,
        "live_load": 50,
        "floors": 2
    }
]

# 批量处理
results = []
for design in designs:
    print(f"\n处理 {design['name']}...")
    
    report = system.design_building(
        description=design['description'],
        dead_load_psf=design['dead_load'],
        live_load_psf=design['live_load'],
        num_floors=design['floors'],
        output_dir=f"output/{design['name']}"
    )
    
    results.append({
        "name": design['name'],
        "total_load": report['column_analysis']['summary']['total_load'],
        "steel_weight": report['column_analysis']['summary']['total_steel_weight'],
        "num_columns": report['column_analysis']['summary']['total_columns']
    })

# 对比分析
print("\n" + "="*60)
print("方案对比")
print("="*60)
for r in results:
    print(f"\n{r['name']}:")
    print(f"  总荷载: {r['total_load']:,.0f} lbs")
    print(f"  钢材用量: {r['steel_weight']:,.0f} lbs")
    print(f"  柱子数量: {r['num_columns']}")
```

**运行脚本：**
```bash
python batch_design.py
```

---

## 💡 示例场景

### 场景1：住宅设计

```
User: 设计一个住宅，包含：
- 客厅 25x20英尺
- 3个卧室，每个15x12英尺
- 厨房 15x12英尺
- 2个卫生间，每个8x6英尺
- 走廊连接所有房间

Dead load: 40 psf (住宅较轻)
Live load: 40 psf (ASCE住宅标准)
Floors: 2
```

### 场景2：仓库设计

```
User: 设计一个仓库，包含：
- 主存储区 60x40英尺
- 办公区 20x15英尺
- 装卸区 30x20英尺
建筑高度15英尺

Dead load: 80 psf (重型结构)
Live load: 125 psf (仓库荷载)
Floors: 1
```

### 场景3：学校教学楼

```
User: 设计一个教学楼，包含：
- 6个教室，每个30x25英尺
- 2个实验室，每个35x30英尺
- 1个大厅 40x30英尺
- 走廊连接所有房间
建筑高度12英尺

Dead load: 70 psf
Live load: 100 psf (教室荷载标准)
Floors: 3
```

---

## ❓ 常见问题

### Q1: 启动时提示"API key not set"怎么办？

**A:** 您需要配置API密钥：
1. 复制`env.example`为`.env`
2. 编辑`.env`文件，填入您的API密钥
3. 保存后重新启动

### Q2: 如何获取API密钥？

**A:** 
- **阿里云DashScope（推荐国内用户）**：
  1. 访问 https://dashscope.aliyun.com
  2. 注册/登录账号
  3. 进入控制台获取API Key
  
- **OpenAI**：
  1. 访问 https://platform.openai.com
  2. 注册/登录账号
  3. 进入API Keys页面创建密钥

### Q3: 安装依赖时出错怎么办？

**A:** 尝试以下方法：
```bash
# 方法1：升级pip
python -m pip install --upgrade pip

# 方法2：使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 方法3：逐个安装
pip install torch numpy pandas scikit-learn matplotlib seaborn openai python-dotenv svgwrite
```

### Q4: PINN模型文件找不到怎么办？

**A:** 
- 系统会自动检测模型文件
- 如果没有模型文件，系统仍可运行，但不能使用高精度PINN计算
- 模型文件应位于：`PINN model/normal/model_20250123_165719.pth`

### Q5: 生成的蓝图打不开？

**A:** 
- 蓝图是SVG格式，可以用浏览器打开
- 也可以用Adobe Illustrator、Inkscape等软件打开
- 如果需要PDF格式，可以在浏览器中打开后打印为PDF

### Q6: 如何理解参数的含义？

**A:** 主要参数说明：

| 参数 | 符号 | 单位 | 说明 | 典型值 |
|------|------|------|------|--------|
| 截面积 | A | in² | 钢柱横截面积 | 5-50 |
| 惯性矩 | I | in⁴ | 截面惯性矩 | 50-500 |
| 距离 | c | in | 截面中心到边缘距离 | 2-10 |
| 长度 | L | in | 柱子有效长度 | 60-300 |
| 屈服强度 | fy | ksi | 钢材屈服强度 | 36-70 |
| 初始缺陷 | delta_o | in | 初始几何缺陷 | 0.05-0.5 |

### Q7: 计算结果的可靠性如何？

**A:** 
- PINN模型基于物理定律和大量数据训练
- 计算结果符合AISC规范
- 建议：重要工程请由专业工程师复核

### Q8: 可以用于实际工程吗？

**A:** 
- ✅ 可用于初步设计和方案比选
- ✅ 可用于教学和学习
- ⚠️ 实际工程需要专业工程师审核
- ⚠️ 需要考虑更多实际因素（地震、风荷载等）

### Q9: 如何保存对话历史？

**A:** 
```python
# 在Python中使用
from agent.agent import SteelDesignAgent

agent = SteelDesignAgent()
agent.chat("计算钢柱强度...")

# 获取对话历史
history = agent.get_conversation_history()

# 保存到文件
import json
with open('conversation.json', 'w') as f:
    json.dump(history, f, indent=2)
```

### Q10: 系统支持哪些语言？

**A:** 
- 系统界面和文档：中文和英文
- LLM对话：支持中文和英文
- 技术术语：遵循国际标准（AISC、ASCE等）

---

## 🔬 技术支持

### 报告问题

如果遇到问题，请提供以下信息：

1. **系统信息**
   ```bash
   python --version
   pip list | grep -E "torch|openai|numpy"
   ```

2. **错误信息**
   - 完整的错误堆栈
   - 您执行的命令
   - 输入的参数

3. **提交方式**
   - GitHub Issues
   - 邮件联系

### 进阶使用

**自定义PINN模型：**
```python
from agent.agent import SteelDesignAgent

# 使用自定义模型
agent = SteelDesignAgent(model_path="path/to/your/model.pth")
```

**扩展功能：**
```python
from building_design import column_analyzer

# 自定义截面库
custom_sections = [
    {"type": "Custom-1", "area": 30, "fy": 60, "cost_factor": 1.2},
    {"type": "Custom-2", "area": 40, "fy": 60, "cost_factor": 1.5}
]

section = column_analyzer.optimize_column_section(
    required_load=100000,
    available_sections=custom_sections
)
```

### 学习资源

- **AISC规范**: [aisc.org](https://www.aisc.org)
- **钢结构设计**: 推荐教材《钢结构设计原理》
- **Python编程**: [python.org/doc](https://docs.python.org)
- **机器学习**: [pytorch.org/tutorials](https://pytorch.org/tutorials)

---

## 📝 更新日志

### v2.0.0 (2025-02-27)
- ✨ 新增建筑布局设计功能
- ✨ 新增3D蓝图可视化
- ✨ 新增柱子荷载分析
- ✨ 新增集成设计系统
- 🌐 完整英文化
- 📚 新增详细使用文档

### v1.0.0 (2025-01-23)
- 🎉 初始版本发布
- ✅ PINN钢柱强度计算
- ✅ 多轮对话功能
- ✅ 参数智能提示

---

## 📄 许可证

本项目采用 MIT 许可证。

---

## 👥 贡献者

感谢所有为本项目做出贡献的开发者！

---

## 📞 联系方式

- **项目主页**: [GitHub Repository]
- **问题反馈**: [GitHub Issues]
- **邮件**: your-email@example.com

---

**祝您使用愉快！如有任何问题，欢迎随时联系我们。** 🎉

