# rayleigh()

# 4.11. rayleigh command

rayleigh(*alphaM*, *betaK*, *betaKinit*, *betaKcomm*)
:   This command is used to assign damping to all previously-defined elements and nodes. When using rayleigh damping in OpenSees, the damping matrix for an element or node, D is specified as a combination of stiffness and mass-proportional damping matrices:

    \[D = \alpha\_M \* M + \beta\_K \* K\_{curr} + \beta\_{Kinit} \* K\_{init} + \beta\_{Kcomm} \* K\_{commit}\]

    |  |  |
    | --- | --- |
    | `alphaM` ([float](https://docs.python.org/3/library/functions.html#float)) | factor applied to elements or nodes mass matrix |
    | `betaK` ([float](https://docs.python.org/3/library/functions.html#float)) | factor applied to elements current stiffness matrix. |
    | `betaKinit` ([float](https://docs.python.org/3/library/functions.html#float)) | factor applied to elements initial stiffness matrix. |
    | `betaKcomm` ([float](https://docs.python.org/3/library/functions.html#float)) | factor applied to elements committed stiffness matrix. |