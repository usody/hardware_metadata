build:
	./build/build_workbench.sh

cleanBuild:
	# TODO hardcoded
	rm -rf staging/live/filesystem.squashfs

test:
	python3 test.py