# 4.9. mass command

# 4.9. mass command

mass(*nodeTag*, *\*massValues*)
:   This command is used to set the mass at a node, replacing any previously defined mass at the node.

    |  |  |
    | --- | --- |
    | `nodeTag` ([int](https://docs.python.org/3/library/functions.html#int)) | integer tag identifying node whose mass is set |
    | `massValues` ([list](https://docs.python.org/3/library/stdtypes.html#list) ([float](https://docs.python.org/3/library/functions.html#float))) | ndf nodal mass values corresponding to each DOF |