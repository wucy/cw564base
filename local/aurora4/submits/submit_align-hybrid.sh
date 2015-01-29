#!/bin/tcsh

set ALLARGS=($*)
set cmdopts 
set CHANGED
if ( $#argv > 1 ) then
while ( $?CHANGED )
  unset CHANGED
  if (`echo "$argv[1]" | awk '{print(substr($1,1,1))}'` == "-" ) then
      set CHANGED
      set cmdopts = "$cmdopts $argv[1]"
      shift argv
      set cmdopts = "$cmdopts $argv[1]"
      shift argv
  endif
end
endif

if (( $#argv != 3 ) && ( $#argv != 4 ))  then
   echo "Usage: $0 env trainset qnenv"
   echo "       $0 env train qnenv"
   exit 100
endif

set HTE = $1
setenv TRAINSET $2
set HTEQN = $3

if ($#argv == 4) then
    set WAITID = "-hold_jid $4"
else
    set WAITID
endif

if ( ! -f $HTE ) then
    echo "ERROR: env file $HTE not found"
    exit 100
endif
if ( ! -f $HTEQN ) then
    echo "ERROR: env file $HTEQN not found"
    exit 100
endif

# Grid settings
if ( -f lib/htesystem/HTE.system ) then
    source lib/htesystem/HTE.system
endif
if ( $?CODINESETTING ) then
  source $CODINESETTING 
endif
if ( $?QSUBQUEUE ) then
   set QUEUE = $QSUBQUEUE
else
   set QUEUE = low
endif

if ( $?QSUBPROJECT ) then
   set QPROJ = $QSUBPROJECT
else
   set QPROJ = babel
endif

set QOPT
if ( $?UBUNTU ) then
   set QOPT = ($QOPT -l ubuntu=1)
endif
if ( $?QMAXJOBS ) then
   set QOPT = ($QOPT -tc $QMAXJOBS)
endif
set QOPT = ( $QOPT -l generation=80 )

set RUN_ARRAY_JOB=base/tools/run-array-job.sh

# Generate LOG information directory
if ( ! -d LOGs/${TRAINSET} ) mkdir -p LOGs/${TRAINSET}

# Generate CMD run directory
if ( ! -d CMDs ) mkdir -p CMDs

# Cache the command lines (useful to keep track of things)
echo "# Running align-hybrid default script" >> CMDs/${TRAINSET}.cmds
echo "$0 $ALLARGS" >> CMDs/${TRAINSET}.cmds
echo "------------------------------------" >> CMDs/${TRAINSET}.cmds

set HTEST=base/local/dtools/halign-hybrid
set SETLIST=lib/flists_align/${TRAINSET}.lst
set NJOBS=`wc -l $SETLIST | gawk '{print $1}'`

set LOGFILE=LOGs/${TRAINSET}/align_${TRAINSET}_\$TASK_ID.LOG

set qsubopts = "$QOPT -P $QPROJ -l qp=$QUEUE"

set substr=`qsub -cwd $qsubopts -o $LOGFILE -j y $WAITID -S /bin/bash -t 1-$NJOBS $RUN_ARRAY_JOB $SETLIST ${HTEST} $cmdopts ${HTE} $TRAINSET SET align $HTEQN`

set jnum=`echo $substr | awk '{print $3}' | cut -f 1 -d .`

echo $jnum
