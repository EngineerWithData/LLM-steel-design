# 5.3. system commands

# 5.3. system commands

system(*systemType*, *\*systemArgs*)
:   This command is used to construct the LinearSOE and LinearSolver objects to store and solve the system of equations in the analysis.

    |  |  |
    | --- | --- |
    | `systemType` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | system type |
    | `systemArgs` ([list](https://docs.python.org/3/library/stdtypes.html#list)) | a list of system arguments |

The following contain information about available `systemType`:

1. [BandGeneral SOE](BandGen.html)
2. [BandSPD SOE](BandSPD.html)
3. [ProfileSPD SOE](ProfileSPD.html)
4. [SuperLU SOE](SuperLU.html)
5. [UmfPack SOE](UmfPack.html)
6. [FullGeneral SOE](FullGeneral.html)
7. [SparseSYM SOE](SparseSYM.html)
8. [PFEM SOE](pfemSystem.html#pfem-system)
9. [MUMPS Solver](Mumps.html)