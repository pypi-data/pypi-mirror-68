#
# ISCNSNAKE : ISCN Structural and Numerical Analysis of Karyotype Entries
#

ISCNSNAKE is a tool to use with ISCN : the International System for
Cytogenic Nomenclature written in python 3.7. The repository contains
three python files, one is the core of the module (ISCNParser.py) and the
second (run_SNAKE.py) is a quick script that executes the main function of
ISCNParser. Most features are accessible through the console menu that
opens when the script is ran but if you want to automate multiple files
or do something more complicated it is suggested that you import the
module into your own script. The third script (quick_run_SNAKE.py)
runs ISCNParser at the default settings with users only having to specify
the location of the Mitelman database on their computer, the desired output
folder and filenames, and any criteria they wish to use as filters. For a 
description on how to use these filters consult readthedocs.org/ISCNSNAKE/


#
# SYSTEM REQUIREMENTS
#

Python 3.6 or greater (anaconda strongly recommended)

Python modules
- pandas 
- numpy
- easy_install (for installation)

#
# INSTALLATION
#

1. Open either terminal or command line in the fold you place the download (this folder).
2. Input the following:

easy_install --always-unzip .

3. You should be able to run the program from anywhere with the upcoming instructions.

#
# HOW TO USE
#

quick_SNAKE 

runs ISCNSNAKE.parse_file at the default settings, so if want to change the handling of clones, filenames, or analyze aberration cooccurance you will have to interact with the menu provided by run_SNAKE.py. For the vast majority of use
cases this version is more than adequate.

After installation, quick_SNAKE can be ran from any location using the following prompt entered in terminal or command prompt:

python -m ISCNSNAKE.quick_SNAKE [-options]

This can also be done by entering interactive mode (just type python) and then:

import ISCNSNAKE.quick_SNAKE

With no options specified, the program will ask for some user input. These can also be specified by command line options.

[-f] : Mitelman filters for selection rows and columns of the Mitelman database. 

Filter syntax is “column:attribute”. For example, if you wanted to select only cases with topography indicated as breast, you would enter “Topography:Breast” as a filter. If you want to add additional filters, such as wanting to specify only adenocarcinomas with the same topography, create a second filter with the same syntax and separate it with two forward slashes.

Example: “Topography:Breast//Morphology:Adenocarcinoma”. 

Double slashes are used as commas, spaces, and dashes are all within the attributes in the Mitelman Database. Filters place restrictions on which categories are acceptable
so it is possible to analyze multiple types by adding more filters. 

Example: “Topography:Breast//Topography:Lung//Morphology:Adenocarcinoma”
This would analyze all Breast and Lung adenocarcinomas

[-p] : File prefix, determines names of output files. ex. -p Skeletal makes output files Skeletal_DeepDel.txt, Skeletal_DeepAmp.txt
[-o] : Name of output folder, if it doesn’t exist it will make one. Defaults to current directory.
[-v] : Verbosity. If specified, will output each ISCN it comes across. Useful if you’re unsure whether or not your filters were correct on filter usage but does slow the program down a bit.
[-i] : Path to the plain text file of the Mitelman database

Step by Step Tutorial:

In this example I will be using the Mitelman.txt file included in the download, looking to analyze
Retinoblastomas.
1. After installation, navigate to the folder where your desired data file is.
2. Enter the command:
python -m ISCNSNAKE.quick_SNAKE -i -p RB -o retinoblastoma -v 

You will then be prompted to add filters. Since we want to analyze retinoblastomas we should enter
"Topography:Eye//Morphology:Retinoblastoma"

You will then see the output to the terminal (because you specified verbose) and the files created from the
analysis in the folder "retinoblastoma"




The full version of the program with many experimental settings can be ran with the following prompt:

python -m ISCNSNAKE.run_SNAKE

This can also be done in interactive mode.

This will open a menu that will allow you to configure many options. Here is a brief description of what each of the of the more complex options do. Many of the options simply specify filenames and should be fairly self-explanitory. 

1 -- input filename 
Required. Enter the path to the file containing the karyotype data. 
ex: ../../Mitelman.txt

2 -- input data type (ISCN/Mitelman)
Can be set to either ISCN or Mitelman. Default ISCN. Mitelman is the format that the text version of the database
is in, as provided in Mitelman.txt. ISCN is a format where each karyotype in ISCN format is on a seperate line by itself,
as in ISCN_example.txt

