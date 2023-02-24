install_HWMD_dependencies:
	# Add bullseye backports to install lshw=02.19* utility
	echo "deb http://deb.debian.org/debian bullseye-backports main contrib" | sudo tee /etc/apt/sources.list.d/backports.list
	sudo apt update
	# Install HWMD debian requirements
	cat requirements.debian.txt | sudo xargs apt install -y
	# Install HWMD python requirements
	sudo pip3 install -r requirements.txt

run:
	DISABLE_HWINFO=1 python3 main.py

test:
	DISABLE_HWINFO=1 python3 -m unittest tests/test.py -v

#remove snapshots folder
snapshots_clean:
	rm -rf snapshots/

#remove logs folder
logs_clean:
	rm -rf logs/