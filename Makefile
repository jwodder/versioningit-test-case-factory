BUILDDIR = build
OUTDIR = $(BUILDDIR)/target
REPODIR = $(BUILDDIR)/repos
PATCHDIR = $(BUILDDIR)/patches

CASES = $(basename $(wildcard *.sh))
PATCHES = $(addprefix $(PATCHDIR)/,$(addsuffix .diff,$(notdir $(wildcard trees/*-*))))

ARCHIVE_CASES = default-tag distance exact
ARCHIVES = $(addprefix $(OUTDIR)/archives/hg-archive-,$(addsuffix .zip,$(ARCHIVE_CASES)))
ARCHIVE_DETAILS = $(addprefix $(OUTDIR)/archives/hg-archive-,$(addsuffix .json,$(ARCHIVE_CASES)))

all : zips details archives

zips : $(addprefix $(OUTDIR)/hg/,$(addsuffix .zip,$(CASES)))

details : $(addprefix $(OUTDIR)/hg/,$(addsuffix .json,$(CASES)))

archives : $(ARCHIVES) $(ARCHIVE_DETAILS)

.SECONDARY : $(addprefix $(REPODIR)/hg/,$(CASES))

$(REPODIR)/hg/% : %.sh $(PATCHES)
	rm -rf $@
	mkdir -p $@
	cd $@ && PATCHDIR=$(abspath $(PATCHDIR)) bash $(abspath $<)

$(OUTDIR)/hg/%.zip : $(REPODIR)/hg/%
	mkdir -p $(dir $@)
	cd $< && zip -r $(abspath $@) .

$(OUTDIR)/hg/%.json : $(REPODIR)/hg/% %.json
	mkdir -p $(dir $@)
	awk -v hash="$$(cd $<; hg id -i)" '{ sub("{hash}", hash); print }' $*.json > $@

$(ARCHIVES) : $(OUTDIR)/archives/hg-archive-%.zip : $(REPODIR)/hg/% $(OUTDIR)/hg/%.json
	mkdir -p $(dir $@)
	mkdir -p $(BUILDDIR)/scratch
	cd $< && hg archive $(abspath $(BUILDDIR)/scratch/hg-archive-$*)
	cd $(BUILDDIR)/scratch/hg-archive-$* && zip -r $(abspath $@) .
	cp -f $(OUTDIR)/hg/$*.json $(OUTDIR)/archives/hg-archive-$*.json

$(PATCHDIR)/0100-code.diff : trees/0000 trees/0100-code
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0200-packaged.diff : trees/0100-code trees/0200-packaged
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-feature.diff : trees/0200-packaged trees/0300-feature
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-default-tag.diff : trees/0200-packaged trees/0300-default-tag
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-dirt.diff : trees/0200-packaged trees/0300-dirt
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-pattern.diff : trees/0200-packaged trees/0300-pattern
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

clean :
	rm -rf $(BUILDDIR)
