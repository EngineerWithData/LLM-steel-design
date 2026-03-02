# frictionModel()

# 4.17. frictionModel commands

frictionModel(*frnType*, *frnTag*, *\*frnArgs*)
:   The frictionModel command is used to construct a friction model object, which specifies the behavior of the coefficient of friction in terms of the absolute sliding velocity and the pressure on the contact area. The command has at least one argument, the friction model type.

    |  |  |
    | --- | --- |
    | `frnType` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | frictionModel type |
    | `frnTag` ([int](https://docs.python.org/3/library/functions.html#int)) | frictionModel tag. |
    | `frnArgs` ([list](https://docs.python.org/3/library/stdtypes.html#list)) | a list of frictionModel arguments, must be preceded with `*`. |

For example,

```python
frnType = 'Coulomb'
frnTag = 1
frnArgs = [mu]
frictionModel(frnType, frnTag, *frnArgs)
```

The following contain information about available `frnType`:

1. [Coulomb](Coulomb.html)
2. [Velocity Dependent Friction](veldependent.html)
3. [Velocity and Normal Force Dependent Friction](velnormal.html)
4. [Velocity and Pressure Dependent Friction](velpressure.html)
5. [Multi-Linear Velocity Dependent Friction](velmulti.html)