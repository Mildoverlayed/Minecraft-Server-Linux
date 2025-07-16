OS=$(sed -n 's/^NAME=//p' /etc/os-release | sed 's/^"\(.*\)"$/\1/')
echo "Detected OS: $OS"

if [ "$OS" = "Debian GNU/Linux" ]; then
    sudo apt update && sudo apt install -y
    sudo apt-get -q update
    sudo apt-get -yq install gnupg curl
    sudo apt-key adv \
    --keyserver hkp://keyserver.ubuntu.com:80 \
    --recv-keys 0xB1998361219BD9C9
    curl -O https://cdn.azul.com/zulu/bin/zulu-repo_1.0.0-2_all.deb
    sudo apt-get install ./zulu-repo_1.0.0-2_all.deb
    sudo apt-get update


    
elif [ "$OS" = "Ubuntu" ]; then
    sudo apt update && sudo apt install -y
    sudo apt install openjdk-8-jre-headless -y
    sudo apt install openjdk-17-jre-headless -y
    sudo apt install openjdk-21-jre-headless -y

elif [ "$OS" = "Fedora" ]; then
    echo "fed"
elif [ "$OS" = "Arch Linux" ]; then
    echo "arch"
elif [ "$OS" = "Manjaro Linux" ]; then
    echo "manjaro"
else
    echo "Unsupported OS: $OS"
    exit 1
fi