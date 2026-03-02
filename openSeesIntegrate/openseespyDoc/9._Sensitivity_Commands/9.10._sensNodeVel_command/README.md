# 9.10. sensNodeVel command

# 9.10. sensNodeVel command

sensNodeVel(*nodeTag*, *dof*, *paramTag*)
:   Returns the current velocity sensitivity to a parameter at a specified node.

    |  |  |
    | --- | --- |
    | `nodeTag` ([int](https://docs.python.org/3/library/functions.html#int)) | node tag |
    | `dof` ([int](https://docs.python.org/3/library/functions.html#int)) | specific dof at the node (1 through ndf) |
    | `paramTag` ([int](https://docs.python.org/3/library/functions.html#int)) | parameter tag |