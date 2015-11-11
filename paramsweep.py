#!/usr/bin/env python
"""
Run multiple simulations varying a single parameter.
"""

import foampy
from foampy.dictionaries import replace_value
import numpy as np
from subprocess import call
import os
import pandas as pd
import shutil
from pyrm2tf import processing as pr


def zero_tsr_fluc():
    """Set TSR fluctuation amplitude to zero."""
    replace_value("system/fvOptions", "tsrAmplitude", 0.0)


def set_tsr(val):
    """Set mean tip speed ratio."""
    print("Setting TSR to", val)
    replace_value("system/fvOptions", "tipSpeedRatio", val)


def log_perf(param="tsr", append=True):
    """Log performance to file."""
    if not os.path.isdir("processed"):
        os.mkdir("processed")
    fpath = "processed/{}_sweep.csv".format(param)
    if append and os.path.isfile(fpath):
        df = pd.read_csv(fpath)
    else:
        df = pd.DataFrame(columns=["tsr", "cp", "cd"])
    df = df.append(pr.calc_perf(t1=3.0), ignore_index=True)
    df.to_csv(fpath, index=False)


def tsr_sweep(start=0.4, stop=3.4, step=0.5, append=False):
    """Run over multiple TSRs. `stop` will be included."""
    if not append and os.path.isfile("processed/tsr_sweep.csv"):
        os.remove("processed/tsr_sweep.csv")
    tsrs = np.arange(start, stop + 0.5*step, step)
    cp = []
    cd = []
    for tsr in tsrs:
        set_tsr(tsr)
        if tsr == tsrs[0]:
            call("./Allclean")
            print("Running blockMesh")
            call("blockMesh > log.blockMesh", shell=True)
            print("Running snappyHexMesh")
            call("snappyHexMesh -overwrite > log.snappyHexMesh",
                 shell=True)
            print("Running topoSet")
            call("topoSet > log.topoSet", shell=True)
            shutil.copytree("0.org", "0")
            print("Running pimpleFoam")
            call("pimpleFoam > log.pimpleFoam", shell=True)
        else:
            print("Running pimpleFoam")
            call("pimpleFoam > log.pimpleFoam", shell=True)
        os.rename("log.pimpleFoam", "log.pimpleFoam." + str(tsr))
        log_perf(append=True)
    # Set tip speed ratio back to default
    set_tsr(3.1)


if __name__ == "__main__":
    tsr_sweep(0.5, 5.0, 0.5, append=False)
