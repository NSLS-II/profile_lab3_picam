# Make ophyd listen to pyepics.
import nslsii
import ophyd.signal

import matplotlib.pyplot as plt

ophyd.signal.EpicsSignal.set_defaults(connection_timeout=5)

# At the end of every run, verify that files were saved and
# print a confirmation message.
from bluesky.callbacks.broker import verify_files_saved, post_run
# RE.subscribe(post_run(verify_files_saved, db), 'stop')
from bluesky import RunEngine
from bluesky.plans import count

# Uncomment the following lines to turn on verbose messages for
# debugging.
# import logging
# ophyd.logger.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)

RE = RunEngine({})


import subprocess


def show_env():
    # this is not guaranteed to work as you can start IPython without hacking
    # the path via activate
    proc = subprocess.Popen(["conda", "list"], stdout=subprocess.PIPE)
    out, err = proc.communicate()
    a = out.decode('utf-8')
    b = a.split('\n')
    print(b[0].split('/')[-1][:-1])

def warmup_hdf5_plugins(detectors):
    """
    Warm-up the hdf5 plugins.
    This is necessary for when the corresponding IOC restarts we have to trigger one image
    for the hdf5 plugin to work correctly, else we get file writing errors.
    Parameter:
    ----------
    detectors: list
    """
    for det in detectors:
        _array_size = det.hdf5.array_size.get()
        if 0 in [_array_size.height, _array_size.width] and hasattr(det, "hdf5"):
            print(f"\n  Warming up HDF5 plugin for {det.name} as the array_size={_array_size}...")
            det.hdf5.warmup()
            print(f"  Warming up HDF5 plugin for {det.name} is done. array_size={det.hdf5.array_size.get()}\n")
        else:
            print(f"\n  Warming up of the HDF5 plugin is not needed for {det.name} as the array_size={_array_size}.")
