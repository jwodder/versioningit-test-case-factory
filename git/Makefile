BUILDDIR = build
OUTDIR = $(BUILDDIR)/target
REPODIR = $(BUILDDIR)/repos
PATCHDIR = $(BUILDDIR)/patches
ARCHIVEDIR = $(OUTDIR)/archives

CASES = $(basename $(notdir $(wildcard cases/*.sh)))
PATCHES = $(addprefix $(PATCHDIR)/,$(addsuffix .diff,$(notdir $(wildcard trees/*-*))))
MARKS = $(notdir $(wildcard cases/*.marks))

ARCHIVE_CASES = distance exact
ARCHIVES = $(addprefix $(ARCHIVEDIR)/git-archive-,$(addsuffix .zip,$(ARCHIVE_CASES)))
ARCHIVE_DETAILS = $(addprefix $(ARCHIVEDIR)/git-archive-,$(addsuffix .json,$(ARCHIVE_CASES)))

all : zips details marks archives sdist

zips : $(addprefix $(OUTDIR)/repos/,$(addsuffix .zip,$(CASES)))

details : $(addprefix $(OUTDIR)/repos/,$(addsuffix .json,$(CASES)))

marks : $(addprefix $(OUTDIR)/repos/,$(MARKS))

archives : $(ARCHIVES) $(ARCHIVE_DETAILS)

.SECONDARY : $(addprefix $(REPODIR)/,$(CASES))

sdist : $(REPODIR)/onbuild-write-fields
	cd $< && python3 -m build --sdist && mv dist/*.tar.gz $(abspath $(OUTDIR))

$(REPODIR)/% : cases/%.sh $(PATCHES)
	rm -rf $@
	mkdir -p $@
	cd $@ && PATCHDIR=$(abspath $(PATCHDIR)) bash $(abspath $<)

$(OUTDIR)/repos/%.zip : $(REPODIR)/%
	mkdir -p $(dir $@)
	cd $< && zip -r $(abspath $@) .

$(OUTDIR)/repos/%.json : $(REPODIR)/% cases/%.json util/format-json.py
	mkdir -p $(dir $@)
	python3 util/format-json.py -o $@ $< cases/$*.json

$(OUTDIR)/repos/%.marks : cases/%.marks
	cp -f $< $@

$(ARCHIVEDIR)/git-archive-distance.zip : $(REPODIR)/archive-repo
	mkdir -p $(dir $@)
	cd $< && git archive --format=zip -o $(abspath $@) HEAD

$(ARCHIVEDIR)/git-archive-distance.json : $(OUTDIR)/repos/archive-repo.json
	cp -f $< $@

$(ARCHIVEDIR)/git-archive-exact.zip : $(REPODIR)/archive-repo-mixed-tags
	mkdir -p $(dir $@)
	cd $< && git archive --format=zip -o $(abspath $@) HEAD

$(ARCHIVEDIR)/git-archive-exact.json : $(OUTDIR)/repos/archive-repo-mixed-tags.json
	cp -f $< $@

$(PATCHDIR)/0100-code.diff : trees/0000 trees/0100-code
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0200-packaged.diff : trees/0100-code trees/0200-packaged
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-archive.diff : trees/0200-packaged trees/0300-archive
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-archive-tags.diff : trees/0200-packaged trees/0300-archive-tags
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-archive-exclude.diff : trees/0200-packaged trees/0300-archive-exclude
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-archive-match.diff : trees/0200-packaged trees/0300-archive-match
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-custom-format.diff : trees/0200-packaged trees/0300-custom-format
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-custom-method-setup.diff : trees/0200-packaged trees/0300-custom-method-setup
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-custom-method-src.diff : trees/0200-packaged trees/0300-custom-method-src
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-default-tag.diff : trees/0200-packaged trees/0300-default-tag
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-default-version.diff : trees/0200-packaged trees/0300-default-version
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-default-version2.diff : trees/0200-packaged trees/0300-default-version2
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-dirt.diff : trees/0200-packaged trees/0300-dirt
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-exclude.diff : trees/0200-packaged trees/0300-exclude
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-feature.diff : trees/0200-packaged trees/0300-feature
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-match.diff : trees/0200-packaged trees/0300-match
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-write-encoding.diff : trees/0200-packaged trees/0300-write-encoding
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-write-py.diff : trees/0200-packaged trees/0300-write-py
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-write-template.diff : trees/0200-packaged trees/0300-write-template
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0300-write-txt.diff : trees/0200-packaged trees/0300-write-txt
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0400-custom-method-pkg.diff : trees/0300-custom-method-src trees/0400-custom-method-pkg
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0400-default-version-bad.diff : trees/0300-default-version trees/0400-default-version-bad
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0400-onbuild.diff : trees/0300-feature trees/0400-onbuild
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0400-onbuild-cfg.diff : trees/0300-feature trees/0400-onbuild-cfg
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0400-write-onbuild.diff : trees/0300-default-version2 trees/0400-write-onbuild
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0500-add-write-to-onbuild.diff : trees/0400-onbuild trees/0500-add-write-to-onbuild
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0500-onbuild-bases.diff : trees/0400-onbuild trees/0500-onbuild-bases
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0500-onbuild-nonidem.diff : trees/0400-onbuild trees/0500-onbuild-nonidem
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

$(PATCHDIR)/0600-all-fields.diff : trees/0500-add-write-to-onbuild trees/0600-all-fields
	mkdir -p $(PATCHDIR)
	-diff -Naur $^ > $@

clean :
	rm -rf $(BUILDDIR)
