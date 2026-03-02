# 7.15. setNodeDisp command

# 7.15. setNodeDisp command

setNodeDisp(*nodeTag*, *dof*, *value*, *'-commit'*)
:   set the nodal displacement at the specified DOF.

    |  |  |
    | --- | --- |
    | `nodeTag` ([int](https://docs.python.org/3/library/functions.html#int)) | node tag. |
    | `dof` ([int](https://docs.python.org/3/library/functions.html#int)) | the DOF of the displacement to be set. |
    | `value` ([float](https://docs.python.org/3/library/functions.html#float)) | displacement value |
    | `'-commit'` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | commit nodal state. (optional) |