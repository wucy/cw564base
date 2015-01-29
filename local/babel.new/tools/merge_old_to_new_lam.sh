#! /bin/bash

cat traincv.lam.esti | awk '{print $1;}' > new
cat traincv.lam.init | awk '{print $1;}' > old

sort new new old | uniq -u > left


./base/local/py/merge_left_to_new_lam.py left traincv.lam.init traincv.lam.esti

