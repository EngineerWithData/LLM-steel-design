# recv()

# 11.5. recv command

recv(*'-pid'*, *pid*)
:   Receive information from another processor.

    |  |  |
    | --- | --- |
    | `pid` ([int](https://docs.python.org/3/library/functions.html#int)) | ID of processor where data is received from |
    | `pid` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | if `pid` is `'ANY'`, the processor can receive data from any processor. |

Note

[send command](send.html) and [recv command](#) must match and the order of calling both
commands matters.