# 6.33. sectionDeformation command

# 6.33. sectionDeformation command

sectionDeformation(*eleTag*, *secNum*, *dof*)
:   Returns the section deformation for a beam-column element. The dof of the section
    depends on the section type. Please check with the section manual.

    |  |  |
    | --- | --- |
    | `eleTag` ([int](https://docs.python.org/3/library/functions.html#int)) | element tag. |
    | `secNum` ([int](https://docs.python.org/3/library/functions.html#int)) | section number, i.e. the Gauss integratio number |
    | `dof` ([int](https://docs.python.org/3/library/functions.html#int)) | the dof of the section |