#! /bin/tcsh



set cmdopts
set ALLARGS=($*)
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

if ( $#argv != 1 && $#argv != 2  ) then
    echo "Usage: $0 env [jwait]"
    exit 1
endif

set MLPENV = $argv[1]


if ( $#argv == 2 ) then
    set WAITID = "-hold_jid $2"
else
    set WAITID
endif

# Grid settings
if ( -f lib/htesystem/HTE.system ) then
    source lib/htesystem/HTE.system
endif
source $MLPENV

if ( $?CODINESETTING ) then
  source $CODINESETTING 
endif
if ( $?ACCELERATE ) then
    if ( $ACCELERATE == "cuda" ) then
        set QUEUE = cuda-low
    else
        set QUEUE = low
    endif
else if ( $?QSUBQUEUE ) then
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
    if ( $?ACCELERATE ) then
        if ( $ACCELERATE != "cuda" ) then
            set QOPT = ($QOPT -l ubuntu=1)
        endif
    else
        set QOPT = ($QOPT -l ubuntu=1)
    endif
else if ( $?ACCELERATE ) then
    if ( $ACCELERATE != "cuda" ) then
        set QOPT = ($QOPT -l ubuntu=1)
    endif
endif
if ( $?QSUBMAXRUNTIME ) then
    set QOPT = ( $QOPT -l h_rt=$QSUBMAXRUNTIME )
endif
if ( $?QSUBMEMFREE ) then
    set QOPT = ($QOPT -l mem_free=$QSUBMEMFREE)
endif
if ( $?QSUBMEMGRAB ) then
    set QOPT = ($QOPT -l mem_grab=$QSUBMEMGRAB)
endif

if ( ! -d LOGs/lamtune ) mkdir -p LOGs/lamtune

if ( ! -d CMDs ) mkdir -p CMDs


echo "# MBT lamtune" >> CMDs/mbt_lamtune.cmds
echo "$0 $ALLARGS" >> CMDs/mbt_lamtune.cmds
echo "------------------------------------" >> CMDs/mbt_lamtune.cmds

set LOGFILE = LOGs/lamtune/MBT_lamtune.log
if ( -f $LOGFILE ) \rm $LOGFILE

set TOOL = base/local/ntools/QN_mbt_gen_lamdata.sh


set FLISTDIR=lib/flists.hcopy

set TRNFN = `wc -l $FLISTDIR/train.scp | awk '{print $1}'`
set CVFN = `wc -l $FLISTDIR/cv.scp | awk '{print $1}'`

set TRNSTA = 0
@ TRNEND = $TRNFN - 1
@ CVSTA = $TRNEND + 1
@ CVEND = $TRNFN + $CVFN - 1

set NUM_HIDDEN_LAYERS = `echo $MLPSIZE | awk -F',' '{print NF-2}'`
set ACCELERATE = 'cuda'
set QNLAMDATAGEN = "base/local/bin/qn.mbt.lamdatagen.gpu.${NUM_HIDDEN_LAYERS}h" 




set cmdopts = "$cmdopts -TRNSTA $TRNSTA -TRNEND $TRNEND -CVSTA $CVSTA -CVEND $CVEND -ACCELERATE $ACCELERATE -QNMULTRN $QNMULTRN -INITWGTS fwdMLP/MLP"


mkdir -p work

set retstr=`qsub -cwd $QOPT -P $QPROJ -l qp=$QUEUE -o $LOGFILE -j y $WAITID -S /bin/tcsh \
    $TOOL $cmdopts $MLPENV work`

set jnum=`echo $retstr | awk '{print $3}' | cut -f 1 -d .`
echo $jnum
