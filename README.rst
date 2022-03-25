Workbench Lite
#########################
A minimalist, open source tool to capture hardware data about computers generating a report on JSON file.

By default Workbench Lite generates a report of the hardware
characteristics of the computer using lshw, dmidecode, hwinfo and smartmontools packages.

You must run this software as root / sudo.

Installation
************
Workbench lite should work in any Linux as long as it has the packages below.

1. Clone this repository and go to the repository main folder.

2. Make sure we have debian required packages installed. Install the `debian packages <requirements.debian.txt>`_, like
   the following way:

.. code-block::

    cat requirements.debian.txt | sudo xargs apt install -y.

2. Make sure we have python required packages installed. Install the `python packages <requirements.txt>`_, like
   the following way:

.. code-block::

    pip3 install -r requirements.txt


Usage
*****
Execute Workbench Lite like sudo:

.. code-block::

    sudo python3 <path>/workbench_lite.py

At the end of the execution, it generates a json file with the collected information,
called '*{date}_{wbid}_WBv{version}_snapshot.json*'.

Testing
*******
1. Clone this repository and go to the repository main folder.
2. Execute on project folder:

.. code-block::

    sudo make test

Code Ownership
*****************

All the code in this repository currently is owned by  **Associació Pangea – Coordinadora Comunicació per a la Cooperació**.
