# 6.16. nodeEigenvector command

# 6.16. nodeEigenvector command

nodeEigenvector(*nodeTag*, *eigenvector*, *dof=-1*)
:   Returns the eigenvector at a specified node.

    |  |  |
    | --- | --- |
    | `nodeTag` ([int](https://docs.python.org/3/library/functions.html#int)) | node tag. |
    | `eigenvector` ([int](https://docs.python.org/3/library/functions.html#int)) | mode number of eigenvector to be returned |
    | `dof` ([int](https://docs.python.org/3/library/functions.html#int)) | specific dof at the node (1 through ndf), (optional), if no `dof` is provided, a list of values for all dofs is returned. |