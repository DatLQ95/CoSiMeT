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
# Store the key using hash algorithm.

# DevOps: 
# set up connection to gerrit.
# Set up Jenkins job to build the python code everytime we commit code in Gerrit.
# Set up Jenkins job to test the code!?
# Set up Countinuos Deployment to deploy to our internal machine.
