"""
Comprehensive tests for OpenSeesPy integration module (Task 3.3)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from openSeesIntegrate.models.structural_json import (
    StructuralModel, Node, Element, Material, Section, Load,
    GeometricTransformation, AnalysisSettings
)
from openSeesIntegrate.agents.model_validator import ModelValidationAgent, ValidationResult
from openSeesIntegrate.agents.code_translator import CodeTranslationAgent
from openSeesIntegrate.models.wsection_database import (
    get_section_properties, recommend_section_for_column,
    recommend_section_for_beam, search_sections_by_area
)


class TestStructuralModel:
    """Test structural model creation and validation"""

    def test_simple_portal_frame(self):
        """Test creating a simple portal frame model"""
        model = StructuralModel(
            structure_type='2D_frame',
            units={'length': 'ft', 'force': 'kip'},
            ndm=2, ndf=3,
            nodes=[
                Node(id=1, x=0, y=0, constraints=[1,1,1]),
                Node(id=2, x=20, y=0, constraints=[1,1,1]),
                Node(id=3, x=0, y=12, constraints=[0,0,0]),
                Node(id=4, x=20, y=12, constraints=[0,0,0]),
            ],
            materials=[Material(id=1, type='steel', E=29000, fy=50)],
            sections=[
                Section(name='W14X90', A=26.5, I=999),
                Section(name='W21X50', A=14.7, I=984),
            ],
            elements=[
                Element(id=1, type='elasticBeamColumn', nodes=[1,3], section='W14X90'),
                Element(id=2, type='elasticBeamColumn', nodes=[2,4], section='W14X90'),
                Element(id=3, type='elasticBeamColumn', nodes=[3,4], section='W21X50'),
            ],
            loads=[
                Load(type='point', node=3, direction='Y', magnitude=-10.0),
                Load(type='point', node=4, direction='Y', magnitude=-10.0),
            ],
            analysis={'type':'static','steps':1}
        )

        assert len(model.nodes) == 4
        assert len(model.elements) == 3
        assert len(model.loads) == 2
        assert model.structure_type == '2D_frame'

    def test_model_dump(self):
        """Test Pydantic V2 model_dump"""
        model = StructuralModel(
            structure_type='2D_frame',
            units={'length': 'ft', 'force': 'kip'},
            ndm=2, ndf=3,
            nodes=[Node(id=1, x=0, y=0, constraints=[1,1,1])],
            materials=[Material(id=1, type='steel', E=29000, fy=50)],
            sections=[Section(name='W14X90', A=26.5, I=999)],
            elements=[],
            loads=[],
            analysis={'type':'static','steps':1}
        )

        d = model.model_dump()
        assert isinstance(d, dict)
        assert 'nodes' in d
        assert 'elements' in d

    def test_duplicate_node_ids(self):
        """Test validation catches duplicate node IDs"""
        with pytest.raises(ValueError, match="Node IDs must be unique"):
            StructuralModel(
                structure_type='2D_frame',
                units={'length': 'ft', 'force': 'kip'},
                ndm=2, ndf=3,
                nodes=[
                    Node(id=1, x=0, y=0, constraints=[1,1,1]),
                    Node(id=1, x=10, y=0, constraints=[1,1,1]),  # Duplicate ID
                ],
                materials=[Material(id=1, type='steel', E=29000, fy=50)],
                sections=[Section(name='W14X90', A=26.5, I=999)],
                elements=[],
                loads=[],
                analysis={'type':'static','steps':1}
            )

    def test_nonexistent_node_reference(self):
        """Test validation catches elements referencing nonexistent nodes"""
        with pytest.raises(ValueError, match="references non-existent node"):
            StructuralModel(
                structure_type='2D_frame',
                units={'length': 'ft', 'force': 'kip'},
                ndm=2, ndf=3,
                nodes=[Node(id=1, x=0, y=0, constraints=[1,1,1])],
                materials=[Material(id=1, type='steel', E=29000, fy=50)],
                sections=[Section(name='W14X90', A=26.5, I=999)],
                elements=[
                    Element(id=1, type='elasticBeamColumn', nodes=[1,99], section='W14X90')  # Node 99 doesn't exist
                ],
                loads=[],
                analysis={'type':'static','steps':1}
            )


class TestModelValidator:
    """Test model validation agent"""

    @pytest.fixture
    def validator(self):
        return ModelValidationAgent()

    @pytest.fixture
    def valid_model(self):
        return StructuralModel(
            structure_type='2D_frame',
            units={'length': 'ft', 'force': 'kip'},
            ndm=2, ndf=3,
            nodes=[
                Node(id=1, x=0, y=0, constraints=[1,1,1]),
                Node(id=2, x=20, y=0, constraints=[1,1,1]),
                Node(id=3, x=0, y=12, constraints=[0,0,0]),
                Node(id=4, x=20, y=12, constraints=[0,0,0]),
            ],
            materials=[Material(id=1, type='steel', E=29000, fy=50)],
            sections=[Section(name='W14X90', A=26.5, I=999)],
            elements=[
                Element(id=1, type='elasticBeamColumn', nodes=[1,3], section='W14X90'),
                Element(id=2, type='elasticBeamColumn', nodes=[2,4], section='W14X90'),
                Element(id=3, type='elasticBeamColumn', nodes=[3,4], section='W14X90'),
            ],
            loads=[Load(type='point', node=3, direction='Y', magnitude=-10.0)],
            analysis={'type':'static','steps':1}
        )

    def test_valid_model_passes(self, validator, valid_model):
        """Test that a valid model passes validation"""
        result = validator.validate_model(valid_model)
        assert result.is_valid
        assert len(result.errors) == 0

    def test_insufficient_constraints(self, validator):
        """Test validation catches insufficient boundary constraints"""
        model = StructuralModel(
            structure_type='2D_frame',
            units={'length': 'ft', 'force': 'kip'},
            ndm=2, ndf=3,
            nodes=[
                Node(id=1, x=0, y=0, constraints=[0,0,0]),  # No constraints
                Node(id=2, x=20, y=0, constraints=[0,0,0]),
            ],
            materials=[Material(id=1, type='steel', E=29000, fy=50)],
            sections=[Section(name='W14X90', A=26.5, I=999)],
            elements=[Element(id=1, type='elasticBeamColumn', nodes=[1,2], section='W14X90')],
            loads=[],
            analysis={'type':'static','steps':1}
        )

        result = validator.validate_model(model)
        assert not result.is_valid
        assert any('boundary constraint' in e.lower() for e in result.errors)

    def test_isolated_node_detection(self, validator):
        """Test validation detects isolated nodes"""
        model = StructuralModel(
            structure_type='2D_frame',
            units={'length': 'ft', 'force': 'kip'},
            ndm=2, ndf=3,
            nodes=[
                Node(id=1, x=0, y=0, constraints=[1,1,1]),
                Node(id=2, x=20, y=0, constraints=[1,1,1]),
                Node(id=3, x=10, y=10, constraints=[0,0,0]),  # Isolated node
            ],
            materials=[Material(id=1, type='steel', E=29000, fy=50)],
            sections=[Section(name='W14X90', A=26.5, I=999)],
            elements=[Element(id=1, type='elasticBeamColumn', nodes=[1,2], section='W14X90')],
            loads=[],
            analysis={'type':'static','steps':1}
        )

        result = validator.validate_model(model)
        assert not result.is_valid
        assert any('isolated' in e.lower() for e in result.errors)

    def test_code_syntax_validation(self, validator):
        """Test code syntax validation"""
        valid_code = """
