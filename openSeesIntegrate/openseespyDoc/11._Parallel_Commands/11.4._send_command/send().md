# send()

# 11.4. send command

send(*'-pid'*, *pid*, *\*data*)
:   Send information to another processor.

    |  |  |
    | --- | --- |
    | `pid` ([int](https://docs.python.org/3/library/functions.html#int)) | ID of processor where data is sent to |
    | `data` ([list](https://docs.python.org/3/library/stdtypes.html#list) ([int](https://docs.python.org/3/library/functions.html#int))) | can be a list of integers |
    | `data` ([list](https://docs.python.org/3/library/stdtypes.html#list) ([float](https://docs.python.org/3/library/functions.html#float))) | can be a list of floats |
    | `data` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | can be a string |

Note

[send command](#) and [recv command](recv.html) must match and the order of calling both
commands matters.