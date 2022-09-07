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
# Store the key using hash algorithm.
# deploy feature

# DevOps: 
# Set up Jenkins job to test the python code 
# Set up Jenkins job to send the code to target machine
# Set up Countinuos Deployment to deploy to our internal machine.
# Set up build job in the target machine
# Write the doc how to use the program.

# TODO:
# Write a more brief report, summarize info in better way, how better -> ask Glicci!.

# Finish certificate renewal, need to test to verify
# Who did what ? on which server? which action already taken on each server.
# Transfer info from config to mysql database 
# And build it again!

# TODO: Security:
# Auto remove the key after the server is added.
# Security for the DB best practice.
# Arrow in the text when we adding something.
# Write the upgrade script later!
