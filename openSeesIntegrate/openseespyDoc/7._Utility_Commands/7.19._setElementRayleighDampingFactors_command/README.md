# 7.19. setElementRayleighDampingFactors command

# 7.19. setElementRayleighDampingFactors command

setElementRayleighDampingFactors(*eleTag*, *alphaM*, *betaK*, *betaK0*, *betaKc*)
:   Set the [`rayleigh()`](reyleigh.html#rayleigh "rayleigh") damping for an element.

    |  |  |
    | --- | --- |
    | `eleTag` ([int](https://docs.python.org/3/library/functions.html#int)) | element tag |
    | `alphaM` ([float](https://docs.python.org/3/library/functions.html#float)) | factor applied to elements or nodes mass matrix |
    | `betaK` ([float](https://docs.python.org/3/library/functions.html#float)) | factor applied to elements current stiffness matrix. |
    | `betaK0` ([float](https://docs.python.org/3/library/functions.html#float)) | factor applied to elements initial stiffness matrix. |
    | `betaKc` ([float](https://docs.python.org/3/library/functions.html#float)) | factor applied to elements committed stiffness matrix. |