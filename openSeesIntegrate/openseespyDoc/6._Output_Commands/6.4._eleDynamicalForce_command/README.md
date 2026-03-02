# 6.4. eleDynamicalForce command

# 6.4. eleDynamicalForce command

eleDynamicalForce(*eleTag*, *dof=-1*)
:   Returns the elemental dynamic force.

    |  |  |
    | --- | --- |
    | `eleTag` ([int](https://docs.python.org/3/library/functions.html#int)) | element tag. |
    | `dof` ([int](https://docs.python.org/3/library/functions.html#int)) | specific dof at the element, (optional), if no `dof` is provided, a list of values for all dofs is returned. |