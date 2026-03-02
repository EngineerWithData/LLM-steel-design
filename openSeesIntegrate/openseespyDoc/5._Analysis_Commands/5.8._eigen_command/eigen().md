# eigen()

# 5.8. eigen command

eigen(*solver='-genBandArpack'*, *numEigenvalues*)
:   Eigen value analysis. Return a list of eigen values.

    |  |  |
    | --- | --- |
    | numEigenvalues ([int](https://docs.python.org/3/library/functions.html#int)) | number of eigenvalues required |
    | solver ([str](https://docs.python.org/3/library/stdtypes.html#str)) | optional string detailing type of solver: `'-genBandArpack'`, `'-fullGenLapack'`, (optional) |

Note

1. The eigenvectors are stored at the nodes and can be printed out using a Node Recorder, the nodeEigenvector command, or the Print command.
2. The default eigensolver is able to solve only for N-1 eigenvalues, where N is the number of inertial DOFs. When running into this limitation the -fullGenLapack solver can be used instead of the default Arpack solver.
3. The -fullGenLapack option is VERY SLOW for moderate to large models