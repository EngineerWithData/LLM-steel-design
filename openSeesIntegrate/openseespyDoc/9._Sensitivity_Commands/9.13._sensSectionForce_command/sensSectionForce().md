# sensSectionForce()

# 9.13. sensSectionForce command

sensSectionForce(*eleTag*, *<secNum>*, *dof*, *paramTag*)
:   Returns the current section force sensitivity to a parameter at a specified element and section.

    |  |  |
    | --- | --- |
    | `eleTag` ([int](https://docs.python.org/3/library/functions.html#int)) | element tag |
    | `secNum` ([int](https://docs.python.org/3/library/functions.html#int)) | section number (optional) |
    | `dof` ([int](https://docs.python.org/3/library/functions.html#int)) | specific dof at the element (1 through element force ndf) |
    | `paramTag` ([int](https://docs.python.org/3/library/functions.html#int)) | parameter tag |