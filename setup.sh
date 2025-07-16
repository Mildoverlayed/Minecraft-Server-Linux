cat /etc/os-release
echo $(sed -n 's/^NAME=//p' /etc/os-release | sed 's/^"\(.*\)"$/\1/')