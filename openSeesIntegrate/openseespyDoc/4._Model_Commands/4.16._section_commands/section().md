# section()

# 4.16. section commands

section(*secType*, *secTag*, *\*secArgs*)
:   This command is used to construct a SectionForceDeformation object, hereto referred to as Section, which represents force-deformation (or resultant stress-strain) relationships at beam-column and plate sample points.

    |  |  |
    | --- | --- |
    | `secType` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | section type |
    | `secTag` ([int](https://docs.python.org/3/library/functions.html#int)) | section tag. |
    | `secArgs` ([list](https://docs.python.org/3/library/stdtypes.html#list)) | a list of section arguments, must be preceded with `*`. |

For example,

```python
secType = 'Elastic'
secTag = 1
secArgs = [E, A, Iz]
section(secType, secTag, *secArgs)
```

The following contain information about available `secType`:

1. [Elastic Section](elasticSection.html)
2. [Fiber Section](fibersection.html)
3. [NDFiber Section](ndfiber.html)
4. [Wide Flange Section](wfsection2d.html)
5. [RC Section](rcsection2d.html)
6. [RCCircular Section](rccircularsection.html)
7. [Parallel Section](parallelsection.html)
8. [Section Aggregator](sectionaggregator.html)
9. [Uniaxial Section](uniaxialsection.html)
10. [Elastic Membrane Plate Section](elasticMembranePlateSection.html)
11. [Plate Fiber Section](plateFiberSection.html)
12. [Bidirectional Section](bidirectionalSection.html)
13. [Isolator2spring Section](isolatorsection.html)
14. [LayeredShell](LayeredShell.html)
15. [Pipe Section](pipeSection.html)