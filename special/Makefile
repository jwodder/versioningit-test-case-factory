BUILDDIR = build
OUTDIR = $(BUILDDIR)/target
REPODIR = $(BUILDDIR)/repos

ZIP_GIT_REPO = ../util/zip-git-repo.sh

CASES = $(basename $(notdir $(wildcard cases/*.sh)))
EXTRA = $(notdir $(wildcard cases/*.json) $(wildcard cases/*.marks))

all : cases extra $(OUTDIR)/no-git.zip $(OUTDIR)/shallow.zip

cases : $(addprefix $(OUTDIR)/,$(addsuffix .zip,$(CASES)))

extra : $(addprefix $(OUTDIR)/,$(EXTRA))

.SECONDARY : $(addprefix $(REPODIR)/,$(CASES))

$(REPODIR)/% : cases/%.sh
	rm -rf $@
	mkdir -p $@
	cd $@ && TREEDIR=$(abspath trees) bash $(abspath $<)

$(OUTDIR)/%.zip : $(REPODIR)/%
	mkdir -p $(dir $@)
	$(ZIP_GIT_REPO) $< $(abspath $@)

$(OUTDIR)/%.json : cases/%.json
	cp -f $< $@

$(OUTDIR)/%.marks : cases/%.marks
	cp -f $< $@

$(OUTDIR)/no-git.zip : trees/base
	mkdir -p $(dir $@)
	cd $< && zip -r $(abspath $@) .

$(OUTDIR)/shallow.zip :
	rm -rf $(REPODIR)/shallow
	mkdir -p $(REPODIR)
	git clone --depth 1 https://github.com/jwodder/versioningit-test $(REPODIR)/shallow
	mkdir -p $(dir $@)
	$(ZIP_GIT_REPO) $(REPODIR)/shallow $(abspath $@)

clean :
	rm -rf $(BUILDDIR)
