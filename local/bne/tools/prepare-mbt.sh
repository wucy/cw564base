#! /bin/bash


TSET=traincv

mkdir -p lib/flists.mbt
cp lib/flists.hcopy/${TSET}.scp lib/flists.mbt/

cd lib/flists.mbt
../../base/tools/cutlists_mask.pl '%%%%%%%%%%%%-*' ${TSET}.scp ${TSET}_
cd ../..

cat lib/flists.hcopy/${TSET}.scp | awk -F'-' '{print "traincv_" $1 "-" $2;}' | uniq > lib/flists.mbt/${TSET}.lst


python base/tools/SortBySide.py lib/flists.mbt/${TSET}.scp lib/flists.mbt/${TSET}.lst '%%%%%%%%%%%%*' ${TSET} lib/flists.mbt/${TSET}.sort.scp lib/flists.mbt/${TSET}.range


