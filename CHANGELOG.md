# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Calendar Versioning](https://calver.org/#scheme) scheme (`YYYY.MM.PATCH`).

## prod
[2022.03.0-alpha]

## preprod
[2022.03.0-alpha]

----

## [Unreleased]
- [added] improve resilience with try catch when data is collected
- [added] bootiso makefile function
- [added] autologin on debian starts

## [2022.03.00-alpha] - 2022/03/25

- [added] lshw package 
- [added] build script to generate live ISO image
- [added] submit snapshot function to server
- [added] Makefile to run, test and build
- [added] new wbid hash of snapshot uuid 
- [added] requirements package files for python and debian 
- [changed] snapshot file name {date}_{wbid}_snapshot.json
- [changed] versioning system (semantic to calver)

## [14.0.0] - 2022/01/30
- [added] get dmi table data using dmidecode package
- [added] generate and save snapshot.json with dmidecode output
