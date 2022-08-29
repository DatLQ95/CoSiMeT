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
# Design a container to contain and run the code within the container!
# The container must be able to reach out to connect to outside using ethernet interface!
# Set up CI/CD, the github get the code and then build a container from it, then ready to deploy?

# TODO: check if the CS server is detaching the terminal while connection.




