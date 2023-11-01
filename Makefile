CASES = $(basename $(wildcard *.sh))
PATCHES = $(addprefix patches/,$(addsuffix .diff,$(notdir $(wildcard trees/*-*))))

all : zips details

repos : $(addprefix build/,$(CASES))

zips : $(addprefix build/,$(addsuffix .zip,$(CASES)))

details : $(addprefix build/,$(addsuffix .json,$(CASES)))

build/% : %.sh $(PATCHES)
	rm -rf $@
	mkdir -p $@
	cd $@ && bash ../../$<

build/%.zip : build/%
	cd $< && zip -r ../$(notdir $@) .

build/%.json : build/%
	export SOURCE_DATE_EPOCH=2147483647 \
		&& version="`versioningit $<`" \
		&& next_version="`versioningit --next-version $<`" \
		&& jq --arg version "$$version" --arg next_version "$$next_version" --indent 4 -n '{version: $$version, next_version: $$next_version}' > $@

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

clean :
	rm -rf build patches
