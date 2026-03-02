# model()

# 4.1. model command

model(*'basic'*, *'-ndm'*, *ndm*, *'-ndf'*, *ndf=ndm\*(ndm+1)/2*)
:   Set the default model dimensions and number of dofs.

    |  |  |
    | --- | --- |
    | `ndm` ([int](https://docs.python.org/3/library/functions.html#int)) | number of dimensions (1,2,3) |
    | `ndf` ([int](https://docs.python.org/3/library/functions.html#int)) | number of dofs (optional) |