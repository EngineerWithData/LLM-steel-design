# 4.6. pressureConstraint command

# 4.6. pressureConstraint command

pressureConstraint(*nodeTag*, *pNodeTag*)
:   Create a pressure constraint for incompressible flow.

    |  |  |
    | --- | --- |
    | `nodeTag` ([int](https://docs.python.org/3/library/functions.html#int)) | tag of node to be constrained |
    | `pNodeTag` ([int](https://docs.python.org/3/library/functions.html#int)) | tag of extra pressure node, which must exist before calling this command |

For example,

```python
ops.node(1, 0.0, 0.0)
ops.node(2, 0.0, 0.0, '-ndf', 1)
ops.pressureConstraint(1, 2)
```