eReuse.org Workbench Lite
#########################

Create a hardware report of your computer saving the resulting report as 'computer.json'.

By default Workbench lite generates a report of the hardware
characteristics of the computer, so it is safe to use, using dmidecode package.

You must run this software as root / sudo.

Installation
************
Workbench lite should work in any Linux as long as it has the dmidecode package.

1. Clone this repository and go to the repository main folder.

2. Make sure we have the dmidecode package installed. On Debian systems execute:

.. code-block::

    sudo dmidecode --version

Usage
*****
Execute Workbench lite through the CLI or directly in Python.

Execute like sudo:

.. code-block::

    sudo python3 <path>/workbench_lite.py

At the end of the execution, it generates a json file with the collected information,
called 'snapshot.json'.

Testing
*******
1. Clone this repository and go to the repository main folder.
2. Work in progress..

Known limitations
*****************

