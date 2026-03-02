# node()

# 4.3. node command

node(*nodeTag*, *\*crds*, *'-ndf'*, *ndf*, *'-mass'*, *\*mass*, *'-disp'*, *\*disp*, *'-vel'*, *\*vel*, *'-accel'*, *\*accel*)
:   Create a OpenSees node.

    |  |  |
    | --- | --- |
    | `nodeTag` ([int](https://docs.python.org/3/library/functions.html#int)) | node tag. |
    | `crds` ([list](https://docs.python.org/3/library/stdtypes.html#list) ([float](https://docs.python.org/3/library/functions.html#float))) | nodal coordinates. |
    | `ndf` ([float](https://docs.python.org/3/library/functions.html#float)) | nodal ndf. (optional) |
    | `mass` ([list](https://docs.python.org/3/library/stdtypes.html#list) ([float](https://docs.python.org/3/library/functions.html#float))) | nodal mass. (optional) |
    | `vel` ([list](https://docs.python.org/3/library/stdtypes.html#list) ([float](https://docs.python.org/3/library/functions.html#float))) | nodal velocities. (optional) |
    | `accel` ([list](https://docs.python.org/3/library/stdtypes.html#list) ([float](https://docs.python.org/3/library/functions.html#float))) | nodal accelerations. (optional) |