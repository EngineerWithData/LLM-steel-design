# setNodeAccel()

# 7.17. setNodeAccel command

setNodeAccel(*nodeTag*, *dof*, *value*, *'-commit'*)
:   set the nodal acceleration at the specified DOF.

    |  |  |
    | --- | --- |
    | `nodeTag` ([int](https://docs.python.org/3/library/functions.html#int)) | node tag. |
    | `dof` ([int](https://docs.python.org/3/library/functions.html#int)) | the DOF of the acceleration to be set. |
    | `value` ([float](https://docs.python.org/3/library/functions.html#float)) | acceleration value |
    | `'-commit'` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | commit nodal state. (optional) |