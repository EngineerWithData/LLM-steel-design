# Task 3.3 Implementation Plan: OpenSeesPy Automation System

## Overview
Based on the research paper "Automating 2D Structural Analysis with Multi-Agent LLMs", this document outlines the implementation plan for Task 3.3: Automated structural analysis model creation and interpretation using OpenSeesPy.

## Paper Summary

### Key Findings
1. **Multi-agent approach outperforms single LLM**: Specialized agents achieve 80%+ accuracy vs. 40-60% for GPT-4o/Gemini
2. **Task decomposition is critical**: Separating geometry reasoning from code generation significantly improves reliability
3. **Cost-effective**: Using Llama 3.3 70B achieves good results at lower cost
4. **Structured intermediate representation**: JSON format between geometry and code generation improves accuracy

### Architecture from Paper (Fig. 5)
```
User Input (Natural Language)
         ↓
[Problem Analysis Agent] ← Coordinates overall workflow
         ↓
[Geometry Agent] ← Extracts structural geometry, nodes, elements
         ↓
    JSON Format (Structured representation)
         ↓
[Code Translation Agent] ← Converts JSON → OpenSeesPy code
         ↓
[Model Validation Agent] ← Validates generated code
         ↓
[Load Agent] ← Handles load definitions (integrated)
         ↓
OpenSeesPy Execution
         ↓
Results & Interpretation
```

## Current Project Status

### ✅ Completed (Tasks 3.1 & 3.2)
1. **Task 3.1 - Geometry Optimization** (by Bartu):
   - Natural language building description
   - Automated room layout generation
   - 3D blueprint visualization
   - Column placement optimization

2. **Task 3.2 - Steel Strength Calculation** (by Kai):
   - PINN model for column strength prediction
   - LLM agent for parameter recognition
   - Multi-turn dialogue support
   - Integration with building design

### 🚧 To Implement (Task 3.3)
1. **OpenSeesPy Model Creation**
   - Geometry Agent
   - Code Translation Agent
   - Model Validation Agent

2. **Structural Analysis Execution**
   - Run OpenSeesPy models
   - Capture and interpret results
   - Visualize analysis outputs

3. **Integration**
   - Connect with existing 3.1 (geometry) and 3.2 (strength calculation)
   - Create unified workflow
   - Validate with AISC benchmarks

## Detailed Implementation Plan

### Phase 1: Multi-Agent System Architecture

#### 1.1 Geometry Agent
**Purpose**: Convert natural language structural descriptions → structured JSON

**Input Example**:
```
"A 2-story steel frame building with 3 bays. Each bay is 20 feet wide.
Story heights are 12 feet for the first floor and 10 feet for the second floor.
Use W14x90 columns and W21x50 beams. Fixed supports at the base."
```

**Output Format (JSON)**:
```json
{
  "structure_type": "2D_frame",
  "units": {"length": "ft", "force": "kip"},
  "nodes": [
    {"id": 1, "x": 0, "y": 0, "constraints": [1,1,1]},
    {"id": 2, "x": 20, "y": 0, "constraints": [1,1,1]},
    ...
  ],
  "elements": [
    {
      "id": 1,
      "type": "elasticBeamColumn",
      "nodes": [1, 4],
      "section": "W14x90",
      "orientation": "vertical"
    },
    ...
  ],
  "materials": [
    {"id": 1, "type": "steel", "E": 29000, "fy": 50}
  ],
  "sections": [
    {"name": "W14x90", "A": 26.5, "I": 999}
  ],
  "loads": [
    {
      "type": "point",
      "node": 4,
      "direction": "Y",
      "magnitude": -10.0
    }
  ],
  "analysis": {
    "type": "static",
    "steps": 1
  }
}
```

**Implementation Details**:
- Use LLM with specialized prompt for structural engineering
- Leverage existing building geometry from Task 3.1
- Include W-section database lookup
- Validate geometric consistency (e.g., node connectivity)

#### 1.2 Code Translation Agent
**Purpose**: Convert structured JSON → valid OpenSeesPy code

**Key Responsibilities**:
1. Generate proper OpenSeesPy command sequence
2. Handle coordinate transformations
3. Create material and section definitions
4. Set up boundary conditions and loads
5. Configure analysis parameters

