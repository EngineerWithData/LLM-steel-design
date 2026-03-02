# analyze()

# 5.9. analyze command

analyze(*numIncr=1*, *dt=0.0*, *dtMin=0.0*, *dtMax=0.0*, *Jd=0*)
:   Perform the analysis. Return `0` if successful, `<0` if **NOT** successful

    |  |  |
    | --- | --- |
    | `numIncr` ([int](https://docs.python.org/3/library/functions.html#int)) | Number of analysis steps to perform. (required except for [PFEM analysis](pfemAnalysis.html#pfem-analysis)) |
    | `dt` ([float](https://docs.python.org/3/library/functions.html#float)) | Time-step increment. (required for Transient analysis and VariableTransient analysis.`) |
    | `dtMin` ([float](https://docs.python.org/3/library/functions.html#float)) | Minimum time steps. (required for VariableTransient analysis) |
    | `dtMax` ([float](https://docs.python.org/3/library/functions.html#float)) | Maximum time steps (required for VariableTransient analysis) |
    | `Jd` ([float](https://docs.python.org/3/library/functions.html#float)) | Number of iterations user would like performed at each step. The variable transient analysis will change current time step if last analysis step took more or less iterations than this to converge (required for VariableTransient analysis) |