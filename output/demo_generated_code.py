"""
Auto-generated OpenSeesPy Model
Structure Type: 2D_frame
Units: ft (length), kip (force)
"""

from openseespy.opensees import *
import numpy as np

# Clear any existing model
wipe()

print("=" * 60)
print("OpenSeesPy Structural Analysis")
print("=" * 60)
print(f"Structure: 2D_frame")
print(f"Nodes: 4")
print(f"Elements: 3")
print("=" * 60)

# Model initialization
model('basic', '-ndm', 2, '-ndf', 3)
print("\n[1/7] Model initialized")

# Material definitions
uniaxialMaterial('Elastic', 1, 29000000.0)  # Material 1: STEEL, E=29000.0 ksi
print("[2/7] Materials defined")

# Node definitions
node(1, 0.00, 0.00)
node(2, 240.00, 0.00)
node(3, 0.00, 144.00)
node(4, 240.00, 144.00)

# Boundary conditions
fix(1, 1, 1, 1)  # Node 1
fix(2, 1, 1, 1)  # Node 2
print("[3/7] Nodes and boundary conditions defined")

# Geometric transformations
geomTransf('Linear', 1)  # Linear transformation
print("[4/7] Geometric transformations defined")

# Element definitions
element('elasticBeamColumn', 1, 1, 3, 26.500, 29000000.0, 999.0, 1)  # W14X90, N/A
element('elasticBeamColumn', 2, 2, 4, 26.500, 29000000.0, 999.0, 1)  # W14X90, N/A
element('elasticBeamColumn', 3, 3, 4, 14.700, 29000000.0, 984.0, 1)  # W21X50, N/A
print("[5/7] Elements defined")

# Load definitions
timeSeries('Linear', 1)
pattern('Plain', 1, 1)
    load(3, 0.0, -10.00, 0.0)  # Node 3, DOF 2
    load(4, 0.0, -10.00, 0.0)  # Node 4, DOF 2
print("[6/7] Loads defined")

# Recorders for results
recorder('Node', '-file', 'node_displacements.txt', '-time', '-node', *range(1, 5), '-dof', 1, 2, 3, 'disp')
recorder('Node', '-file', 'node_reactions.txt', '-time', '-node', *range(1, 5), '-dof', 1, 2, 3, 'reaction')
recorder('Element', '-file', 'element_forces.txt', '-time', '-ele', *range(1, 4), 'forces')

# Analysis setup
constraints('Plain')
numberer('RCM')
system('BandGeneral')
test('NormDispIncr', 1e-06, 100)
algorithm('Newton')
integrator('LoadControl', 1.0)
analysis('Static')

# Perform analysis
print("[7/7] Running static analysis...")
ok = analyze(1)

if ok == 0:
    print('✓ Analysis completed successfully')
else:
    print('✗ Analysis failed')


# Output results
print("\n" + "=" * 60)
print("Analysis Results")
print("=" * 60)

# Maximum displacements
max_disp_x = 0.0
max_disp_y = 0.0
max_disp_node = 0

for node_id in range(1, 5):
    disp = nodeDisp(node_id)
    if abs(disp[0]) > abs(max_disp_x):
        max_disp_x = disp[0]
    if abs(disp[1]) > abs(max_disp_y):
        max_disp_y = disp[1]
        max_disp_node = node_id

print(f"Max displacement X: {max_disp_x:.6f} in")
print(f"Max displacement Y: {max_disp_y:.6f} in")
print(f"At node: {max_disp_node}")

# Reactions at supports
print("\nSupport Reactions:")
for node in [1, 2]:
    reactions = nodeReaction(node)
    print(f'  Node {node}: Fx={reactions[0]:.2f} kip, Fy={reactions[1]:.2f} kip, M={reactions[2]:.2f} kip-ft')

print("\n✓ Analysis complete. Results saved to output files.")
print("=" * 60)