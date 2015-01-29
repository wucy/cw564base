#! /usr/bin/env python


import os
import sys
import re

import numpy as np




IN_FEALAB = sys.argv[1]
OUT_NPY = sys.argv[2]

data = np.loadtxt(IN_FEALAB, delimiter=' ')
np.save(OUT_NPY, data)



