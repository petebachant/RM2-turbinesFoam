#!/usr/bin/env python
"""Generate sampleDict for multiple cross-stream profiles."""

from __future__ import division, print_function
import numpy as np
import os
import sys
import foampy

# Input parameters
setformat = "raw"
interpscheme = "cellPoint"
fields = ["UMean", "UPrime2Mean", "kMean"]
x = 1.0
ymax = 1.5
ymin = -1.5
ny = 51
z_H_max = 1.25
z_H_min = -1.25
nz = 19
H = 0.807
zmax = z_H_max*H
zmin = z_H_min*H

header = r"""/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  2.4.x                                 |
|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      sampleDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
"""


def main():
    z_array = np.linspace(zmin, zmax, nz)

    txt = header + "\n"
    txt += "setFormat " + setformat + "; \n\n"
    txt += "interpolationScheme " + interpscheme + "; \n\n"
    txt += "sets \n ( \n"

    for z in z_array:
        # Fix interpolation issues if directly on a face
        if z == 0.0:
            z += 1e-5
        txt += "    " + "profile_" + str(z) + "\n"
        txt += "    { \n"
        txt += "        type        uniform; \n"
        txt += "        axis        y; \n"
        txt += "        start       (" + str(x) + " " + str(ymin) + " " + str(z) + ");\n"
        txt += "        end         (" + str(x) + " " + str(ymax) + " " + str(z) + ");\n"
        txt += "        nPoints     " + str(ny) + ";\n    }\n\n"

    txt += ");\n\n"
    txt += "fields \n(\n"

    for field in fields:
        txt += "    " + field + "\n"

    txt += "); \n\n"
    txt += "// *********************************************************************** // \n"

    with open("system/sampleDict", "w") as f:
        f.write(txt)

if __name__ == "__main__":
    main()
