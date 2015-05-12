#!/bin/sh

# Modify data geometry
# Recently used is data of stream Prompt_v4, which contains runs 165071-172619, corresponding to IOVs E,F,G,H,I,P1,P2


base_dir="$CMSSW_BASE/src/ApeEstimator/ApeEstimator/test/Misalignments"
cfg_file="misalignInputGeometry_cfg.py"


cmsRun $base_dir/$cfg_file spread=5 iov=E
cmsRun $base_dir/$cfg_file spread=5 iov=F
cmsRun $base_dir/$cfg_file spread=5 iov=G
cmsRun $base_dir/$cfg_file spread=5 iov=H
cmsRun $base_dir/$cfg_file spread=5 iov=I
cmsRun $base_dir/$cfg_file spread=5 iov=P1
cmsRun $base_dir/$cfg_file spread=5 iov=P2



cmsRun $base_dir/$cfg_file spread=10 iov=E
cmsRun $base_dir/$cfg_file spread=10 iov=F
cmsRun $base_dir/$cfg_file spread=10 iov=G
cmsRun $base_dir/$cfg_file spread=10 iov=H
cmsRun $base_dir/$cfg_file spread=10 iov=I
cmsRun $base_dir/$cfg_file spread=10 iov=P1
cmsRun $base_dir/$cfg_file spread=10 iov=P2



cmsRun $base_dir/$cfg_file spread=15 iov=E
cmsRun $base_dir/$cfg_file spread=15 iov=F
cmsRun $base_dir/$cfg_file spread=15 iov=G
cmsRun $base_dir/$cfg_file spread=15 iov=H
cmsRun $base_dir/$cfg_file spread=15 iov=I
cmsRun $base_dir/$cfg_file spread=15 iov=P1
cmsRun $base_dir/$cfg_file spread=15 iov=P2



cmsRun $base_dir/$cfg_file spread=20 iov=E
cmsRun $base_dir/$cfg_file spread=20 iov=F
cmsRun $base_dir/$cfg_file spread=20 iov=G
cmsRun $base_dir/$cfg_file spread=20 iov=H
cmsRun $base_dir/$cfg_file spread=20 iov=I
cmsRun $base_dir/$cfg_file spread=20 iov=P1
cmsRun $base_dir/$cfg_file spread=20 iov=P2



rm alignment.log
rm my_treeFile*.root

mkdir $base_dir/output/

#mv my_treeFile*.root $base_dir/output/.
mv pixelTobMisaligned*.db $base_dir/output/.
