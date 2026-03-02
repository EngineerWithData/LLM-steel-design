# OpenSeesPy Documentation

This is a cleaned and organized version of the OpenSeesPy documentation.

## Contents

1. [1. Installation](./1._Installation/README.md)
   1.1. 1.1. PyPi (Windows, Linux, Mac)
2. [2. Compilation](./2._Compilation/README.md)
   2.1. 2.1. Compilation for Windows
   2.2. 2.2. Compilation for MacOS
   2.3. 2.3. Compilation using QT
3. [3. Change Log](./3._Change_Log/README.md)
4. [4. Model Commands](./4._Model_Commands/README.md)
   4.1. 4.1. model command
   4.2. 4.2. element commands
   4.3. 4.3. node command
   4.4. 4.4. sp constraint commands
   4.5. 4.5. mp constraint commands
   4.6. 4.6. pressureConstraint command
   4.7. 4.7. timeSeries commands
   4.8. 4.8. pattern commands
   4.9. 4.9. mass command
   4.10. 4.10. region command
   4.11. 4.11. rayleigh command
   4.12. 4.12. block commands
   4.13. 4.13. beamIntegration commands
   4.14. 4.14. uniaxialMaterial commands
   4.15. 4.15. nDMaterial commands
   4.16. 4.16. section commands
   4.17. 4.17. frictionModel commands
   4.18. 4.18. geomTransf commands
5. [5. Analysis Commands](./5._Analysis_Commands/README.md)
   5.1. 5.1. constraints commands
   5.2. 5.2. numberer commands
   5.3. 5.3. system commands
   5.4. 5.4. test commands
   5.5. 5.5. algorithm commands
   5.6. 5.6. integrator commands
   5.7. 5.7. analysis command
   5.8. 5.8. eigen command
   5.9. 5.9. analyze command
   5.10. 5.10. modalProperties Command
   5.11. 5.11. responseSpectrumAnalysis Command
6. [6. Output Commands](./6._Output_Commands/README.md)
   6.1. 6.1. basicDeformation command
   6.2. 6.2. basicForce command
   6.3. 6.3. basicStiffness command
   6.4. 6.4. eleDynamicalForce command
   6.5. 6.5. eleForce command
   6.6. 6.6. eleNodes command
   6.7. 6.7. eleResponse command
   6.8. 6.8. getEleTags command
   6.9. 6.9. getLoadFactor command
   6.10. 6.10. getNodeTags command
   6.11. 6.11. getTime command
   6.12. 6.12. nodeAccel command
   6.13. 6.13. nodeBounds command
   6.14. 6.14. nodeCoord command
   6.15. 6.15. nodeDisp command
   6.16. 6.16. nodeEigenvector command
   6.17. 6.17. nodeDOFs command
   6.18. 6.18. nodeMass command
   6.19. 6.19. nodePressure command
   6.20. 6.20. nodeReaction command
   6.21. 6.21. nodeResponse command
   6.22. 6.22. nodeVel command
   6.23. 6.23. nodeUnbalance command
   6.24. 6.24. numFact command
   6.25. 6.25. numIter command
   6.26. 6.26. printA command
   6.27. 6.27. printB command
   6.28. 6.28. printGID command
   6.29. 6.29. printModel command
   6.30. 6.30. record command
   6.31. 6.31. recorder command
   6.32. 6.32. sectionForce command
   6.33. 6.33. sectionDeformation command
   6.34. 6.34. sectionStiffness command
   6.35. 6.35. sectionFlexibility command
   6.36. 6.36. sectionLocation command
   6.37. 6.37. sectionWeight command
   6.38. 6.38. systemSize command
   6.39. 6.39. testIter command
   6.40. 6.40. testNorm command
   6.41. 6.41. version command
   6.42. 6.42. logFile command
7. [7. Utility Commands](./7._Utility_Commands/README.md)
   7.1. 7.1. convertBinaryToText command
   7.2. 7.2. convertTextToBinary command
   7.3. 7.3. database command
   7.4. 7.4. InitialStateAnalysis command
   7.5. 7.5. loadConst command
   7.6. 7.6. modalDamping command
   7.7. 7.7. reactions command
   7.8. 7.8. remove command
   7.9. 7.9. reset command
   7.10. 7.10. restore command
   7.11. 7.11. save command
   7.12. 7.12. sdfResponse command
   7.13. 7.13. setTime command
   7.14. 7.14. setNodeCoord command
   7.15. 7.15. setNodeDisp command
   7.16. 7.16. setNodeVel command
   7.17. 7.17. setNodeAccel command
   7.18. 7.18. setPrecision command
   7.19. 7.19. setElementRayleighDampingFactors command
   7.20. 7.20. setNodeTemperature command
   7.21. 7.21. start command
   7.22. 7.22. stop command
   7.23. 7.23. stripXML command
   7.24. 7.24. updateElementDomain command
   7.25. 7.25. updateMaterialStage
   7.26. 7.26. wipe command
   7.27. 7.27. wipeAnalysis command
   7.28. 7.28. setNumthread command
   7.29. 7.29. getNumthread command
8. [8. FSI Commands](./8._FSI_Commands/README.md)
   8.1. 8.1. mesh command
   8.2. 8.2. remesh command
   8.3. 8.3. PFEM integrator
   8.4. 8.4. PFEM SOE
   8.5. 8.5. PFEM test
   8.6. 8.6. PFEM analysis
9. [9. Sensitivity Commands](./9._Sensitivity_Commands/README.md)
   9.1. 9.1. parameter command
   9.2. 9.2. addToParameter command
   9.3. 9.3. updateParameter command
   9.4. 9.4. setParameter command
   9.5. 9.5. getParamTags command
   9.6. 9.6. getParamValue command
   9.7. 9.7. computeGradients command
   9.8. 9.8. sensitivityAlgorithm command
   9.9. 9.9. sensNodeDisp command
   9.10. 9.10. sensNodeVel command
   9.11. 9.11. sensNodeAccel command
   9.12. 9.12. sensLambda command
   9.13. 9.13. sensSectionForce command
   9.14. 9.14. sensNodePressure command
10. [10. Reliability Commands](./10._Reliability_Commands/README.md)
   10.1. 10.1. randomVariable command
11. [11. Parallel Commands](./11._Parallel_Commands/README.md)
   11.1. 11.1. getPID command
   11.2. 11.2. getNP command
   11.3. 11.3. barrier command
   11.4. 11.4. send command
   11.5. 11.5. recv command
   11.6. 11.6. Bcast command
   11.7. 11.7. setStartNodeTag command
   11.8. 11.8. domainChange command
   11.9. 11.9. partition command
12. [12. Preprocessing Commands](./12._Preprocessing_Commands/README.md)
   12.1. 12.1. DiscretizeMember command
13. [13. Postprocessing Modules](./13._Postprocessing_Modules/README.md)
14. [14. Examples](./14._Examples/README.md)
   14.1. 14.1. Structural Examples
   14.2. 14.2. Earthquake Examples
   14.3. 14.3. Tsunami Examples
   14.4. 14.4. GeoTechnical Examples
   14.5. 14.5. Thermal Examples
   14.6. 14.6. Parallel Examples
   14.7. 14.7. Plotting Examples
   14.8. 14.8. Sensitivity Examples
