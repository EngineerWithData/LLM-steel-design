# 11. Parallel Commands

# 11. Parallel Commands

The parallel commands are currently only
working in the Linux version.
The parallel OpenSeesPy is similar to OpenSeesMP, which
requires users to divide the model
to distributed processors.

You can still run the single-processor version as before.
To run the parallel version, you have
to install a MPI implementation, such as [mpich](https://www.mpich.org/downloads/). Then
call your python scripts in the command line

```python
mpiexec -np np python filename.py
```

where `np` is the number of processors to be used,
`python` is the python interpreter, and
`filename.py` is the script name.

Inside the script, OpenSeesPy is still imported as

```python
import openseespy.opensees as ops
```

Common problems:

1. Unmatch send/recv will cause deadlock.
2. Writing to the same files at the same from different processors will cause race conditions.
3. Poor model decomposition will cause load imbalance problem.

Following are commands related to parallel computing:

1. [getPID command](getPID.html)
2. [getNP command](getNP.html)
3. [barrier command](barrier.html)
4. [send command](send.html)
5. [recv command](recv.html)
6. [Bcast command](Bcast.html)
7. [setStartNodeTag command](setStartNodeTag.html)
8. [domainChange command](domainChange.html)
9. [Parallel Plain Numberer](ParallelPlainNumberer.html)
10. [Parallel RCM Numberer](ParallelRCMNumberer.html)
11. [MUMPS Solver](Mumps.html)
12. [Parallel DisplacementControl](ParallelDisplacementControl.html)
13. [partition command](partition.html)