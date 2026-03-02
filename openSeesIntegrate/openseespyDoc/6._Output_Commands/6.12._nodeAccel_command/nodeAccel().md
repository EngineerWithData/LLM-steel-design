# nodeAccel()

# 6.12. nodeAccel command

nodeAccel(*nodeTag*, *dof=-1*)
:   Returns the current acceleration at a specified node.

    |  |  |
    | --- | --- |
    | `nodeTag` ([int](https://docs.python.org/3/library/functions.html#int)) | node tag. |
    | `dof` ([int](https://docs.python.org/3/library/functions.html#int)) | specific dof at the node (1 through ndf), (optional), if no `dof` is provided, a list of values for all dofs is returned. |