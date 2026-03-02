# nodeReaction()

# 6.20. nodeReaction command

nodeReaction(*nodeTag*, *dof=-1*)
:   Returns the reactions at a specified node. Must call [`reactions()`](reactions.html#reactions "reactions") command before
    this command.

    |  |  |
    | --- | --- |
    | `nodeTag` ([int](https://docs.python.org/3/library/functions.html#int)) | node tag. |
    | `dof` ([int](https://docs.python.org/3/library/functions.html#int)) | specific dof at the node (1 through ndf), (optional), if no `dof` is provided, a list of values for all dofs is returned. |