# sensitivityAlgorithm()

# 9.8. sensitivityAlgorithm command

sensitivityAlgorithm(*type*)
:   This command is used to create a sensitivity algorithm.

    |  |  |
    | --- | --- |
    | `type` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | the type of the sensitivity algorithm,   * `'-computeAtEachStep'` automatically compute   at the end of each step * `'-compuateByCommand'` compute by   calling `computeGradients`. |