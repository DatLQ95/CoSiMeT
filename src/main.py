#!/usr/bin/env python3
from src.Program import Program


def main():
    program = Program()
    while (True):
        program.run()
    # print("hello")


if __name__ == "__main__":
    main()

# TODO:
# Dev job:
# Arrow in the text when we adding something.
# Auto remove the key after the server is added. -> Need to discuss again!
# Test all the current features : upgrade/ http certificate update.
# Develop http certificate and upgrade new version at the same time!
# About the certificate feature 
# Host a storage server for all the license, then query from there? 
#
# FEature: Automatic tunneling for connection via lapgaps PC. 
# Check if it is pingable from the CS server, if not -> print out to do tunneling manually.
# 
# DevOps:
# Write the doc how to use the program.
# Set up Jenkins to deploy dev branch to test server / master branch on the prod server
# Test the code after we build it in staging environment!
# Back up the DB into difference machine?
# Yellow for the expired certificate.
# Add the SSH command printout in the first screen. 


# TODO:
# Write a more brief report, summarize info in better way, how better -> ask Glicci!.
#
# Finish certificate renewal, need to test to verify
# Who did what ? on which server? which action already taken on each server.
# Transfer info from config to mysql database
# And build it again!
#
#
# TODO: Security:
# Security for the DB best practice.
# add exception handling for every outsider module!
# Change the encryption key feature!
#
#
# keyclack
# For upgrade: check the old values of the installation, keycloack and
# check if the values is existed? If not,

# Task: to estimate how many devices get affected. 

# Evaluate the how much percentage are affected -> we have included the fix in new FW patch already.

# Observae that roughly some percentage still affected 

# Solution -> Replace with new device with hgiher than a certain 

# Even the 2% malfunctioning with ACS server but still can be provisioned by CS -> not 
