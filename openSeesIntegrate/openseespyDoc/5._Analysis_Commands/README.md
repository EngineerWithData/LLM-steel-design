# 5. Analysis Commands

# 5. Analysis Commands

In OpenSees, an analysis is an object which is composed by the aggregation of component objects. It is the component objects which define the type of analysis that is performed on the model. The component classes, as shown in the figure below, consist of the following:

1. ConstraintHandler – determines how the constraint equations are enforced in the analysis – how it handles the boundary conditions/imposed displacements
2. DOF\_Numberer – determines the mapping between equation numbers and degrees-of-freedom
3. Integrator – determines the predictive step for time t+dt
4. SolutionAlgorithm – determines the sequence of steps taken to solve the non-linear equation at the current time step
5. SystemOfEqn/Solver – within the solution algorithm, it specifies how to store and solve the system of equations in the analysis
6. Convergence Test – determines when convergence has been achieved.

Analysis commands

1. [constraints commands](constraints.html)
2. [numberer commands](numberer.html)
3. [system commands](system.html)
4. [test commands](test.html)
5. [algorithm commands](algorithm.html)
6. [integrator commands](integrator.html)
7. [analysis command](analysis.html)
8. [eigen command](eigen.html)
9. [analyze command](analyze.html)
10. [modalProperties Command](modalProperties.html)
11. [responseSpectrumAnalysis Command](responseSpectrumAnalysis.html)