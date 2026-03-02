# printA()

# 6.26. printA command

printA(*'-file'*, *filename*, *'-ret'*)
:   print the contents of a FullGeneral system that the integrator creates to the screen or a file if the `'-file'` option is used. If using a static integrator, the resulting matrix is the stiffness matrix. If a transient integrator, it will be some combination of mass and stiffness matrices. The printA command can only be issued after an analyze command.

    |  |  |
    | --- | --- |
    | `filename` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | name of file to which output is sent, by default, print to the screen. (optional) |
    | `'-ret'` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | return the A matrix as a list. (optional) |