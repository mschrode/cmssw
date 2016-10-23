# Introduction to the Tracker-Alignment Software

## Install
```bash
scram p CMSSW CMSSW_8_0_21
cd CMSSW_8_0_21/src
cmsenv
git cms-addpkg Alignment/OfflineValidation
git cms-merge-topic mschrode:TkAl_Intro_8-0-21
scram b -j 4
```

## Offline validation (DMR)
We will run an example of the "offline validation" ("DMR plots") for the ideal detector (perfect alignment) and several mis-aligned detectors.
Visit the [https://twiki.cern.ch/twiki/bin/view/CMS/TkAlAllInOneValidation][documentation TWiki] for more information.


### Create the misalignment scenario
We will use the `CommonAlignmentProducer` to create a misaligned geometry.
Visit the [https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMisalignmentTools][documentation TWiki] for more information.

Go to `Alignment/Introduction/test` and run
```bash
cmsRun createRandomlyMisalignedDetector_cfg.py
rm *root
```
(The last command `rm *root` is not strictly necessary but removes some non-needed files.)
This will create the sqlite database file `geometry_PixelMisalignmentScenario1_from80X_mcRun2_design_v20.db`, which contains the alignment constants for a particular misalignment scenario.
Internally, the constants are stored in an instance (called tag) of type `TrackerAlignmentRcd` with the name `Alignments`.

The used misalignment scenario `PixelMisalignmentScenario1` is defined in `Alignment/Introduction/python/MisalignmentScenarios_cff.py`.
Browse the file to locate the scenario defintion.
What kind of misalignment is introduced?

You can create different misalignment scenarios by telling the `createRandomlyMisalignedDetector_cfg.py` script to load a different scenario, e.g. to use the `PixelMisalignmentScenario2` scenario, run
```bash
cmsRun createRandomlyMisalignedDetector_cfg.py scenario=PixelMisalignmentScenario2
rm *root
```
(The default value of the parameter scenario is `PixelMisalignmentScenario1`, which is why in the first step we did not have to specify any value.)
What output `.db` file created?

You can browse the output sqlite files (example here for `PixelMisalignmentScenario1`) using either sqlite:
```bash
sqlite3 geometry_PixelMisalignmentScenario1_from80X_mcRun2_design_v20.db
```
This will open the sqlite3 prompt.
To browse the content, type `.tables`.
We are interested in the table IOV, so do
```bash
select * from IOV;
```
which will display all payloads in IOV.
You notice our tag with name `Alignments`.
Exit sqlite with `.exit`.
Alternatively, you can use the CMSSW built-in `conddb` tool to browse the database content:
```bash
conddb --db geometry_PixelMisalignmentScenario1_from80X_mcRun2_design_v20.db listTags
```
which lists all tags, so also our `Alignments`.
To display more information of the tag, e.g. its payloads, type
```bash
conddb --db geometry_PixelMisalignmentScenario1_from80X_mcRun2_design_v20.db list Alignments
```


### Produce geometry-comparison and offline-validation plots
The offline validation as well as other TkAl validation plots are configured and run via the "all-in-one" tool (invoked with `validateAlignments.py`).
Visit the [https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMisalignmentTools][documentation TWiki] for more information.

Go to `Alignment/Introduction/test`.
The validation job is configured via an `.ini` file.
An example for our purpose is
```bash
example.ini
```
Browse it and familiarize yourself with the different config settings; they are documented [https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMisalignmentTools][here].
Where are the following parameters defined:
- the alignments to compare?
- the input data for the DMR plots? Where exactly are the files located?
- the statement which validations to run?

As you can see, there are two alignments defined: "ideal" and "misalign1", our previously produced misalignment scenario.
As you can see from the `[validation]` section, we will not only produce the DMR plots (`offline`) but also produce geometry comparison plots (`compare`) to inspect the misalignment scenario we have created.

Before running the validation, **first adjust all pathes*** in the `.ini` file to directories in your area.
Then, run the validation by
```bash
validateAlignments.py -c example.ini -N example --getImages
```
This will submit the validation jobs to the lxplus batch.
You can check the status of the jobs with
```bash
bjobs
```
Once all jobs are done (none listed when doing `bjobs`), go to the directory `example` that has been created by invoking the above validation and execut
```bash
TkAlMerge.sh
```
which will run the final steps to produce the validation plots.
Afterwards, the validation plots should be in the path specified in the field `datadir` in the `[general]` section of your `example.ini` file.

What do you see? Why?
