.PHONY: build
build:
	build/build_workbench.sh

# force build of bullseye
build_bullseye:
	VERSION_CODENAME='buster' build/build_workbench.sh

cleanBuild:
	# TODO hardcoded
	rm -rf staging/live/filesystem.squashfs

test:
	python3 test.py
