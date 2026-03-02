# 7.8. remove command

# 7.8. remove command

remove(*type*, *tag*)
:   This commmand is used to remove components from the model.

    |  |  |
    | --- | --- |
    | `type` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | type of the object, `'ele'`, `'loadPattern'`, `'parameter'`, `'node'`, `'timeSeries'`, `'sp'`, `'mp'`. |
    | `tag` ([int](https://docs.python.org/3/library/functions.html#int)) | tag of the object |

remove(*'recorders'*)
:   Remove all recorder objects.

remove(*'sp'*, *nodeTag*, *dofTag*, *patternTag*)
:   Remove a sp object based on node

    |  |  |
    | --- | --- |
    | `nodeTag` ([int](https://docs.python.org/3/library/functions.html#int)) | node tag |
    | `dof` ([int](https://docs.python.org/3/library/functions.html#int)) | dof the sp constrains |
    | `patternTag` ([int](https://docs.python.org/3/library/functions.html#int)) | pattern tag, (optional) |