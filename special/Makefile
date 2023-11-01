BUILDDIR = build
OUTDIR = $(BUILDDIR)/target

all : $(OUTDIR)/no-git.zip

$(OUTDIR)/no-git.zip : no-git
	mkdir -p $(dir $@)
	cd $< && zip -r $(abspath $@) .
