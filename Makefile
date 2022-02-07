CASES = $(basename $(wildcard *.sh))
PATCHES = $(addprefix patches/,$(addsuffix .diff,$(notdir $(wildcard trees/*-*))))

all : $(addprefix build/,$(CASES))

build/% : %.sh $(PATCHES)
	rm -rf $@
	mkdir -p $@
	( cd $@ ; bash ../../$< )

patches/0100-code.diff : trees/0000 trees/0100-code
	mkdir -p patches
	-diff -Naur $^ > $@

patches/0200-packaged.diff : trees/0100-code trees/0200-packaged
	mkdir -p patches
	-diff -Naur $^ > $@

patches/0300-feature.diff : trees/0200-packaged trees/0300-feature
	mkdir -p patches
	-diff -Naur $^ > $@

patches/0300-default-tag.diff : trees/0200-packaged trees/0300-default-tag
	mkdir -p patches
	-diff -Naur $^ > $@

patches/0300-dirt.diff : trees/0200-packaged trees/0300-dirt
	mkdir -p patches
	-diff -Naur $^ > $@

patches/0300-pattern.diff : trees/0200-packaged trees/0300-pattern
	mkdir -p patches
	-diff -Naur $^ > $@
