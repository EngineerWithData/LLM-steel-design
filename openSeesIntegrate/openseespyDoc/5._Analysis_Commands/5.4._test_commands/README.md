# 5.4. test commands

# 5.4. test commands

test(*testType*, *\*testArgs*)
:   This command is used to construct the LinearSOE and LinearSolver objects to store and solve the test of equations in the analysis.

    |  |  |
    | --- | --- |
    | `testType` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | test type |
    | `testArgs` ([list](https://docs.python.org/3/library/stdtypes.html#list)) | a list of test arguments |

The following contain information about available `testType`:

1. [NormUnbalance](normUnbalance.html)
2. [NormDispIncr](normDispIncr.html)
3. [energyIncr](energyIncr.html)
4. [RelativeNormUnbalance](relativeNormUnbalance.html)
5. [RelativeNormDispIncr](relativeNormDispIncr.html)
6. [RelativeTotalNormDispIncr](relativeTotalNormDispIncr.html)
7. [RelativeEnergyIncr](relativeEnergyIncr.html)
8. [FixedNumIter](fixedNumIter.html)
9. [NormDispAndUnbalance](normDispAndUnbalance.html)
10. [NormDispOrUnbalance](normDispOrUnbalance.html)
11. [PFEM test](pfemTest.html#pfem-test)