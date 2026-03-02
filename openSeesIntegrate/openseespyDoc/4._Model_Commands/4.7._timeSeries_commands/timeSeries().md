# timeSeries()

# 4.7. timeSeries commands

timeSeries(*tsType*, *tsTag*, *\*tsArgs*)
:   This command is used to construct a TimeSeries object which represents the relationship between the time in the domain, \(t\), and the load factor applied to the loads, \(\lambda\), in the load pattern with which the TimeSeries object is associated, i.e. \(\lambda = F(t)\).

    |  |  |
    | --- | --- |
    | `tsType` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | time series type. |
    | `tsTag` ([int](https://docs.python.org/3/library/functions.html#int)) | time series tag. |
    | `tsArgs` ([list](https://docs.python.org/3/library/stdtypes.html#list)) | a list of time series arguments |

The following contain information about available `tsType`:

1. [Constant TimeSeries](constantTs.html)
2. [Linear TimeSeries](linearTs.html)
3. [Trigonometric TimeSeries](trigTs.html)
4. [Triangular TimeSeries](triangleTs.html)
5. [Rectangular TimeSeries](rectTs.html)
6. [Pulse TimeSeries](pulseTs.html)
7. [Path TimeSeries](pathTs.html)