# constraints()

# 5.1. constraints commands

constraints(*constraintType*, *\*constraintArgs*)
:   This command is used to construct the ConstraintHandler object. The ConstraintHandler object determines how the constraint equations are enforced in the analysis. Constraint equations enforce a specified value for a DOF, or a relationship between DOFs.

    |  |  |
    | --- | --- |
    | `constraintType` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | constraints type |
    | `constraintArgs` ([list](https://docs.python.org/3/library/stdtypes.html#list)) | a list of constraints arguments |

The following contain information about available `constraintType`:

1. [Plain Constraints](PlainConstraint.html)
2. [Lagrange Multipliers](LagrangeMultipliers.html)
3. [Penalty Method](PenaltyMethod.html)
4. [Transformation Method](TransformationMethod.html)