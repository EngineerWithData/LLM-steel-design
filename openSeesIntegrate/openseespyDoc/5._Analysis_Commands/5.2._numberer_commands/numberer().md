# numberer()

# 5.2. numberer commands

numberer(*numbererType*, *\*numbererArgs*)
:   This command is used to construct the DOF\_Numberer object. The DOF\_Numberer object determines the mapping between equation numbers and degrees-of-freedom – how degrees-of-freedom are numbered.

    |  |  |
    | --- | --- |
    | `numbererType` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | numberer type |
    | `numbererArgs` ([list](https://docs.python.org/3/library/stdtypes.html#list)) | a list of numberer arguments |

The following contain information about available `numbererType`:

1. [Plain Numberer](PlainNumberer.html)
2. [RCM Numberer](RCM.html)
3. [AMD Numberer](AMD.html)
4. [Parallel Plain Numberer](ParallelPlainNumberer.html)
5. [Parallel RCM Numberer](ParallelRCMNumberer.html)