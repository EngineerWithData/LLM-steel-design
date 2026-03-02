# 6.14. nodeCoord command

# 6.14. nodeCoord command

nodeCoord(*nodeTag*, *dim=-1*)
:   Returns the coordinates of a specified node.

    |  |  |
    | --- | --- |
    | `nodeTag` ([int](https://docs.python.org/3/library/functions.html#int)) | node tag. |
    | `dof` ([int](https://docs.python.org/3/library/functions.html#int)) | specific dimension at the node (1 through ndf), (optional), if no `dim` is provided, a list of values for all dimensions is returned. |