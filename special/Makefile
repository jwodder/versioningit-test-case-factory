BUILDDIR = build
OUTDIR = $(BUILDDIR)/target

all : $(OUTDIR)/no-git.zip $(OUTDIR)/no-pyproject.zip

$(OUTDIR)/no-git.zip : trees/no-git
	mkdir -p $(dir $@)
	cd $< && zip -r $(abspath $@) .

$(OUTDIR)/no-pyproject.zip : cases/no-pyproject.sh trees/no-pyproject
	mkdir -p $(dir $@)
	rm -rf $(BUILDDIR)/scratch/no-pyproject
	mkdir -p $(BUILDDIR)/scratch/no-pyproject
	cd $(BUILDDIR)/scratch/no-pyproject && TREEDIR=$(abspath trees) bash $(abspath $<)
	cd $(BUILDDIR)/scratch/no-pyproject && zip -r $(abspath $@) .

clean :
	rm -rf $(BUILDDIR)
