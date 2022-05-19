stty -echo # Do not show what we type in terminal so it does not meddle with our nice output
dmesg -n 1 # Do not report *useless* system messages to the terminal
python3 /opt/workbench/workbench_core.py
stty echo
