# 6.35. sectionFlexibility command

# 6.35. sectionFlexibility command

sectionFlexibility(*eleTag*, *secNum*)
:   Returns the section flexibility matrix for a beam-column element.
    A list of values in the row order will be returned.

    |  |  |
    | --- | --- |
    | `eleTag` ([int](https://docs.python.org/3/library/functions.html#int)) | element tag. |
    | `secNum` ([int](https://docs.python.org/3/library/functions.html#int)) | section number, i.e. the Gauss integration number |