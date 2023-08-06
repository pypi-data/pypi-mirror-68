## Introduction

A typical data analysis will consist of many stages requiring computation and presentation of results. Consider the following two stage data analysis using Rmarkdown (quality control followed by data modelling):

```
|-- input/raw_data.csv
|-- code
│   |-- QC.Rmd
│   |-- model.Rmd
|-- output/QC/QC_data.csv
|-- report/out_md
|   |-- _site.yml
|   |-- QC.md
|   |-- model.md
|-- report/out_html
|   |-- QC.html
|   |-- model.html
```

The steps required for this analysis could be exhaustively defined as:

>raw_data.csv is input to QC.Rmd which produces QC.md and QC_data.csv.
QC_data.csv is input to model.Rmd which produces model.md. _site.yml is used to render QC.md and model.md into QC.html and model.html pages.

Using a workflow execution tool one can efficiently execute the commands needed 
to accomplish this workflow. However, it would be easier on the analyst to 
reduce the workflow to the following definition:

>QC.Rmd must run before model.Rmd

This simplified workflow can be expanded into the concrete computational tasks 
needed to build the final website. Tasks such as defining the 
rendering commands and the website layout get in the way of the data analysis.

### **scikick**

scikick is a command-line-tool for connecting data analysis 
pages with simple commands inspired by git. The workflow will execute to build a 
website of results from a set of R/Rmarkdown files. Users can specify ordering 
of the execution such that some pages will be run before others.

**Features**

- Commands inspired by git for configuring the workflow: `sk init`, `sk add`, `sk status`, `sk del`, `sk mv`.
- Automated website design (from directory structure of `.Rmd` files)
- Collects page metadata (session info, page runtime, git history)
- Automated conversion of `.R` to `.Rmd` with `knitr::spin` (coming soon)

This framework can simplify the collection of outputs from various scripts
allowing all figures generated during execution to be captured and presented 
to readers.