**Template-Based Approach**:
```python
# Template structure
wipe()
model('basic', '-ndm', {ndm}, '-ndf', {ndf})

# Materials
{material_definitions}

# Nodes
{node_definitions}

# Boundary conditions
{fix_definitions}

# Geometric transformations
{geom_transf_definitions}

# Sections (if using fiber sections)
{section_definitions}

# Elements
{element_definitions}

# Loads
{load_definitions}

# Analysis
{analysis_setup}
{analysis_execution}

# Output
{recorder_setup}
```

#### 1.3 Model Validation Agent
**Purpose**: Verify OpenSeesPy code before execution

**Validation Checks**:
1. **Syntax validation**: Parse Python code for errors
2. **Semantic validation**:
   - All referenced nodes exist
   - Element connectivity is valid
   - Material/section IDs are defined before use
   - Boundary conditions are sufficient (prevent rigid body motion)
3. **Structural validation**:
   - Check for unstable configurations
   - Verify load paths
   - Ensure analysis convergence settings are reasonable

**Implementation**:
- Use AST parsing for syntax checking
- Build dependency graph for semantic validation
- Run quick structural checks (determinant, eigenvalues)

### Phase 2: OpenSeesPy Execution Engine

#### 2.1 Code Execution
**Features**:
- Safe execution environment (sandbox if needed)
- Timeout handling
- Error capture and reporting
- Result file management

**Implementation**:
```python
class OpenSeesPyExecutor:
    def __init__(self, working_dir="./analysis"):
        self.working_dir = working_dir

    def execute_model(self, code: str, timeout=60):
        """Execute OpenSeesPy code and capture results"""
        # Write code to file
        # Set up recorders
        # Execute with subprocess
        # Capture output
        # Parse results
        return results

    def parse_results(self, output_files):
        """Parse OpenSeesPy output files"""
        # Read node displacements
        # Read element forces
        # Calculate derived quantities
        return structured_results
```

#### 2.2 Result Interpretation
**Outputs to Extract**:
1. **Displacements**: Node displacements (max, locations)
2. **Forces**: Element axial forces, shears, moments
3. **Reactions**: Support reactions
4. **Stresses**: If using fiber sections
5. **Mode shapes & periods**: For eigenvalue analysis

**Natural Language Summary**:
- Generate human-readable interpretations
- Highlight critical values (max displacement, max stress ratio)
- Compare against code limits (e.g., drift limits)

### Phase 3: Integration with Existing Modules

#### 3.1 Integration Architecture
```
[Building Design Module - Task 3.1]
  - Room layout generation
  - Column placement
  - Load tributary areas
         ↓
[Geometry Agent - Task 3.3]
  - Convert building to structural model
  - Define frame elements
         ↓
[Steel Strength Module - Task 3.2]
  - Calculate member capacities
  - Verify design adequacy
         ↓
[OpenSeesPy Analysis - Task 3.3]
  - Run structural analysis
  - Get actual forces and displacements
         ↓
[Integrated Report]
  - Design is adequate / needs revision
  - Utilization ratios
  - Recommendations
```

#### 3.2 Unified Workflow
```python
class IntegratedStructuralDesignSystem:
    def __init__(self):
        self.building_designer = BuildingDesignModule()  # Task 3.1
        self.steel_calculator = SteelStrengthCalculator()  # Task 3.2
        self.geometry_agent = GeometryAgent()  # Task 3.3
        self.code_translator = CodeTranslationAgent()  # Task 3.3
        self.validator = ModelValidationAgent()  # Task 3.3
        self.executor = OpenSeesPyExecutor()  # Task 3.3

    def complete_design(self, description, loads):
        # Step 1: Generate building layout (3.1)
        building = self.building_designer.design(description)

        # Step 2: Convert to structural model (3.3)
        structural_json = self.geometry_agent.process(building, loads)

        # Step 3: Generate OpenSeesPy code (3.3)
        code = self.code_translator.translate(structural_json)

        # Step 4: Validate code (3.3)
        validation = self.validator.validate(code, structural_json)
        if not validation.is_valid:
            return {"error": validation.errors}

        # Step 5: Execute analysis (3.3)
        results = self.executor.execute(code)

        # Step 6: Calculate member capacities (3.2)
        design_checks = self.check_member_adequacy(results, structural_json)

        # Step 7: Generate report
        return self.generate_integrated_report(building, results, design_checks)
```

### Phase 4: Testing & Validation

