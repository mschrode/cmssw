#!/bin/sh

# Merge geometries for different IOVs


# Set up environment
#cd <...>/CMSSW_4_2_<X>
#cmsenv

if [ ! $# == 1 ]; then
  echo "Usage: $0 misalignmentSpread"
  exit 1
fi

echo "misalignmentSpread: $1"

misalignmentSpread="$1"


dir_base="$PWD"
input_base="pixelTobMisaligned_${misalignmentSpread}"

cmscond_export_iov -l sqlite_file:log.db -d sqlite_file:${input_base}.db -t TrackerScenario -s sqlite_file:${dir_base}/${input_base}_E.db -b 1
cmscond_export_iov -l sqlite_file:log.db -d sqlite_file:${input_base}.db -t TrackerScenario -s sqlite_file:${dir_base}/${input_base}_F.db -b 165415
cmscond_export_iov -l sqlite_file:log.db -d sqlite_file:${input_base}.db -t TrackerScenario -s sqlite_file:${dir_base}/${input_base}_G.db -b 166000
cmscond_export_iov -l sqlite_file:log.db -d sqlite_file:${input_base}.db -t TrackerScenario -s sqlite_file:${dir_base}/${input_base}_H.db -b 166399
cmscond_export_iov -l sqlite_file:log.db -d sqlite_file:${input_base}.db -t TrackerScenario -s sqlite_file:${dir_base}/${input_base}_I.db -b 167044
cmscond_export_iov -l sqlite_file:log.db -d sqlite_file:${input_base}.db -t TrackerScenario -s sqlite_file:${dir_base}/${input_base}_P1.db -b 170249
cmscond_export_iov -l sqlite_file:log.db -d sqlite_file:${input_base}.db -t TrackerScenario -s sqlite_file:${dir_base}/${input_base}_P2.db -b 171876

# to check the result:
#cmscond_list_iov -t TrackerScenario -c sqlite_file:pixelTobMisaligned_10.db
