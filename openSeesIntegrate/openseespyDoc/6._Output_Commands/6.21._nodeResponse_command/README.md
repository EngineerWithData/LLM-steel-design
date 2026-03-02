# 6.21. nodeResponse command

# 6.21. nodeResponse command

nodeResponse(*nodeTag*, *dof*, *responseID*)
:   Returns the responses at a specified node. To get reactions (id=6), must call the `reactions` command before
    this command.

    |  |  |
    | --- | --- |
    | `nodeTag` ([int](https://docs.python.org/3/library/functions.html#int)) | node tag. |
    | `dof` ([int](https://docs.python.org/3/library/functions.html#int)) | specific dof of the response |
    | `responseID` ([int](https://docs.python.org/3/library/functions.html#int)) | the id of responses:   * Disp = 1 * Vel = 2 * Accel = 3 * IncrDisp = 4 * IncrDeltaDisp = 5 * Reaction = 6 * Unbalance = 7 * RayleighForces = 8 |