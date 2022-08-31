# Make ophyd listen to pyepics.
import nslsii
import ophyd.signal

import matplotlib.pyplot as plt

ophyd.signal.EpicsSignal.set_defaults(connection_timeout=5)
                      magics=True, mpl=True, epics_context=False)


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