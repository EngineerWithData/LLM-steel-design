# 4.14. uniaxialMaterial commands

# 4.14. uniaxialMaterial commands

uniaxialMaterial(*matType*, *matTag*, *\*matArgs*)
:   This command is used to construct a UniaxialMaterial object which represents uniaxial stress-strain (or force-deformation) relationships.

    |  |  |
    | --- | --- |
    | `matType` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | material type |
    | `matTag` ([int](https://docs.python.org/3/library/functions.html#int)) | material tag. |
    | `matArgs` ([list](https://docs.python.org/3/library/stdtypes.html#list)) | a list of material arguments, must be preceded with `*`. |

For example,

```python
matType = 'Steel01'
matTag = 1
matArgs = [Fy, E0, b]
uniaxialMaterial(matType, matTag, *matArgs)
```

The following contain information about available `matType`:

## 4.14.1. Steel & Reinforcing-Steel Materials

1. [Steel01](steel01.html)
2. [Steel02](steel02.html)
3. [Steel4](steel4.html)
4. [ReinforcingSteel](ReinforcingSteel.html)
5. [Dodd\_Restrepo](Dodd_Restrepo.html)
6. [RambergOsgoodSteel](RambergOsgoodSteel.html)
7. [SteelMPF](SteelMPF.html)
8. [Steel01Thermal](steel01thermal.html)

## 4.14.2. Concrete Materials

1. [Concrete01](Concrete01.html)
2. [Concrete02](Concrete02.html)
3. [Concrete04](Concrete04.html)
4. [Concrete06](Concrete06.html)
5. [Concrete07](Concrete07.html)
6. [Concrete01WithSITC](Concrete01WithSITC.html)
7. [ConfinedConcrete01](ConfinedConcrete01.html)
8. [ConcreteD](ConcreteD.html)
9. [FRPConfinedConcrete](FRPConfinedConcrete.html)
10. [FRPConfinedConcrete02](FRPConfinedConcrete02.html)
11. [ConcreteCM](ConcreteCM.html)
12. [TDConcrete](TDConcrete.html)
13. [TDConcreteEXP](TDConcreteEXP.html)
14. [TDConcreteMC10](TDConcreteMC10.html)
15. [TDConcreteMC10NL](TDConcreteMC10NL.html)

## 4.14.3. Standard Uniaxial Materials

1. [Elastic Uniaxial Material](ElasticUni.html)
2. [Elastic-Perfectly Plastic Material](ElasticPP.html)
3. [Elastic-Perfectly Plastic Gap Material](ElasticPPGap.html)
4. [Elastic-No Tension Material](ENT.html)
5. [Hysteretic](Hysteretic.html)
6. [Parallel Material](ParallelUni.html)
7. [Series Material](SeriesUni.html)

## 4.14.4. PyTzQz uniaxial materials for p-y, t-z and q-z elements for modeling soil-structure interaction through the piles in a structural foundation

1. [PySimple1 Material](PySimple1.html)
2. [TzSimple1 Material](TzSimple1.html)
3. [QzSimple1 Material](QzSimple1.html)
4. [PyLiq1 Material](PyLiq1.html)
5. [TzLiq1 Material](TzLiq1.html)
6. [QzLiq1 Material](QzLiq1.html)

## 4.14.5. Other Uniaxial Materials

1. [Hardening Material](Hardening.html)
2. [CastFuse Material](Cast.html)
3. [ViscousDamper Material](ViscousDamper.html)
4. [BilinearOilDamper Material](BilinearOilDamper.html)
5. [Modified Ibarra-Medina-Krawinkler Deterioration Model with Bilinear Hysteretic Response (Bilin Material)](Bilin.html)
6. [Modified Ibarra-Medina-Krawinkler Deterioration Model with Peak-Oriented Hysteretic Response (ModIMKPeakOriented Material)](ModIMKPeakOriented.html)
7. [Modified Ibarra-Medina-Krawinkler Deterioration Model with Pinched Hysteretic Response (ModIMKPinching Material)](ModIMKPinching.html)
8. [SAWS Material](SAWS.html)
9. [BarSlip Material](BarSlip.html)
10. [Bond SP01 - - Strain Penetration Model for Fully Anchored Steel Reinforcing Bars](Bond_SP01.html)
11. [Fatigue Material](Fatigue.html)
12. [Impact Material](ImpactMaterial.html)
13. [Hyperbolic Gap Material](HyperbolicGapMaterial.html)
14. [Limit State Material](LimitState.html)
15. [MinMax Material](MinMax.html)
16. [ElasticBilin Material](ElasticBilin.html)
17. [ElasticMultiLinear Material](ElasticMultiLinear.html)
18. [MultiLinear](MultiLinear.html)
19. [Initial Strain Material](InitStrainMaterial.html)
20. [Initial Stress Material](InitStressMaterial.html)
21. [PathIndependent Material](PathIndependent.html)
22. [Pinching4 Material](Pinching4.html)
23. [Engineered Cementitious Composites Material](ECC01.html)
24. [SelfCentering Material](SelfCentering.html)
25. [Viscous Material](Viscous.html)
26. [BoucWen Material](BoucWen.html)
27. [BWBN Material](BWBN.html)
28. [KikuchiAikenHDR Material](KikuchiAikenHDR.html)
29. [KikuchiAikenLRB Material](KikuchiAikenLRB.html)
30. [AxialSp Material](AxialSp.html)
31. [AxialSpHD Material](AxialSpHD.html)
32. [Pinching Limit State Material](PinchingLimitStateMaterial.html)
33. [CFSWSWP Wood-Sheathed Cold-Formed Steel Shear Wall Panel](CFSWSWP.html)
34. [CFSSSWP Steel-Sheathed Cold-formed Steel Shear Wall Panel](CFSSSWP.html)
35. [Backbone Material](Backbone.html)
36. [Masonry](Masonry.html)
37. [Pipe Material](pipeMaterial.html)