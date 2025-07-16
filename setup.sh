cat /etc/os-release
echo "NEW LINE"
sed -n 's/^NAME=//p' /etc/os-release | sed 's/^"\(.*\)"$/\1/'