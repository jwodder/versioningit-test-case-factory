all :
	make -C git all
	make -C hg all
	make -C special all
	rm -rf target
	mkdir -p target/repos
	mkdir -p target/repos/archives
	mkdir -p target/repos/errors
	mkdir -p target/repos/git
	mkdir -p target/repos/hg
	cp git/build/target/*.tar.gz target
	cp -R git/build/target/archives/ target/repos/archives
	cp -R git/build/target/repos/ target/repos/git
	cp -R hg/build/target/archives/ target/repos/archives
	cp -R hg/build/target/repos/ target/repos/hg
	cp -R special/build/target/ target/repos
	cd target/repos && mv no-tag.* template-fields-error.* errors

clean :
	make -C git clean
	make -C hg clean
	make -C special clean
	rm -rf target
