cat /etc/os-release
echo "NEW LINE"
sed -n 's/^NAME="\?\(.*\)"\?/\1/p' /etc/os-release