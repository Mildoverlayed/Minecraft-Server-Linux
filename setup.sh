#!/bin/bash

cat /etc/os-release
echo "NEW LINE"
os_name=$(sed -n 's/^NAME=//p' /etc/os-release | sed 's/^"\(.*\)"$/\1/')

if [ -z "$os_name" ]; then
    echo "Operating system name could not be determined."
elif 
fi