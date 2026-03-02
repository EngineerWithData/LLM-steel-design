# 12.1. DiscretizeMember command

# 12.1. DiscretizeMember command

preprocessing.DiscretizeMember.DiscretizeMember(*ndI*, *ndJ*, *numEle*, *eleType*, *integrTag*, *transfTag*, *nodeTag*, *eleTag*)
:   Discretize beam elements between two nodes.

    |  |  |
    | --- | --- |
    | `ndI` ([int](https://docs.python.org/3/library/functions.html#int)) | node tag at I end |
    | `ndJ` ([int](https://docs.python.org/3/library/functions.html#int)) | node tag at J end |
    | `numEle` ([int](https://docs.python.org/3/library/functions.html#int)) | number of element to discretize |
    | `eleType` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | the element type |
    | `integrTag` ([int](https://docs.python.org/3/library/functions.html#int)) | beam integration tag ([beamIntegration commands](beamIntegration.html)) |
    | `transfTag` ([int](https://docs.python.org/3/library/functions.html#int)) | geometric transformation tag ([geomTransf commands](geomTransf.html)) |
    | `nodeTag` ([int](https://docs.python.org/3/library/functions.html#int)) | starting node tag |
    | `eleTag` ([int](https://docs.python.org/3/library/functions.html#int)) | starting element tag |