#### 4.1 Test Cases (AISC Benchmarks)
1. **Simple Portal Frame**: 1-story, 1-bay (baseline)
2. **Multi-story Frame**: 3-story, 2-bay frame from AISC examples
3. **Complex Frame**: 7-story frame (like PortalFrame2d example)
4. **Various Load Cases**: Gravity, lateral, combinations

#### 4.2 Validation Metrics
- **Accuracy**: Compare results with hand calculations / commercial software
- **Success Rate**: % of models that execute successfully
- **Code Quality**: % of generated code that passes validation
- **User Experience**: Time from description to results

## Implementation Timeline

### Week 1: Foundation
- [x] Set up OpenSeesPy documentation
- [ ] Implement Geometry Agent
- [ ] Create JSON schema for structural representation

### Week 2: Code Generation
- [ ] Implement Code Translation Agent
- [ ] Create OpenSeesPy code templates
- [ ] Build W-section database

### Week 3: Validation & Execution
- [ ] Implement Model Validation Agent
- [ ] Create OpenSeesPy executor
- [ ] Develop result parser

### Week 4: Integration & Testing
- [ ] Integrate with existing modules (3.1, 3.2)
- [ ] Create unified workflow
- [ ] Run AISC benchmark tests

## Technical Stack

### Core Technologies
- **Python 3.8+**: Main language
- **OpenSeesPy**: Structural analysis engine
- **LLM**: OpenAI/Qwen for agents (already integrated)
- **JSON**: Intermediate representation format

### Key Libraries
- `openseespy`: Structural analysis
- `openai`: LLM integration (existing)
- `pydantic`: Data validation for JSON schemas
- `matplotlib`: Result visualization
- `numpy/pandas`: Data processing

## File Structure
```
LLM_steel_design/
├── openSeesIntegrate/          # NEW: Task 3.3 module
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── geometry_agent.py       # Converts NL → JSON
│   │   ├── code_translator.py      # Converts JSON → OpenSeesPy
│   │   ├── model_validator.py      # Validates generated code
│   │   └── problem_analyzer.py     # Coordinates workflow
│   ├── models/
│   │   ├── structural_json.py      # JSON schema definitions
│   │   └── wsection_database.py    # W-section properties
│   ├── executor/
│   │   ├── opensees_runner.py      # Execute OpenSeesPy models
│   │   └── result_parser.py        # Parse and interpret results
│   ├── templates/
│   │   └── opensees_templates.py   # Code generation templates
│   ├── openseespyDoc/              # Downloaded documentation
│   ├── reference_paper.pdf         # Research paper
│   └── tests/
│       ├── test_geometry_agent.py
│       ├── test_code_translator.py
│       └── benchmark_aisc.py
├── building_design/                # Existing: Task 3.1
├── agent/                          # Existing: Task 3.2
└── integrated_design.py            # Updated: Full integration
```

## Success Criteria

### Minimum Viable Product (MVP)
1. ✅ Successfully generate OpenSeesPy code from natural language for simple frames
2. ✅ Execute generated code without errors
3. ✅ Extract and display key results (displacements, forces)
4. ✅ Integrate with existing modules (3.1, 3.2)

### Full Success (Research-Grade)
1. ✅ 80%+ accuracy on AISC benchmark examples
2. ✅ Handle complex multi-story frames
3. ✅ Provide actionable design recommendations
4. ✅ Complete end-to-end workflow: description → analysis → design check

## Risk Mitigation

### Technical Risks
1. **LLM hallucination**: Use structured prompts, JSON validation
2. **OpenSeesPy convergence**: Include robust analysis settings, fallback strategies
3. **Integration complexity**: Modular design, clear interfaces

### Mitigation Strategies
- Template-based code generation (reduces LLM errors)
- Multi-stage validation (syntax → semantics → structural)
- Comprehensive testing with known examples
- Fallback to simpler models if complex analysis fails

## References

1. Research Paper: "Automating 2D Structural Analysis with Multi-Agent LLMs"
2. OpenSeesPy Documentation: `openseespyDoc/` directory
3. AISC Steel Construction Manual (15th Edition)
4. Example code: `PortalFrame2d.py`, `SteelFrame2D.py`

## Next Steps

1. ✅ Complete this implementation plan
2. [ ] Review plan with team
3. [ ] Start implementation with Geometry Agent
4. [ ] Iterate based on testing feedback

---
**Created**: March 2, 2026
**Author**: Kai Chen
**Status**: Planning Complete → Ready for Implementation
