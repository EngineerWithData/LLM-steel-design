# algorithm()

# 5.5. algorithm commands

algorithm(*algoType*, *\*algoArgs*)
:   This command is used to construct a SolutionAlgorithm object, which determines the sequence of steps taken to solve the non-linear equation.

    |  |  |
    | --- | --- |
    | `algoType` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | algorithm type |
    | `algoArgs` ([list](https://docs.python.org/3/library/stdtypes.html#list)) | a list of algorithm arguments |

The following contain information about available `algoType`:

1. [Linear Algorithm](linearAlgo.html)
2. [Newton Algorithm](newton.html)
3. [Newton with Line Search](newtonLineSearch.html)
4. [Modified Newton Algorithm](modifiedNewton.html)
5. [Krylov-Newton Algorithm](krylovNewton.html)
6. [SecantNewton Algorithm](secantNewton.html)
7. [RaphsonNewton Algorithm](raphsonNewton.html)
8. [PeriodicNewton Algorithm](periodicNewton.html)
9. [BFGS Algorithm](bfgs.html)
10. [Broyden Algorithm](broyden.html)