# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

----
## [Unreleased]

## [1.0.0-beta2] - 2023-05-05
_(dmidecode = 3.3 | smartmontools = 7.2 | hwinfo = 21.72 | lshw = 02.19 | lspci = 3.7.0)_
- [added] hwmd_version in snapshot 
- [changed] settings file
- [fixed] software_version var
- [removed] ERASURE_METHOD settings var

## [1.0.0-beta1] - 2023-04-21
_(dmidecode = 3.3 | smartmontools = 7.2 | hwinfo = 21.72 | lshw = 02.19 | lspci = 3.7.0)_
- [added] \_\_init\_\_.py file
- [added] snapshot tests field
- [changed] snapshot data field
- [changed] rename hw_retrieval.py file
- [changed] software and software_version in Core class
- [fixed] snapshot sid

## [1.0.0-beta]
- [added] core.py file
- [changed] main.py file
- [changed] print functions
- [removed] unnecessary imports


## [1.0.0-alpha]
- [changed] calver to semantic versioning
- [changed] python filenames
- [removed] build shell script
- [removed] Makefile build and boot commands

## [2022.12.2-beta]
_(dmidecode = 3.3 | smartmontools = 7.2 | hwinfo = 21.72 | lshw = 02.19 | lspci = 3.7.0)_
- [added] increasing resilience when uploading snapshots
- [changed] hwmd_settings folder name to settings (rel #4212)
- [fixed] checking the Internet connection

## [2022.12.1-beta] - 2022/12/22
_(dmidecode = 3.3 | smartmontools = 7.2 | hwinfo = 21.72 | lshw = 02.19 | lspci = 3.7.0)_
- [added] log file feature (rel #4116)
- [added] empty bash history on shell script (rel #4117)
- [changed] snapshots path name
- [fixed] logging error when sudo/root is required
- [fixed] loging warning when No Internet (rel #4168)
- [fixed] exception saving snapshot

## [2022.12.0-beta] - 2022/12/12
_(dmidecode = 3.3 | smartmontools = 7.2 | hwinfo = 21.72 | lshw = 02.19 | lspci = 3.7.0)_
- [added] snapshots_clean on Makefile
- [changed] rename all code to Hardware Metadata
- [changed] delete unnecessary files on .gitignore
- [changed] update README.md accordingly to HWMD
- [fixed] add pciutils on debian requirements file

## [2022.11.3-beta] - 2022/11/28
_(dmidecode = 3.3 | smartmontools = 7.2 | hwinfo = 21.72 | lshw = 02.19 | lspci = 3.7.0)_
- [added] highlight the information displayed on screen (rel #3939)
- [added] colorlog python module for display information
- [added] HWMDLog class
- [added] bash_history on build script
- [removed] print function for display information

## [2022.11.2-beta] - 2022/11/21
_(dmidecode = 3.3 | smartmontools = 7.2 | hwinfo = 21.72 | lshw = 02.19 | lspci = 3.7.0)_
- [fixed] hwinfo field in the snapshot when DISABLE_HWINFO is on 
- [added] default settings.ini template in the build script (rel #4068)
- [added] display DEVICE URL & SNAPSHOT on summary screen
- [added] settings_version new variable in the snapshot (rel #3999)
- [changed] create .profile file in the build scipt
- [changed] improve the messages displayed when interacting with DH API

## [2022.11.1-beta] - 2022/11/08
_(dmidecode = 3.3 | smartmontools = 7.2 | hwinfo = 21.72 | lshw = 02.19 | lspci = 3.7.0)_
- [added] display 'No Settings Version (NaN)' when version not defined
- [changed] save snapshots on current dir if not defined on settings file (rel #4053)

## [2022.11.0-beta] - 2022/11/08
_(dmidecode = 3.3 | smartmontools = 7.2 | hwinfo = 21.72 | lshw = 02.19 | lspci = 3.7.0)_
- [added] check for Internet connection and display message accordingly (rel #3653)
- [added] new variable in the settings, VERSION (rel #3998)
- [added] display the path and filename of the json (snapshot)
- [changed] improve the warnings message
- [changed] hardware data retrieval functions within a specific class
  

## [2022.10.1-beta] - 2022/10/26
_(dmidecode = 3.3 | smartmontools = 7.2 | hwinfo = 21.72 | lshw = 02.19 | lspci = 3.7.0)_
- [added] display summary of important data on screen (rel #3943)
- [changed] rename Snapshot ID to SID
- [changed] rename Device ID to DHID
- [changed] rename WB_SNAPSHOT_PATH to SNAPSHOT_PATH on settings
  
## [2022.10.0-beta] - 2022/10/24
_(dmidecode = 3.3 | smartmontools = 7.2 | hwinfo = 21.72 | lshw = 02.19 | lspci = 3.7.0)_
- [added] new environment variable DISABLE_HWINFO (rel #3761)
- [added] new nameserver 8.8.8.8 on debian resolv.conf file (rel #3762) 
- [changed] refactor SID to numeric id based on snapshot_uuid (rel #3940)
- [removed] hashids python dependency

## [2022.8.0-beta] - 2022/08/03
_(dmidecode = 3.3 | smartmontools = 7.2 | hwinfo = 21.72 | lshw = 02.19 | lspci = 3.7.0)_

- [added] both boot compatibility (legacy & uefi)
- [changed] refactor build script (start app abstraction)
- [removed] TODO comments on build script
- [removed] BOOT_TYPE selection

## [2022.5.2-beta] - 2022/05/30
_(dmidecode = 3.3 | smartmontools = 7.2 | hwinfo = 21.72 | lshw = 02.19 | lspci = 3.7.0)_

- [fixed] autologin root user
- [added] WIP uefi compatibility
- [changed] smartctl output is reduced

## [2022.5.1-beta] - 2022/05/24
_(dmidecode = 3.3 | smartmontools = 7.2 | hwinfo = 21.72 | lshw = 02.19 | lspci = 3.7.0)_

- [fixed] set root password correctly to the first build
- [added] settings file using python-decouple
- [added] WIP test suite folder
- [changed] remove sudo dependency
- [changed] settings default path
- [removed] DH_DOMAIN & DH_SCHEMA vars on settings

## [2022.5.0-beta] - 2022/05/14
_(dmidecode = 3.3 | smartmontools = 7.2 | hwinfo = 21.72 | lshw = 02.19 | lspci = 3.7.0)_

- [fixed] timestamp generated in init
- [changed] name workbench lite to workbench core


## [2022.4.1-beta] - 2022/04/30
_(dmidecode = 3.3 | smartmontools = 7.2 | hwinfo = 21.72 | lshw = 02.19 | lspci = 3.7.0)_

- [fixed] timestamp generated in init
- [added] improve feedback printing new labels and steps
- [changed] general code structure corrections 


## [2022.4.0-beta] - 2022/04/20
_(dmidecode = 3.3 | smartmontools = 7.2 | hwinfo = 21.72 | lshw = 02.19 | lspci = 3.7.0)_

- [added] response when snapshot parsing on the server fails
- [added] first functional version of ISO persistence 
- [changed] wbid to sid (snapshot id)  
- [changed] calver scheme to YYYY.MM.PATCH
- [changed] usb name DEBIAN_CUSTOM to WORKBENCH

## [2022.03.3-alpha] - 2022/04/08
_(dmidecode = 3.3 | smartmontools = 7.2 | hwinfo = 21.72 | lshw = 02.19 | lspci = 3.7.0)_

- [fixed] timestamp iso format
- [added] lspci package 
- [added] new save_snapshot function
- [added] new field shcema_api in the snapshot
- [changed] update dict of hw data in snapshot
- [changed] wbid to max 5 characters
- [changed] url to submit snapshot

## [2022.03.2-alpha] - 2022/04/01
_(dmidecode = 3.3-2 | smartmontools = 7.2-1 | hwinfo = 21.72-1 | lshw = 02.19)_

- [fixed] ethernet network debian iso configuration
- [fixed] makefile build_clean function
- [fixed] debian packages requirements installation
- [added] makefile build_bullseye function
- [added] makefile install_WB_dependencies function
- [added] testing user@dhub.com token hardcored on submit function
- [changed] build script installation WB dependencies
- [changed] ISO name file generated by build script
- [changed] update README.md

## [2022.03.1-alpha] - 2022/03/30

- [fixed] minor changes in getting smart info
- [added] improve resilience with try catch when data is collected
- [added] boot_iso makefile function
- [added] autologin on debian starts

## [2022.03.0-alpha] - 2022/03/25

- [added] lshw package 
- [added] build script to generate live ISO image
- [added] submit snapshot function to server
- [added] makefile to run, test and build
- [added] new wbid hash of snapshot uuid 
- [added] requirements package files for python and debian 
- [changed] snapshot file name {date}_{wbid}_snapshot.json
- [changed] versioning system (semantic to calver)

## [14.0.0] - 2022/01/30
- [added] get dmi table data using dmidecode package
- [added] generate and save snapshot.json with dmidecode output
