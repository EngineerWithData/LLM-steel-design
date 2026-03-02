# geomTransf()

# 4.18. geomTransf commands

geomTransf(*transfType*, *transfTag*, *\*transfArgs*)
:   The geometric-transformation command is used to construct a coordinate-transformation (CrdTransf) object, which transforms beam element stiffness and resisting force from the basic system to the global-coordinate system. The command has at least one argument, the transformation type.

    |  |  |
    | --- | --- |
    | `transfType` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | geomTransf type |
    | `transfTag` ([int](https://docs.python.org/3/library/functions.html#int)) | geomTransf tag. |
    | `transfArgs` ([list](https://docs.python.org/3/library/stdtypes.html#list)) | a list of geomTransf arguments, must be preceded with `*`. |

For example,

```python
transfType = 'Linear'
transfTag = 1
transfArgs = []
geomTransf(transfType, transfTag, *transfArgs)
```

The following contain information about available `transfType`:

1. [Linear Transformation](LinearTransf.html)
2. [PDelta Transformation](pdelta.html)
3. [Corotational Transformation](corotational.html)