# 9.2. addToParameter command

# 9.2. addToParameter command

addToParameter(*tag*, *<specific parameter args>*)
:   In case that more objects (e.g., element, section) are mapped to an existing parameter,
    the command can be used to relate these additional objects to the specific parameter.

    |  |  |
    | --- | --- |
    | `tag` ([int](https://docs.python.org/3/library/functions.html#int)) | integer tag identifying the parameter. |
    | `<specific parameter args>` | depend on the object in the FE model encapsulating the desired parameters. |