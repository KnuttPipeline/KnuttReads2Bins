#!/usr/bin/env python3

##
## dataConcat.py - Combine data files while adding id columns
##
## Knutt.org/KnuttReads2Bins

# Some steps generate one file per sample, this scripts combines
# these while adding wildcard values as columns

newcolumnnames = snakemake.params["colnames"]
sep = "\t"
inputfiles = snakemake.input.files
outputfile = snakemake.output.out


def readheader(file):
    with open(file) as lines:
        return next(lines)

header = {readheader(file) for file in inputfiles}

if(len(header)!=1 and "header" not in snakemake.params.keys()):
    print(f"Different headers: {header}!")
    exit(1)

header = snakemake.params.get("header",header.pop())

if(len(inputfiles)!=len(snakemake.params["vals"])):
    print("Wrong number of values!")
    exit(1)

inputfiles = list(zip(inputfiles, snakemake.params["vals"]))

with open(outputfile,"w") as out:
    out.write(sep.join(newcolumnnames))
    out.write(sep)
    out.write(header)
    for infile, newelements in inputfiles:
        if(not isinstance(newelements,str)):
            newelements = sep.join(newelements)
        with open(infile) as lines:
            next(lines)
            for line in lines:
                out.write(newelements)
                out.write(sep)
                out.write(line)