3 -- clone handling

Set this to one the 3 following options:
first_only: only analyzes the first clone in each ISCN, good for small data sets with few clonal karyotypes
and one or two massive karyotypes with 10+ clones
seperate: analyzes each clone as a seperate patient, your frequency percentages will be very low, I 
personally don't recommend this option.
merge: creates a consensus karyotype out of all the clonal karyotypes

4 -- Output to file

If this is False, you will get no output. Can be good if you just want the raw data. To use this you will have
to change how you call run_SNAKE or assign _ to a variable afterwards.

6 -- output mode
relative if you want percentages, minmax if you want it to be a result between 0 and 1 (for machine learning
and possibly other purposes)\

7 -- current filters

Enter filters as described for quick_SNAKE but instead of seperating with double slashes just enter each
one seperately.

You may also incorporate elements of the ISCNParser algorithm into your script by importing ISCNSNAKE.ISCNParser
and then calling the functions and classes for your needs. 

15 -- analyze dependancies
Will make a list of co occurances of various aberrations. Very very very very slow. Creates a list
of links in circos format.

16 -- dependence quantile
Trims links to the quantile selected. Useful as most dependancy matrixes end up with hundreds of thousands
of co-occurances.

18 -- analyze errors
Set to True if you want a seperate file containing every instance of an unparsable karyotype. Could be used
pretty easily to check your own karyotypes to check for proper ISCN syntax. Will try to explain errors
but isn't very descriptive.

20 – legacy ploidy correction
This mode allows correction for ploidy to revert to the pre 2.3 operation of the ISCNSNAKE. When True the program will convert all deletions that are homozygous to -2 and all heterozygous deletions to -1. If your concern is more related to questions regarding homozygosity vs heterozygosity, enable this, but recognize your raw ISCN file will not contain absolute loss values. Example: ISCN 88,XX,-2,-2,-2,-2. In this ISCN we have a karyotype that is tetraploid and has lost all four copies of chromosome 2. If this feature is disabled (default behaviour) the rawISCN file will show a value of -4 for the chromosome 2 region, but if this were enabled it would only show -2 (indicating a homozygous deletion. On the other side, with the karyotype 67,XX,-2,-2,-2, where only 3 copies are lost, the default behaviour will return the absolute value (-3) and the legacy ploidy correction behavious will only indicate -1. This mode essentially changes the definition of deep loss, once enabled, deep losses are synonymous with homozygous deletions, but when turned off (default) the definition is changed so that all deletions of 2 or more copies is marked as a deep deletion. There is some ambiguity in the level of ploidy in any given sample so this ends up being somewhat of an estimate of homozygous deletions, and is sometimes prone to false positives and negatives,

21 – verbose
Set to True if you want all the karyotypes the program reads to be printed to console. (same as -v in quick_SNAKE)


## Authors

* Conception and design: **F.S. Vizeacoumar, A. Freywald, B.A. Weaver, F.J. Vizeacoumar**

* Development of methodology: **C. Denomy, S. Germain, F.S. Vizeacoumar, F.J. Vizeacoumar**

* Acquisition of data (provided animals, acquired and managed patients, provided facilities, etc.): **C. Denomy, S. Germain, F.S. Vizeacoumar**

* Analysis and interpretation of data (e.g., statistical analysis, biostatistics, computational analysis): **C. Denomy, S. Germain, F.S. Vizeacoumar, A. Freywald, F.J. Vizeacoumar**

* Writing, review, and/or revision of the manuscript: **C. Denomy, B. Haave, F.S. Vizeacoumar, A. Freywald, B.A. Weaver, F.J. Vizeacoumar**

* Administrative, technical, or material support (i.e., reporting or organizing data, constructing databases): **C. Denomy**

* Study supervision: **B.A. Weaver, F.J. Vizeacoumar**

* **C. Denomy** (connordenomy@gmail.com) - *Lead author*
Feel free to email me any questions you have about using this program.

#
# Acknowledgments
#

We thank members of the Vizeacoumar and Freywald laboratories for their insight and comments during the development of this project. This work is supported by NSERC Discovery grant (RGPIN-2014-04110) to F.J. Vizeacoumar.