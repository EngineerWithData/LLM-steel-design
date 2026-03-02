# 11.6. Bcast command

# 11.6. Bcast command

Bcast(*\*data*)
:   Broadcast information from processor 0 to all processors.

    |  |  |
    | --- | --- |
    | `data` ([list](https://docs.python.org/3/library/stdtypes.html#list) ([int](https://docs.python.org/3/library/functions.html#int))) | can be a list of integers |
    | `data` ([list](https://docs.python.org/3/library/stdtypes.html#list) ([float](https://docs.python.org/3/library/functions.html#float))) | can be a list of floats |
    | `data` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | can be a string |

Note

Run the same command to receive data sent from pid = 0.

For example,

```python
if pid == 0:

  data1 = []
  data2 = []

  ops.Bcast(*data1)
  ops.Bcast(*data2)

if pid != 0:
  data1 = ops.Bcast()
  data2 = ops.Bcast()
```