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
# Develop multiple upgrade servers
#
#
# DevOps: 
# Write the doc how to use the program.
# Set up Jenkins to deploy dev branch to test server / master branch on the prod server
#
#
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
# Encrypt the info in general_info table!
# Password with blank info (getpass module)
# Change the encryption key feature! 

