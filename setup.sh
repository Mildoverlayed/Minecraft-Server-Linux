#!/bin/bash

os_name=$(sed -n 's/^NAME=//p' /etc/os-release | sed 's/^"\(.*\)"$/\1/')

if [ -z "$os_name" ]; then
    echo "Operating system name could not be determined. And or is not supported."
elif [ "$os_name" == "Debian GNU/Linux" ]; then
    echo "Deb"
fi