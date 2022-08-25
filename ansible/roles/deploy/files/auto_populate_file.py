#!/usr/bin/python

import sys
import os

domain_name = sys.argv[1]
license_component_name = sys.argv[2]
license_component_secret = sys.argv[3]
freeacs_install = sys.argv[4]
aws_accessKey_id = sys.argv[5]
aws_accessKey_secret = sys.argv[6]
aws_region = sys.argv[7]
aws_maintainer_email = sys.argv[8]


hostname_line = "iopsys.hostname"
license_component_name_line = "iopsys.license.component.name"
license_component_secret_line = "iopsys.license.component.secret"

freeacs_install_line = "freeacs.install"
aws_accessKey_id_line = "aws.accessKey.id"
aws_accessKey_secret_line = "aws.accessKey.secret"
aws_region_line = "aws.region"
aws_maintainer_email_line = "aws.maintainer.email"

new_line = list()

with open("installation.properties", "r") as f:
    lines = f.readlines()

with open("installation_values.txt", "r") as f:
    default_lines = f.readlines()

found_license_component_line = False
found_license_component_secret = False
found_default_line = False
found_aws_access_key = False

for line in lines:
    if hostname_line in line.strip("\n"):
        new_line.append(hostname_line + "=" + domain_name + "\n")
        continue
    if license_component_name_line in line.strip("\n"):
        found_license_component_line = True
        new_line.append(license_component_name_line + "=" + license_component_name + "\n")
        continue
    if license_component_secret_line in line.strip("\n"):
        found_license_component_secret = True
        new_line.append(license_component_secret_line + "=" + license_component_secret + "\n")
        continue
    if aws_accessKey_id_line in line.strip("\n"):
        found_aws_access_key = True
        new_line.append(aws_accessKey_id_line + "=" + aws_accessKey_id + "\n")
        new_line.append(aws_accessKey_secret_line + "=" + aws_accessKey_secret + "\n")
        new_line.append(aws_region_line + "=" + aws_region + "\n")
        new_line.append(aws_maintainer_email_line + "=" + aws_maintainer_email + "\n")
        continue
    if freeacs_install_line in line.strip("\n"):
        new_line.append(freeacs_install_line + "=" + freeacs_install + "\n")
        continue
    if line in default_lines:
        found_default_line = True
    new_line.append(line)

if not found_default_line:
    new_line.append("\n")
    new_line = new_line + default_lines
    new_line.append("\n")
    new_line.append("\n")

# If the line is not there, then we add it, if it is there, we replace it: 

if not found_license_component_line:
    new_line.append(license_component_name_line + "=" + license_component_name + "\n")
if not found_license_component_secret:
    new_line.append(license_component_secret_line + "=" + license_component_secret + "\n")
if not found_aws_access_key:
    new_line.append(aws_accessKey_id_line + "=" + aws_accessKey_id + "\n")
    new_line.append(aws_accessKey_secret_line + "=" + aws_accessKey_secret + "\n")
    new_line.append(aws_region_line + "=" + aws_region + "\n")
    new_line.append(aws_maintainer_email_line + "=" + aws_maintainer_email + "\n")

with open("installation.properties", "w") as f:
    for line in new_line:
        f.write(line)
