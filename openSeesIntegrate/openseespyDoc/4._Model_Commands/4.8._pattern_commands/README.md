# 4.8. pattern commands

# 4.8. pattern commands

pattern(*patternType*, *patternTag*, *\*patternArgs*)

The pattern command is used to construct a LoadPattern and add it to the Domain. Each LoadPattern in OpenSees has a TimeSeries associated with it. In addition it may contain ElementLoads, NodalLoads and SinglePointConstraints. Some of these SinglePoint constraints may be associated with GroundMotions.

|  |  |
| --- | --- |
| `patternType` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | pattern type. |
| `patternTag` ([int](https://docs.python.org/3/library/functions.html#int)) | pattern tag. |
| `patternArgs` ([list](https://docs.python.org/3/library/stdtypes.html#list)) | a list of pattern arguments |

The following contain information about available `patternType`:

1. [Plain Pattern](plainPattern.html)
2. [UniformExcitation Pattern](uniformExcitation.html)
3. [Multi-Support Excitation Pattern](multiExcitation.html)