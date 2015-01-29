#! /usr/bin/env python

import os
import sys
import random


num_states = int(sys.argv[1])
num_class = int(sys.argv[2])

output_fn = sys.argv[3]


output = open(output_fn, 'w')

output.write("%d %d\n" % (num_states, num_class))

for i in range(num_states):
    output.write("%d %d\n" % (i, random.randint(0, num_class - 1)))

output.close()

