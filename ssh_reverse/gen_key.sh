#!/bin/sh

# TODO afegir-ho en el makefile

printf "\nfor passwordless key press enter two times\n\n"
ssh-keygen -t ed25519 -C "key for usody" -f ./keys/ssh_workbench;