[Example Output](https://petronislab.camh.ca/pub/scikick_tests/master/)

## Getting Started

The following should be installed prior to installing scikick.

|**Requirements**   |**Recommended**|
|---|---|
|python3 (>=3.6)   | [git >= 2.0](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) |
|R + packages `install.packages(c("rmarkdown", "knitr", "yaml","git2r"))`   | [singularity >= 2.4](http://singularity.lbl.gov/install-linux)  |
|[pandoc > 2.0](https://pandoc.org/installing.html)   | [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/)   |

### Installation

```
# For now
python3 setup.py install

# Once put on public repositories
pip install scikick
conda install scikick
```

## Example Project

##### sk init

Initialize scikick with `sk init`. This can be done in an existing or an empty project. 

```
mkdir scikick_example
cd scikick_example
sk init
```

This creates `scikick.yml`. This file is used by scikick to store the workflow
definition and it is modified using scikick commands.

##### sk add

Next, create an Rmd file and add it to the workflow.
This is achieved with `sk add`.

```
# Create a hello world Rmarkdown file
printf "%s\n%s\n%s\n" '```{r, include = TRUE}' 'cat("Hello, World!")' '```' > hw.Rmd

sk add hw.Rmd
```

##### sk status

Now scikick is configured to process hw.Rmd. Use `sk status` to view the state of scikick.

```
sk status
# Number of Rmd => md => html tasks: 1
# 	hw.Rmd
```

This shows that hw.Rmd requires execution to generate its output.

##### sk run

Now, run all scikick jobs with

```
sk run
```

After execution is finished, the directory structure should look like

```
.
├── hw.Rmd
├── report
│   ├── donefile
│   ├── out_html
│   │   ├── hw.html
│   │   └── index.html
│   └── out_md # has many files we can ignore for now
└── scikick.yml
```

The `report/` directory contains all of scikick's output.

Opening `report/out_html/index.html` in a web browser should show the website 
homepage with one menu item for hw.html (hw.Rmd's output).

### Tracking out-of-date files

Running `sk status` again will result in no jobs to be run.

```
sk status
```

And `sk run` will do nothing.

```
sk run
<...>
Nothing to be done.
<...>
```

scikick tracks files using their timestamp (using snakemake) to determine if the report is up-to-date.
For example, if we make changes to hw.Rmd and run scikick

```
touch hw.Rmd
sk run
```

then scikick re-executes to create `report/out_html/hw.html` from scratch.

### Using dependencies

If the project has dependencies between different files, we can make scikick aware of these.

Let's say we have an R script `hello.R` which is sourced by `greets.Rmd`.

```
# create the files
# code/hello.R
echo 'greeting_string = "Hello World"' > code/hello.R
# code/greets.Rmd
printf "%s\n%s\n%s\n" '```{r, include = TRUE}' 'source("code/hello.R")
print(greeting_string)' '```' > code/greets.Rmd

# add the Rmd to the workflow
sk add code/greets.Rmd 
```

Be aware that while `code/greets.Rmd` and `code/hello.R` are in the same 
directory, all code is executed from the project root. This means that 
`source("hello.R")` will error and we instead need `source("code/hello.R")`. 

Let's run `sk run` to create `report/out_html/greets.html`.

Then let's make changes to `code/hello.R` and `sk run` again.

```
touch code/hello.R
sk run
```

Nothing happens since scikick does not know that changes in `code/hello.R` also affect `code/greets.Rmd`.
In order to make scikick track changes in `hello.R`, we have to add it as a dependency to `greets.Rmd`.

##### sk depadd

```
sk depadd code/greets.Rmd code/hello.R
```

Now whenever we change `hello.R` and run `sk run`, the file that depends on it (`greets.Rmd`) will be rerun as if it was changed.

Use `sk depdel` to remove dependencies.

These commands should be enough for most projects. Read on for additional usage.

## Other Useful Commands

##### sk status -v

Use this command to view the full scikick configuration where dependencies for
each file are indented below it. `+` and `*`
mark out-of-date files that will be run on the next `sk run`.

##### sk mv

While rearranging files in the project, use `sk mv` so scikick can adjust the workflow definition accordingly.

```
mkdir code
sk mv hw.Rmd code/hw.Rmd
```

If you are using git, use `sk mv -g` to use `git mv`.

##### sk del

We can remove `hw.Rmd` from our analysis with

```
sk del hw.Rmd
```

Note that this does not delete the hw.Rmd file.

### Adding structure

In order to make our project more tidy, we can create some dedicated directories with

```
sk init --dirs
# creates:
# report/ - output directory for scikick
# output/ - directory for outputs from scripts
# code/ - directory containing scripts (Rmd and others)
# input/ - input data directory
```

If git is in use for the project, directories `report`, `output`, `input` should not be tracked.
They can be added to `.gitignore` with

```
sk init --git
```

and git will be know to ignore these directories.

## sk layout

The order of tabs in the website can be configured using `sk layout`.
Running the command without arguments

```
sk layout
```

returns the current ordered list of tab indices and their names:

```
0:  a
1:  b
2:  c
3:  d
4:  e
```

The order can be changed by specifying the new order of tab indices, e.g.

```
# to reverse the tab order:
sk layout 4 3 2 1
# the list does not have to include all of the indices (0 to 4 in this case):
sk layout 4 # move tab 4 to the front
# the incomplete list '4' is interpreted as '4 0 1 2 3'
```

Output after running `sk layout 4`:

```
0:  e
1:  a
2:  b
3:  c
4:  d
```

Also, individual tabs can be moved with

```
# move tab with index 1 to tab with index 3
sk layout 1 to 3
# swap tabs with indices 1 and 3
sk layout 1 sw 3
```

## Rstudio with scikick

Rstudio, by default, executes code relative to opened Rmd file's location. This
can be changed by going to `Tools > Global Options > Rmarkdown > Evaluate chunks in directory`
and setting to "Current".

## Other scikick files in `report/`
- `donefile` - dummy file created during the snakemake workflow that is executed by scikick
- `out_md/`
  - `out_md/*.md` - markdown files that were `knit` from our initial Rmarkdown files
  - `out_md/_site.yml` - YAML file specifying the structure of the to-be-created website
  - `out_md/knitmeta/` - directory of RDS files containing information about javascript libraries that need to be included when rendering markdown files to HTMLs.
  - `out_html/` - contains the resulting HTML files

## External vs Internal Dependencies

**Internal dependencies** - code or files the Rmd uses directly during execution  
**External dependencies** - code that must be executed prior to the page

scikick assumes that any depedency that is not added as a page is an internal dependency. 

Currently, only `Rmd` files are supported as pages. In the future, executables and other file types may be
supported by scikick to allow easy usage of arbitrary scripts between `Rmd` pages.

## Snakemake Backend

Data pipelines have benefitted from improved workflow execution tools 
(Snakemake, Bpipe, Nextflow), however, final data analysis is often left out of 
this workflow definition. Using scikick, projects can quickly configure reports
to take advantage of the snakemake backend with:

- Basic depedency management (i.e. GNU Make)  
- Distribution of tasks on compute clusters (thanks to snakemake's `--cluster` argument)    
- Software virtualization (Singularity, Docker, Conda)  
- Other snakemake functionality

### Singularity

In order to run our Rmd in a singularity image, we have to do two things: specify the singularity image and notify snakemake that singularity, as a feature, should be used.

```
# specify a singularity image
sk snake --singularity docker://rocker/tidyverse
# notify snakemake that singularity is to be used
sk snake --args-set --use-singularity
# run the project within a singularity container
sk run
```

It can be noticed that only the code that is included inside the Rmarkdown files is run in the singularity container.
This eliminates the necessity for scikick to be included in the container itself.

### Conda

The same steps are necessary to use conda, except the needed file is a conda environment YAML file.

```
# create an env.yml file
conda env export -n base > env.yml
# specify that this file is the conda environment file
sk snake --conda env.yml
# enable conda usage in snakemake
sk snake --args-set --use-conda
# run
sk run
```

### Conda and singularity

It must be noted that usage of conda and singularity simultaneously requires that the singularity image has conda internally.

## Incorporating with other Pipelines

Additional workflows written in [snakemake](http://snakemake.readthedocs.io/en/stable/) should play nicely with the scikick workflow.

These jobs can be added to the begining, middle, or end of scikick related tasks:

- Beginning 
  - `sk depadd first_step.rmd pipeline_donefile` (where pipeline_donefile is the last file generated by the Snakefile)
- Middle
  - Add `report/out_md/first_step.md` as the input to the first job of the Snakefile.
  - `sk depadd second_step.rmd pipeline_donefile`
- End 
  - Add `report/out_md/last_step.md` as the input to the first job of the Snakefile.
