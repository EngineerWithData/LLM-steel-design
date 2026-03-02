# modalProperties()

# 5.10. modalProperties Command

This command is used to compute the modal properties of a model after an [eigen command](eigen.html).

This command computes the following modal properties:

> * \(m\_t\) : A vector with the total mass of the structure for each DOF, considering both free and fixed DOFs.
> * \(m\_f\) : The total mass of the structure, but considering only the masses at free DOFs.
> * \(CoM\) : The center of mass.
> * \(gm\) : The generalized mass matrix.
> * \(MPF\) : The modal participation factors.
> * \(MPM\) : The modal participation masses.
> * \(MPMc\) : The cumulative modal participation masses.
> * \(MPM\left(\%\right)\) : The modal participation masse ratios.
> * \(MPMc\left(\%\right)\) : The cumulative modal participation masse ratios.

modalProperties(*<'-print'>*, *<'-file'*, *reportFileName>*, *<'-unorm'>*, *<'-return'>*)

| Argument | Type | Description |
| --- | --- | --- |
| `'-print'` | ([str](https://docs.python.org/3/library/stdtypes.html#str)) | Optional. If included, a report of the modal properties is printed to the console. |
| `'-file'` | ([str](https://docs.python.org/3/library/stdtypes.html#str)) | Optional. If included, a report of the modal properties is printed to the file `reportFileName`. |
| `reportFileName` | ([str](https://docs.python.org/3/library/stdtypes.html#str)) | Optional, but mandatory if the -file option is included. Indicates the filename for the report. If the file does not exist, it will be created. If the file exists, it will be overwritten. |
| `'-unorm'` | ([str](https://docs.python.org/3/library/stdtypes.html#str)) | Optional. If included, the computation of the modal properties will be carried out using a displacement-normalized version of the eigenvectors. |
| `'-return'` | ([str](https://docs.python.org/3/library/stdtypes.html#str)) | Optional. If included, a report of the modal properties will be returned as a dict object to Python. |

Return value with `'-return'` (In next version 3.4.0.3 or later)

```python
{
   # list of one int value
   "domainSize": [ndm],

   # list of lambda values for all modes
   "eigenLambda": [lambdas],

   # list of omega values for all modes
   "eigenOmega": [omega],

   # list of frequency values for all modes
   "eigenFrequency": [frequency],

   # list of period values for all modes
   "eigenPeriod": [period],

   # list of total mass values, [MX] for 1D, [MX, MY, RMZ] for 2D,
   # [MX, MY, MZ, MRX, RMY, RMZ] for 3D
   "totalMass": [mass],

   # list of total mass values for free DOFs, [MX] for 1D,
   # [MX, MY, RMZ] for 2D,  [MX, MY, MZ, MRX, RMY, RMZ] for 3D
   "totalFreeMass": [mass],

   # coordinates of mass center, [X] for 1D, [X, Y] for 2D,
   # [X, Y, Z] for 3D
   "centerOfMass": [center],

   #
   # modal participation factors for all modes
   #

   # for MX direction for 1D, 2D and 3D
   "partiFactorMX": [factor],

   # for MY direction for 2D and 3D
   "partiFactorMY": [factor],

   # for MZ direction for 3D
   "partiFactorMZ": [factor],

   # for RMX direction for 3D
   "partiFactorRMX": [factor],

   # for RMY direction for 3D
   "partiFactorRMY": [factor],

   # for RMZ direction for 2D and 3D
   "partiFactorRMX": [factor],

   #
   # modal participation masses for all modes
   #

   # for MX direction for 1D, 2D and 3D
   "partiMassMX": [mass],

   # for MY direction for 2D and 3D
   "partiMassMY": [mass],

   # for MZ direction for 3D
   "partiMassMZ": [mass],

   # for RMX direction for 3D
   "partiMassRMX": [mass],

   # for RMY direction for 3D
   "partiMassRMY": [mass],

   # for RMZ direction for 2D and 3D
   "partiMassRMX": [mass],

   #
   # modal participation masses (cumulative) for all modes
   #

   # for MX direction for 1D, 2D and 3D
   "partiMassesCumuMX": [mass],

   # for MY direction for 2D and 3D
   "partiMassesCumuMY": [mass],

   # for MZ direction for 3D
   "partiMassesCumuMZ": [mass],

   # for RMX direction for 3D
   "partiMassesCumuRMX": [mass],

   # for RMY direction for 3D
   "partiMassesCumuRMY": [mass],

   # for RMZ direction for 2D and 3D
   "partiMassesCumuRMZ": [mass],

   #
   # modal participation mass ratios (%) for all modes
   #

   # for MX direction for 1D, 2D and 3D
   "partiMassRatiosMX": [mass],

   # for MY direction for 2D and 3D
   "partiMassRatiosMY": [mass],

   # for MZ direction for 3D
   "partiMassRatiosMZ": [mass],

   # for RMX direction for 3D
   "partiMassRatiosRMX": [mass],

   # for RMY direction for 3D
   "partiMassRatiosRMY": [mass],

   # for RMZ direction for 2D and 3D
   "partiMassRatiosRMX": [mass],

   #
   # modal participation mass ratios (%) (cumulative) for all modes
   #

   # for MX direction for 1D, 2D and 3D
   "partiMassRatiosCumuMX": [mass],

   # for MY direction for 2D and 3D
   "partiMassRatiosCumuMY": [mass],

   # for MZ direction for 3D
   "partiMassRatiosCumuMZ": [mass],

   # for RMX direction for 3D
   "partiMassRatiosCumuRMX": [mass],

   # for RMY direction for 3D
   "partiMassRatiosCumuRMY": [mass],

   # for RMZ direction for 2D and 3D
   "partiMassRatiosCumuRMX": [mass],
}
```

Note

* This command can be used only if a previous call to [eigen command](eigen.html) has been performed.
* This command has only optional arguments, and they can be given in any order. Note, however, that the only requirement is that the `reportFileName` must follow the `'-file'` option if used.
* The modal properties are computed and stored in the `Domain` object, so that they can be accessed later in the [responseSpectrumAnalysis Command](responseSpectrumAnalysis.html).
* This command directly accesses the mass matrix of the model, so it accounts for both nodal masses and element’s (distributed) masses. And the element mass matrix can be either lumped or consistent.
* The global mass matrix is then stored into a temporary sparse matrix storage, so it can be used for both small and large models.
* This command can be used for both 2D problems (-ndm = 2, -ndf = 2 or 3) and 3D problems (-ndm = 3, -ndf = 3, 4 or 6). In both cases the algorithm computes rotational masses. If a node has rotational DOFs, the rotational masses account for both the direct rotational masses (i.e. those input by the user at rotational DOFs) and the effect of translational masses gyrating about the center of mass. If a node has no rotational DOF, only the latter is considered.
* Only the values in \(gm\) and \(MPF\) depend on the normalization of the eigenvectors. This normalization depends on the solver used in the [eigen command](eigen.html). The default `'-genBandArpack'` uses a mass-normalization, so that the \(gm\) is the identity. On the contrary, the `'-fullGenLapack'` uses a displacement-normalization, so that the largest component of the eigenvector is 1. If you use the `'-genBandArpack'`, but want a displacement-normalization of the eigenvectors, use the `'-unorm'` option.

## 5.10.1. Theory

The eigenvalues \(\lambda\) and the eigenvectors \(\Phi\) can be obtained after solving the *generalized eigenvalue problem* for two symmetric matrices \(K\) (stiffness) and \(M\) (mass) given by:

\[\left (K - \lambda M \right ) \Phi = 0\]

The global mass matrix \(M\) is given by the assembly of \(n\) elemental and nodal mass matrices \(m\_e\):

\[M = \bigwedge\_{i=1}^{n}m\_e\]

\(M\) is not necessarily diagonal, because some elemental matrices \(m\_e\) may be consistent. However, the computation of \(CoM\), \(m\_t\) and \(m\_f\) requires a lumped version of \(M\). The global lumped mass matrix \(LM\) can be computed by the assembly of a diagonalized version of the elemental mass matrices \(m\_e\):

\[LM = \bigwedge\_{i=1}^{n}diag\left(m\_e\right)\]

\(diag\left(m\_e\right)\) cannot be computed just by summing the summing the components of each row (in beams or solid with higher order interpolation, this would produces negative terms on the diagonal mass matrix that would be unphysical).

Instead we use the **HRZ** algorithm [[HintonEtAl1976]](#hintonetal1976), named after the authors Hinton, Rock and Zienkiewicz: *“The procedure of lumping recommended in view of the infinite possibilities offered by condition (5) is to compute the diagonal terms of the consistent mass matrix and then scale these terms so as to preserve the total mass of the element”*.

The procedure is as follows:

> * compute \(DM\), a vector containing the sum of each row of \(m\_e\).
> * compute \(SM\), a vector of size=ndf, obtained summing the components in \(DM\) pertaining to the same DOF (i to ndf). This procedures allows to obtain the total elemental mass for each DOF.
> * compute \(DC\), a vector containing only the diagonal terms in the consistent mass matrix \(m\_e\).
> * compute \(SC\), a vector of size=ndf, obtained summing the components in \(DC\) pertaining to the same DOF (i to ndf).
> * now we can obtain the scale factors for each dof \(i\) as: \(SM\_i/SC\_i\).
> * scale each diagonal term of the consistent mass matrix \(DC\_j\) using the scale factor of the respective DOF \(SM\_i/SC\_i\):
>
>   \(diag\left(m\_e\right)\_j = DC\_j \cdot SM\_i/SC\_i\).

The center of mass \(CoM\) and the total masses \(m\_t\) and \(m\_f\) of the structure, for each node \(n\) with position \(X\_n\) and each DOF \(i\), can now be easily computed from \(LM\):

\[\begin{split}m\_{t\_i} &= \sum\_{n=1}^{Nnodes} LM\_{ni}\\
m\_{f\_i} &= \sum\_{n=1}^{Nnodes} LM\_{ni}\quad(\text{if}\:i = free)\\
CoM\_i &= \frac{\sum\_{n=1}^{Nnodes} X\_{ni} \cdot LM\_{ni}}{m\_{f\_i}} \quad(\text{if}\:i = free)\end{split}\]

The generalized mass matrix is

\[gm = \Phi^T M \Phi\]

If the default solver is used in the [eigen command](eigen.html) (-genBandArpack), and the option **-unorm** is not used, the eigenvectors are mass-normalized and \(gm\) will be an identity matrix, i.e. a diagonal matrix whose diagonal entries are = 1, and whose size is \(n\_m \times n\_m\) (where \(n\_m\) is the number of requested eigenvalues).

The modal participation factor matrix \(MPF\) is a \(n\_m \times ndf\) matrix (where ndf = 3 in 2D and 6 in 3D), where each row contains the modal participation factors for each DOF. The modal participation factor for a certain mode \(i\) and DOF \(j\) indicates how strongly the motion (or rotation) associated to that DOF is represented in the eigenvector \(i\)

\[MPF\_{ij} = \frac{\Phi\_{i}^T M T\_j}{gm\_{ii}}\]

where \(T\_j\) defines the magnitude of the rigid body response to imposed rigid body motion (displacement or infinitesimal rotation) in the DOF \(j\). Each \(ndf \times 1\) block \(T\_{nj}\) corresponds to the node \(n\) and it is defined as (for the 3D/6DOFs case):

\[\begin{split}T\_{nj} =
\begin{pmatrix}
1 & 0 & 0 & 0 & d\_z & -d\_z \\
0 & 1 & 0 & -d\_z & 0 & d\_x \\
0 & 0 & 1 & d\_y & -d\_x & 0 \\
0 & 0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 0 & 1
\end{pmatrix}
\begin{Bmatrix}
e\_1 \\
e\_2 \\
e\_3 \\
e\_4 \\
e\_5 \\
e\_6 \\
\end{Bmatrix}\end{split}\]

where \(e\_j\) is 1, and all other \(e\_p\:(\text{with}\:p \neq j)\) are 0. \(d\_x\), \(d\_y\) and \(d\_z\) are the distances of the node \(n\) coordinates \(X\_n=\left(x, y, z\right)\) from the center of mass \(CoM=\left(x\_0, y\_0, z\_0\right)\). Therefore, the modal participation factors accounts for the masses directly input at translational and rotational DOFs, and also the rotational masses given by the translational masses gyrating about the center of mass. Note, in fact, that even if the user does not input any rotational mass, or even if the user uses 3D solid elements with no rotational DOF, the modal participation factors associated to the rotational DOFs may be \(\neq 0\).

The modal participation mass matrix \(MPM\) is a \(n\_m \times ndf\) matrix (where ndf = 3 in 2D and 6 in 3D), where each row contains the modal participation masses for each DOF. The modal participation mass for a certain mode \(i\) and DOF \(j\) is defined as

\[MPM\_{ij} = \frac{\left(\Phi\_{i}^T M T\_j\right)^2}{gm\_{ii}}\]

If the modal participation masses for each mode in a particular DOF are summed, it should give the total mass of the structure for that DOF, exlcluding the masses at fixed DOFs.

[[HintonEtAl1976](#id2)]

Hinton, E., Rock, T. & Zienkiewicz, O. (1976). “A note on mass lumping and related processes in the Finite element method.” Earthquake Engineering and Structural Dynamics, 13, 9, p. A112.

Example

The following example shows how to:

* Use the modalProperties command
* Print the results on the console (`'-print'`)
* Generate a report file in the current directory (`'-file', 'ModalReport.txt'`)
* Use a displacement-normalization for the eigenvectors

```python
modalProperties('-print', '-file', 'ModalReport.txt', '-unorm')
```

For a complete example that runs an **eigenvalue analysis**, extracts the **modal properties** and runs a **response spectrum analysis**, see the documentation of the [responseSpectrumAnalysis Command](responseSpectrumAnalysis.html)

ReportFile

The generated report file looks like this:

```python
# MODAL ANALYSIS REPORT

* 1. DOMAIN SIZE:
# This is the size of the problem: 2 for 2D problems, 3 for 3D problems.
3

* 2. EIGENVALUE ANALYSIS:
#          MODE        LAMBDA         OMEGA     FREQUENCY        PERIOD
# ------------- ------------- ------------- ------------- -------------
              1        7578.8       87.0563       13.8554     0.0721738
              2       8484.47       92.1112       14.6599     0.0682131
              3       10518.5        102.56       16.3229     0.0612636
              4         85779       292.881       46.6134     0.0214531
              5       89260.1       298.764       47.5498     0.0210306
              6        101089       317.945       50.6025     0.0197619
              7   1.71885e+06       1311.05        208.66    0.00479249

* 3. TOTAL MASS OF THE STRUCTURE:
# The total masses (translational and rotational) of the structure
# including the masses at fixed DOFs (if any).
#            MX            MY            MZ           RMX           RMY           RMZ
# ------------- ------------- ------------- ------------- ------------- -------------
           1600          1600          1600          7200         10000         10000

* 4. TOTAL FREE MASS OF THE STRUCTURE:
# The total masses (translational and rotational) of the structure
# including only the masses at free DOFs.
#            MX            MY            MZ           RMX           RMY           RMZ
# ------------- ------------- ------------- ------------- ------------- -------------
           1600          1600          1600          7200         10000         10000

* 5. CENTER OF MASS:
# The center of mass of the structure, calculated from free masses.
#             X             Y             Z
# ------------- ------------- -------------
              2           1.5           4.5

* 6. MODAL PARTICIPATION FACTORS:
# The participation factor for a certain mode 'a' in a certain direction 'i'
# indicates how strongly displacement along (or rotation about)
# the global axes is represented in the eigenvector of that mode.
#          MODE            MX            MY            MZ           RMX           RMY           RMZ
# ------------- ------------- ------------- ------------- ------------- ------------- -------------
              1       1.20368             0             0             0      0.661418             0
              2             0      -1.20172             0      0.637456             0             0
              3             0             0             0             0             0      -2.39705
              4      0.430981             0             0             0       -1.8352             0
              5             0      -0.41375             0      -1.83591             0             0
              6             0             0             0             0             0      0.780575
              7             0             0      -1.17082             0             0             0

* 7. MODAL PARTICIPATION MASSES:
# The modal participation masses for each mode.
#          MODE            MX            MY            MZ           RMX           RMY           RMZ
# ------------- ------------- ------------- ------------- ------------- ------------- -------------
              1       1418.18             0             0             0        428.21             0
              2             0       1430.41             0        402.49             0             0
              3             0             0             0             0             0       9041.23
              4        181.82             0             0             0       3296.78             0
              5             0        169.58             0       3338.87             0             0
              6             0             0             0             0             0       958.755
              7             0             0       1515.54             0             0             0

* 8. MODAL PARTICIPATION MASSES (cumulative):
# The cumulative modal participation masses for each mode.
#          MODE            MX            MY            MZ           RMX           RMY           RMZ
# ------------- ------------- ------------- ------------- ------------- ------------- -------------
              1       1418.18             0             0             0        428.21             0
              2       1418.18       1430.41             0        402.49        428.21             0
              3       1418.18       1430.41             0        402.49        428.21       9041.23
              4          1600       1430.41             0        402.49       3724.99       9041.23
              5          1600       1599.99             0       3741.36       3724.99       9041.23
              6          1600       1599.99             0       3741.36       3724.99       9999.99
              7          1600       1599.99       1515.54       3741.36       3724.99       9999.99

* 9. MODAL PARTICIPATION MASS RATIOS (%):
# The modal participation mass ratios (%) for each mode.
#          MODE            MX            MY            MZ           RMX           RMY           RMZ
# ------------- ------------- ------------- ------------- ------------- ------------- -------------
              1        88.636             0             0             0        4.2821             0
              2             0       89.4005             0       5.59014             0             0
              3             0             0             0             0             0       90.4123
              4       11.3638             0             0             0       32.9678             0
              5             0       10.5988             0       46.3732             0             0
              6             0             0             0             0             0       9.58755
              7             0             0       94.7214             0             0             0

* 10. MODAL PARTICIPATION MASS RATIOS (%) (cumulative):
# The cumulative modal participation mass ratios (%) for each mode.
#          MODE            MX            MY            MZ           RMX           RMY           RMZ
# ------------- ------------- ------------- ------------- ------------- ------------- -------------
              1        88.636             0             0             0        4.2821             0
              2        88.636       89.4005             0       5.59014        4.2821             0
              3        88.636       89.4005             0       5.59014        4.2821       90.4123
              4       99.9997       89.4005             0       5.59014       37.2499       90.4123
              5       99.9997       99.9993             0       51.9633       37.2499       90.4123
              6       99.9997       99.9993             0       51.9633       37.2499       99.9999
              7       99.9997       99.9993       94.7214       51.9633       37.2499       99.9999
```

Code Developed by: **Massimo Petracca** at ASDEA Software, Italy