from openseespy.opensees import *
wipe()
model('basic', '-ndm', 2, '-ndf', 3)
node(1, 0.0, 0.0)
"""
        result = validator.validate_code(valid_code)
        assert result.is_valid

        invalid_code = "def foo(:\n    pass"  # Syntax error
        result = validator.validate_code(invalid_code)
        assert not result.is_valid
        assert any('syntax' in e.lower() for e in result.errors)


class TestCodeTranslator:
    """Test code translation agent"""

    @pytest.fixture
    def translator(self):
        return CodeTranslationAgent()

    @pytest.fixture
    def simple_model(self):
        return StructuralModel(
            structure_type='2D_frame',
            units={'length': 'ft', 'force': 'kip'},
            ndm=2, ndf=3,
            nodes=[
                Node(id=1, x=0, y=0, constraints=[1,1,1]),
                Node(id=2, x=20, y=0, constraints=[1,1,1]),
                Node(id=3, x=0, y=12, constraints=[0,0,0]),
                Node(id=4, x=20, y=12, constraints=[0,0,0]),
            ],
            materials=[Material(id=1, type='steel', E=29000, fy=50)],
            sections=[Section(name='W14X90', A=26.5, I=999), Section(name='W21X50', A=14.7, I=984)],
            elements=[
                Element(id=1, type='elasticBeamColumn', nodes=[1,3], section='W14X90'),
                Element(id=2, type='elasticBeamColumn', nodes=[2,4], section='W14X90'),
                Element(id=3, type='elasticBeamColumn', nodes=[3,4], section='W21X50'),
            ],
            loads=[
                Load(type='point', node=3, direction='Y', magnitude=-10.0),
                Load(type='point', node=4, direction='Y', magnitude=-10.0),
            ],
            analysis={'type':'static','steps':1}
        )

    def test_code_generation(self, translator, simple_model):
        """Test basic code generation"""
        code = translator.translate(simple_model)

        assert isinstance(code, str)
        assert len(code) > 0
        assert 'from openseespy.opensees import *' in code
        assert 'wipe()' in code
        assert "model('basic'" in code

    def test_generated_code_syntax(self, translator, simple_model):
        """Test generated code has valid Python syntax"""
        import ast
        code = translator.translate(simple_model)

        # Should not raise SyntaxError
        ast.parse(code)

    def test_node_generation(self, translator, simple_model):
        """Test node commands are generated correctly"""
        code = translator.translate(simple_model)

        # Check all nodes are present
        assert 'node(1,' in code
        assert 'node(2,' in code
        assert 'node(3,' in code
        assert 'node(4,' in code

        # Check boundary conditions
        assert 'fix(1, 1, 1, 1)' in code
        assert 'fix(2, 1, 1, 1)' in code

    def test_element_generation(self, translator, simple_model):
        """Test element commands are generated correctly"""
        code = translator.translate(simple_model)

        # Check elements are present
        assert "element('elasticBeamColumn', 1," in code
        assert "element('elasticBeamColumn', 2," in code
        assert "element('elasticBeamColumn', 3," in code

    def test_load_generation(self, translator, simple_model):
        """Test load commands are generated correctly"""
        code = translator.translate(simple_model)

        # Check loads are present and NOT indented (bug fix verification)
        load_lines = [l for l in code.splitlines() if 'load(' in l and '# Node' in l]
        assert len(load_lines) == 2

        # Verify loads are at top level (not indented)
        for line in load_lines:
            assert not line.startswith(' '), f"Load command should not be indented: {line}"

    def test_analysis_generation(self, translator, simple_model):
        """Test analysis commands are generated"""
        code = translator.translate(simple_model)

        assert "constraints('Plain')" in code
        assert "numberer('RCM')" in code
        assert "system('BandGeneral')" in code
        assert "algorithm('Newton')" in code
        assert "analyze(" in code


class TestWSectionDatabase:
    """Test W-section database"""

    def test_get_section_properties(self):
        """Test retrieving section properties"""
        section = get_section_properties('W14X90')

        assert section is not None
        assert section.name == 'W14X90'
        assert section.A == 26.5
        assert section.Ix == 999
        assert section.weight == 90

    def test_section_name_normalization(self):
        """Test section name normalization"""
        # Different formats should all work
        assert get_section_properties('W14X90') is not None
        assert get_section_properties('W14x90') is not None
        assert get_section_properties('w14x90') is not None
        assert get_section_properties('14X90') is not None

    def test_nonexistent_section(self):
        """Test retrieving nonexistent section"""
        section = get_section_properties('W99X999')
        assert section is None

    def test_search_by_area(self):
        """Test searching sections by area"""
        sections = search_sections_by_area(20, 30)

        assert len(sections) > 0
        for section in sections:
            assert 20 <= section.A <= 30

        # Should be sorted by area
        areas = [s.A for s in sections]
        assert areas == sorted(areas)

    def test_recommend_column_section(self):
        """Test column section recommendation"""
        section = recommend_section_for_column(required_area=15, required_Ix=500)

        assert section is not None
        assert section.A >= 15
        assert section.Ix >= 500

    def test_recommend_beam_section(self):
        """Test beam section recommendation"""
        section = recommend_section_for_beam(required_Zx=100, max_depth=22)

        assert section is not None
        assert section.Zx >= 100
        assert section.d <= 22


class TestEndToEndIntegration:
    """Test complete end-to-end workflow"""

    def test_complete_workflow(self):
        """Test complete workflow from model to code"""
        # Create model
        model = StructuralModel(
            structure_type='2D_frame',
            units={'length': 'ft', 'force': 'kip'},
            ndm=2, ndf=3,
            nodes=[
                Node(id=1, x=0, y=0, constraints=[1,1,1]),
                Node(id=2, x=20, y=0, constraints=[1,1,1]),
                Node(id=3, x=0, y=12, constraints=[0,0,0]),
                Node(id=4, x=20, y=12, constraints=[0,0,0]),
            ],
            materials=[Material(id=1, type='steel', E=29000, fy=50)],
            sections=[Section(name='W14X90', A=26.5, I=999), Section(name='W21X50', A=14.7, I=984)],
            elements=[
                Element(id=1, type='elasticBeamColumn', nodes=[1,3], section='W14X90'),
                Element(id=2, type='elasticBeamColumn', nodes=[2,4], section='W14X90'),
                Element(id=3, type='elasticBeamColumn', nodes=[3,4], section='W21X50'),
            ],
            loads=[
                Load(type='point', node=3, direction='Y', magnitude=-10.0),
                Load(type='point', node=4, direction='Y', magnitude=-10.0),
            ],
            analysis={'type':'static','steps':1}
        )

        # Validate model
        validator = ModelValidationAgent()
        model_result = validator.validate_model(model)
        assert model_result.is_valid, f"Model validation failed: {model_result.errors}"

        # Translate to code
        translator = CodeTranslationAgent()
        code = translator.translate(model)
        assert len(code) > 0

        # Validate code
        code_result = validator.validate_code(code, model)
        assert code_result.is_valid, f"Code validation failed: {code_result.errors}"

        # Verify syntax
        import ast
        ast.parse(code)  # Should not raise


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
