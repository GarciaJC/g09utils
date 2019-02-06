#!/usr/bin/env python

import g09pbs as pbs
import sys
from subprocess import call

for arg in sys.argv[1:]:
    basename = str(arg)
    if basename.endswith('.com'):
        basename = basename[:-4]

    submit = pbs.pbs(basename,'12:00:00')
    pbsfile = basename + ".pbs"
    submit.write_file(pbsfile)
    call(["qsub", pbsfile ])

