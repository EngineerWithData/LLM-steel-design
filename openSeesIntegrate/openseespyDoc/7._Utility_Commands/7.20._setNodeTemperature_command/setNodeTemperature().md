# setNodeTemperature()

# 7.20. setNodeTemperature command

setNodeTemperature(*nodeTag*, *value*)
:   set the nodal temperature for [Elastic Pipe Element](pipe.html) and [Curved Pipe Element](curvedPipe.html) elements.

    |  |  |
    | --- | --- |
    | `nodeTag` ([int](https://docs.python.org/3/library/functions.html#int)) | node tag. |
    | `value` ([float](https://docs.python.org/3/library/functions.html#float)) | the temperature value for the node. The nodal temperature will affect the thermal expansion for both [Elastic Pipe Element](pipe.html) and [Curved Pipe Element](curvedPipe.html) elements. |