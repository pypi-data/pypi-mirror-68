# loading snakefile variables
suppressWarnings({
input = snakemake@input$rmd
output = snakemake@output$md
templatedir = snakemake@params$template_dir
dataparent = snakemake@params$data_parent
reportfile <- input
reportname <- gsub("\\.Rmd$", "", basename(input),ignore.case=TRUE)
outdatadir <- paste0(file.path(dataparent, reportname), "/")
source(file.path(templatedir, "outputLook.R"))
knitr::opts_chunk$set(optionsRender$knitr$opts_chunk)

rmd <- readLines(input)
if(reportname=="index") {
	index <- readLines(file.path(templatedir, "index.Rmd"))
	# when no index.Rmd exists - template is passed
	if(!identical(rmd, index)){
		# if that's the case - we don't include it
		rmd <- c(rmd, index)
	}
} else {
	footer <- readLines(file.path(templatedir, "footer.Rmd"))
	rmd <- c(rmd, footer)
}
knitr::opts_knit$set(root.dir = "./")
knitr::opts_knit$set(base.dir = dirname(output))
# to prevent interactive plots from being turned into PNGs
knitr::opts_chunk$set(screenshot.force = FALSE)
knitr::opts_chunk$set(fig.path = outdatadir)
knitr::opts_chunk$set(cache.path = paste0(outdatadir, "/cache/"))
# used for reporting calculation start time in the report
.scikick = new.env()
.scikick$starttime = Sys.time()
# output errors
tryCatch({
	knitr::knit(textConnection(rmd), output, quiet=TRUE)
}, error = function(e){
	write("sk: Error in Rmd execution", stderr())
	write(paste0("sk: \t", toString(e)), stderr())
	quit(status = 1)
})

knit_meta_obj = knitr::knit_meta(clean = FALSE)
saveRDS(knit_meta_obj,
	file = sub(output, pattern = ".md$", replacement = ".knitmeta.RDS"))
})
