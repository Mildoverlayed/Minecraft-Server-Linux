

OS=$(sed -n 's/^NAME=//p' /etc/os-release | sed 's/^"\(.*\)"$/\1/')

if [OS == "Debian GNU/Linux" ]; then
    sudo apt update && sudo apt intall -y

elif [[ $OS == "Ubuntu" ]]; then
    sudo apt update && sudo apt install -y
    sudo apt install openjdk-8-jre-headless
    sudo apt install openjdk-17-jre-headless
    sudo apt install openjdk-21-jre-headless

elif [[ $OS == "Fedora" ]]; then

elif [[ $OS == "Arch Linux" ]]; then

elif [[ $OS == "Manjaro Linux" ]]; then

else
    echo "Unsupported OS: $OS"
    exit 1
fi