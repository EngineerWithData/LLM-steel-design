# setNodeVel()

# 7.16. setNodeVel command

setNodeVel(*nodeTag*, *dof*, *value*, *'-commit'*)
:   set the nodal velocity at the specified DOF.

    |  |  |
    | --- | --- |
    | `nodeTag` ([int](https://docs.python.org/3/library/functions.html#int)) | node tag. |
    | `dof` ([int](https://docs.python.org/3/library/functions.html#int)) | the DOF of the velocity to be set. |
    | `value` ([float](https://docs.python.org/3/library/functions.html#float)) | velocity value |
    | `'-commit'` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | commit nodal state. (optional) |