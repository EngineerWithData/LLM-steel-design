"""
OpenSeesPy Executor
Executes OpenSeesPy code and captures results
"""

import os
import sys
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Dict, Optional, Tuple
from io import StringIO
import contextlib


class OpenSeesPyExecutor:
    """
    Executor for OpenSeesPy models with result capture
    """

    def __init__(self, working_dir: Optional[str] = None, timeout: int = 60):
        """
        Initialize executor

        Args:
            working_dir: Working directory for execution (default: temp dir)
            timeout: Execution timeout in seconds
        """
        if working_dir:
            self.working_dir = Path(working_dir)
            self.working_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.working_dir = Path(tempfile.mkdtemp(prefix="opensees_"))

        self.timeout = timeout
        self.last_execution_time = 0

    def execute(
        self,
        code: str,
        save_code: bool = True,
        capture_output: bool = True
    ) -> Dict:
        """
        Execute OpenSeesPy code

        Args:
            code: OpenSeesPy Python code to execute
            save_code: Whether to save code to file
            capture_output: Whether to capture stdout/stderr

        Returns:
            Dictionary with execution results
        """
        start_time = time.time()

        # Save code to file
        code_file = self.working_dir / "model.py"
        if save_code:
            with open(code_file, 'w') as f:
                f.write(code)

        # Execute code
        try:
            if capture_output:
                result = self._execute_with_subprocess(code_file)
            else:
                result = self._execute_inline(code)

            execution_time = time.time() - start_time
            self.last_execution_time = execution_time

            result['execution_time'] = execution_time
            result['working_dir'] = str(self.working_dir)

            # Parse output files if they exist
            if result['success']:
                result['output_files'] = self._collect_output_files()

            return result

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'stdout': '',
                'stderr': str(e),
                'execution_time': time.time() - start_time,
                'working_dir': str(self.working_dir)
            }

    def _execute_with_subprocess(self, code_file: Path) -> Dict:
        """
        Execute code in subprocess

        Args:
            code_file: Path to code file

        Returns:
            Execution result dictionary
        """
        try:
            # Run in subprocess
            process = subprocess.run(
                [sys.executable, str(code_file)],
                cwd=self.working_dir,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            return {
                'success': process.returncode == 0,
                'stdout': process.stdout,
                'stderr': process.stderr,
                'returncode': process.returncode
            }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': f'Execution timeout after {self.timeout} seconds',
                'stdout': '',
                'stderr': 'Timeout',
                'returncode': -1
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'stdout': '',
                'stderr': str(e),
                'returncode': -1
            }

    def _execute_inline(self, code: str) -> Dict:
        """
        Execute code inline (in current process)

        Args:
            code: Python code string

        Returns:
            Execution result dictionary
        """
        # Change to working directory
        old_cwd = os.getcwd()
        os.chdir(self.working_dir)

        # Capture stdout/stderr
        stdout_capture = StringIO()
        stderr_capture = StringIO()

        try:
            with contextlib.redirect_stdout(stdout_capture), \
                 contextlib.redirect_stderr(stderr_capture):

                # Execute code
                exec(code, {'__name__': '__main__'})

            return {
                'success': True,
                'stdout': stdout_capture.getvalue(),
                'stderr': stderr_capture.getvalue(),
                'returncode': 0
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'stdout': stdout_capture.getvalue(),
                'stderr': stderr_capture.getvalue() + f"\n{str(e)}",
                'returncode': 1
            }

        finally:
            os.chdir(old_cwd)

    def _collect_output_files(self) -> Dict[str, Path]:
        """
        Collect generated output files

        Returns:
            Dictionary mapping file type to file path
        """
        output_files = {}

        # Common OpenSees output files
        file_patterns = {
            'node_displacements': 'node_displacements.txt',
            'node_reactions': 'node_reactions.txt',
            'element_forces': 'element_forces.txt',
            'eigenvalues': 'eigenvalues.txt'
        }

        for key, pattern in file_patterns.items():
            file_path = self.working_dir / pattern
            if file_path.exists():
                output_files[key] = file_path

        return output_files

    def execute_and_parse(
        self,
        code: str,
        model_info: Optional[Dict] = None
    ) -> Dict:
        """
        Execute code and parse results

        Args:
            code: OpenSeesPy code
            model_info: Optional model information for result interpretation

        Returns:
            Dictionary with execution results and parsed output
        """
        from .result_parser import ResultParser

        # Execute code
        exec_result = self.execute(code)

        if not exec_result['success']:
            return exec_result

        # Parse results
        parser = ResultParser()
        parsed_results = parser.parse_from_files(
            exec_result.get('output_files', {}),
            model_info
        )

        # Combine results
        exec_result['parsed_results'] = parsed_results

        return exec_result

    def cleanup(self):
        """Clean up working directory"""
        import shutil
        if self.working_dir.exists():
            shutil.rmtree(self.working_dir)


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("OpenSeesPy Executor Demo")
    print("=" * 60)

    # Sample OpenSeesPy code
    sample_code = """
from openseespy.opensees import *
import math

# Initialize model
wipe()
model('basic', '-ndm', 2, '-ndf', 3)

print("Building simple portal frame...")

# Nodes
node(1, 0.0, 0.0)
node(2, 240.0, 0.0)
node(3, 0.0, 144.0)
node(4, 240.0, 144.0)

# Boundary conditions
fix(1, 1, 1, 1)
fix(2, 1, 1, 1)

# Geometric transformation
geomTransf('Linear', 1)

# Materials and sections (steel)
E = 29000000.0  # psi (29000 ksi)
A_col = 26.5    # in²
I_col = 999.0   # in⁴
A_beam = 14.7   # in²
I_beam = 984.0  # in⁴

# Elements
element('elasticBeamColumn', 1, 1, 3, A_col, E, I_col, 1)  # Left column
element('elasticBeamColumn', 2, 2, 4, A_col, E, I_col, 1)  # Right column
element('elasticBeamColumn', 3, 3, 4, A_beam, E, I_beam, 1)  # Beam

# Loads
timeSeries('Linear', 1)
pattern('Plain', 1, 1)
load(3, 0.0, -10.0, 0.0)  # 10 kip downward at node 3
load(4, 0.0, -10.0, 0.0)  # 10 kip downward at node 4

# Recorders
recorder('Node', '-file', 'node_displacements.txt', '-node', 1, 2, 3, 4, '-dof', 1, 2, 3, 'disp')
recorder('Node', '-file', 'node_reactions.txt', '-node', 1, 2, '-dof', 1, 2, 3, 'reaction')

# Analysis
constraints('Plain')
numberer('RCM')
system('BandGeneral')
test('NormDispIncr', 1.0e-6, 100)
algorithm('Newton')
integrator('LoadControl', 1.0)
analysis('Static')

# Perform analysis
print("Running analysis...")
ok = analyze(1)

if ok == 0:
    print("✓ Analysis completed successfully")

    # Print results
    print("\\nDisplacements:")
    for node_id in [3, 4]:
        disp = nodeDisp(node_id)
        print(f"  Node {node_id}: dx={disp[0]:.6f} in, dy={disp[1]:.6f} in")

    print("\\nReactions:")
    for node_id in [1, 2]:
        react = nodeReaction(node_id)
        print(f"  Node {node_id}: Rx={react[0]:.2f} kip, Ry={react[1]:.2f} kip, M={react[2]:.2f} kip-in")
else:
    print("✗ Analysis failed")
"""

    # Execute code
    executor = OpenSeesPyExecutor()

    print("\nExecuting OpenSeesPy code...")
    result = executor.execute(sample_code)

    print(f"\nExecution result: {'✓ SUCCESS' if result['success'] else '✗ FAILED'}")
    print(f"Execution time: {result['execution_time']:.3f} seconds")
    print(f"Working directory: {result['working_dir']}")

    if result['success']:
        print("\n" + "=" * 60)
        print("Output:")
        print("=" * 60)
        print(result['stdout'])

        if result.get('output_files'):
            print("\nGenerated output files:")
            for key, path in result['output_files'].items():
                print(f"  - {key}: {path}")
    else:
        print(f"\nError: {result.get('error', 'Unknown error')}")
        if result['stderr']:
            print(f"stderr: {result['stderr']}")

    # Cleanup
    # executor.cleanup()
    print(f"\n✓ Working directory preserved at: {executor.working_dir}")
    print("=" * 60)
