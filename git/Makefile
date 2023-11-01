BUILDDIR = build
OUTDIR = $(BUILDDIR)/target
REPODIR = $(BUILDDIR)/repos
PATCHDIR = $(BUILDDIR)/patches

CASES = $(basename $(wildcard *.sh))
PATCHES = $(addprefix $(PATCHDIR)/,$(addsuffix .diff,$(notdir $(wildcard trees/*-*))))

ARCHIVE_CASES = default-tag distance exact
ARCHIVES = $(addprefix $(OUTDIR)/archives/git-archive-,$(addsuffix .zip,$(ARCHIVE_CASES)))
ARCHIVE_DETAILS = $(addprefix $(OUTDIR)/archives/git-archive-,$(addsuffix .json,$(ARCHIVE_CASES)))

# Git archives need special prep
#all : zips details archives
all : zips details

zips : $(addprefix $(OUTDIR)/repos/,$(addsuffix .zip,$(CASES)))

details : $(addprefix $(OUTDIR)/repos/,$(addsuffix .json,$(CASES)))

archives : $(ARCHIVES) $(ARCHIVE_DETAILS)

.SECONDARY : $(addprefix $(REPODIR)/,$(CASES))

$(REPODIR)/% : %.sh $(PATCHES)
	rm -rf $@
	mkdir -p $@
	cd $@ && PATCHDIR=$(abspath $(PATCHDIR)) bash $(abspath $<)

$(OUTDIR)/repos/%.zip : $(REPODIR)/%
	mkdir -p $(dir $@)
	cd $< && zip -r $(abspath $@) .

$(OUTDIR)/repos/%.json : $(REPODIR)/% %.json
	mkdir -p $(dir $@)
	awk -v hash="$$(cd $<; git show -s --format=%h)" '{ sub("{hash}", hash); print }' $*.json > $@

$(ARCHIVES) : $(OUTDIR)/archives/git-archive-%.zip : $(REPODIR)/% $(OUTDIR)/repos/%.json
	mkdir -p $(dir $@)
	cd $< && git archive --format=zip -o $(abspath $@) HEAD
	cp -f $(OUTDIR)/repos/$*.json $(OUTDIR)/archives/git-archive-$*.json

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
