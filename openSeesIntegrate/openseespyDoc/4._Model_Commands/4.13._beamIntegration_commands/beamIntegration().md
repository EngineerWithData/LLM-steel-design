# beamIntegration()

# 4.13. beamIntegration commands

beamIntegration(*type*, *tag*, *\*args*)
:   A wide range of numerical integration options are available in OpenSees to represent distributed plasticity or non-prismatic section details in Beam-Column Elements, i.e., across the entire element domain [0, L].

Following are beamIntegration types available in the OpenSees:

Integration Methods for Distributed Plasticity.
Distributed plasticity methods permit yielding at any integration point along the element
length.

1. [Lobatto](Lobatto.html)
2. [Legendre](Legendre.html)
3. [NewtonCotes](NewtonCotes.html)
4. [Radau](Radau.html)
5. [Trapezoidal](Trapezoidal.html)
6. [CompositeSimpson](CompositeSimpson.html)
7. [UserDefined](userDefined.html)
8. [FixedLocation](FixedLocation.html)
9. [LowOrder](LowOrder.html)
10. [MidDistance](MidDistance.html)

Plastic Hinge Integration Methods. Plastic hinge integration methods confine material yielding to regions of the element of specified length while the remainder of the element is linear elastic. A summary of plastic hinge integration methods is found in ([Scott and Fenves 2006](https://doi.org/10.1061/(ASCE)0733-9445(2006)132:2(244))).

1. [UserHinge](UserHinge.html)
2. [HingeMidpoint](HingeMidpoint.html)
3. [HingeRadau](HingeRadau.html)
4. [HingeRadauTwo](HingeRadauTwo.html)
5. [HingeEndpoint](HingeEndpoint.html)
6. [HingeEndpoint](HingeEndpoint.html)
7. [ConcentratedPlasticity](ConcentratedPlasticity.html)
8. [ConcentratedCurvature](ConcentratedCurvature.html)