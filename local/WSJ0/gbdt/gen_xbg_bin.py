#! /usr/bin/env python


import os
import sys
import re

import numpy as np
import xgboost as xbg



IN_TXT = sys.argv[1]
OUT_BIN = sys.argv[2]



data = xbg.DMatrix(IN_TXT)

data.save_binary(OUT_BIN)


