#!/usr/bin/env python3
from Program import Program

def main():
    program = Program()
    while (True):
        program.run()

if __name__ == "__main__":
    main()

# TODO: 
# Dev job: 
# Access the server using Ansible ssh key.
# Access multiple servers: nl-cs and demoportal.
# Store the key using hash algorithm.
# Feature: update the CS version in update server status/ checking connection.
# Feature: upgrade server version.

# New Ansible module need to be tested /
# Prepare the host files / variables files/  
# Using CLI to run playbook 
# get the result and analyze it 
# Return to the variables and save it to database!
# Save the result to the result folder

# DevOps: 
# set up connection to gerrit.
# Set up Jenkins job to build the python code everytime we commit code in Gerrit.
# Set up Jenkins job to test the code!?
# Set up Countinuos Deployment to deploy to our internal machine.





