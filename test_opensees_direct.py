"""
Direct OpenSeesPy test - bypassing code generation
Tests if OpenSeesPy works correctly
"""

from openseespy.opensees import *

print("="*60)
print("Direct OpenSeesPy Test")
print("="*60)

# Clear model
wipe()

# Initialize model
model('basic', '-ndm', 2, '-ndf', 3)
print("\n✓ Model initialized")

# Define nodes (inches)
node(1, 0.0, 0.0)
node(2, 240.0, 0.0)
node(3, 0.0, 144.0)
node(4, 240.0, 144.0)
print("✓ Nodes defined: 4 nodes")

# Boundary conditions
fix(1, 1, 1, 1)
fix(2, 1, 1, 1)
print("✓ Fixed supports at base")

# Geometric transformation
geomTransf('Linear', 1)

# Materials (E in psi)
E = 29000000.0  # 29000 ksi = 29,000,000 psi
A_col = 26.5    # in²
I_col = 999.0   # in⁴
A_beam = 14.7   # in²
I_beam = 984.0  # in⁴

# Elements
element('elasticBeamColumn', 1, 1, 3, A_col, E, I_col, 1)  # Left column
element('elasticBeamColumn', 2, 2, 4, A_col, E, I_col, 1)  # Right column
element('elasticBeamColumn', 3, 3, 4, A_beam, E, I_beam, 1)  # Beam
print("✓ Elements defined: 3 elements")

# Loads (kips)
timeSeries('Linear', 1)
pattern('Plain', 1, 1)
load(3, 0.0, -10.0, 0.0)  # 10 kip downward at node 3
load(4, 0.0, -10.0, 0.0)  # 10 kip downward at node 4
print("✓ Loads applied: 10 kip each at nodes 3 & 4")

# Recorders
recorder('Node', '-file', 'displacements.txt', '-node', 1, 2, 3, 4, '-dof', 1, 2, 3, 'disp')
recorder('Node', '-file', 'reactions.txt', '-node', 1, 2, '-dof', 1, 2, 3, 'reaction')

# Analysis
constraints('Plain')
numberer('RCM')
system('BandGeneral')
test('NormDispIncr', 1.0e-6, 100)
algorithm('Newton')
integrator('LoadControl', 1.0)
analysis('Static')

print("\n" + "="*60)
print("Running analysis...")
print("="*60)

# Perform analysis
ok = analyze(1)

if ok == 0:
    print("\n✓ Analysis completed successfully!")

    # Get displacements
    print("\nDisplacements:")
    for node_id in [3, 4]:
        disp = nodeDisp(node_id)
        print(f"  Node {node_id}: dx={disp[0]:.6f} in, dy={disp[1]:.6f} in")

    # Get reactions
    print("\nReactions:")
    for node_id in [1, 2]:
        react = nodeReaction(node_id)
        print(f"  Node {node_id}: Rx={react[0]:.2f} kip, Fy={react[1]:.2f} kip")

    # Check equilibrium
    total_fy = nodeReaction(1)[1] + nodeReaction(2)[1]
    print(f"\nEquilibrium check:")
    print(f"  Total vertical reaction: {total_fy:.2f} kip")
    print(f"  Total applied load: 20.00 kip")
    print(f"  Difference: {abs(total_fy - 20.0):.6f} kip")

    if abs(total_fy - 20.0) < 0.01:
        print("  ✓ Forces balanced!")

    print("\n" + "="*60)
    print("TEST PASSED!")
    print("="*60)
else:
    print("\n✗ Analysis failed")
    print("="*60)
