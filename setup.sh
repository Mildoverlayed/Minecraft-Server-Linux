OS=$(sed -n 's/^NAME=//p' /etc/os-release | sed 's/^"\(.*\)"$/\1/')
echo "Detected OS: $OS"
if [ "$OS" = "Debian GNU/Linux" ]; then
    jq '.DISTRO = "Debian GNU/Linux"' config.json > config.tmp && mv config.tmp config.json
    sudo apt update && sudo apt install -y
    sudo apt-get -q update
    sudo apt-get -yq install gnupg curl
    sudo apt-key adv \
    --keyserver hkp://keyserver.ubuntu.com:80 \
    --recv-keys 0xB1998361219BD9C9
    curl -O https://cdn.azul.com/zulu/bin/zulu-repo_1.0.0-2_all.deb
    sudo apt-get install ./zulu-repo_1.0.0-2_all.deb
    sudo apt-get update
    sudo apt install tmux -y
    # Install gotop (latest .deb from v4.2.0 release)
    GOTOP_URL=$(curl -s https://api.github.com/repos/xxxserxxx/gotop/releases/tags/v4.2.0 \
      | grep "browser_download_url" \
      | grep "amd64.deb" \
      | cut -d '"' -f 4 | head -n 1)

    if [ -n "$GOTOP_URL" ]; then
        wget "$GOTOP_URL" -O gotop.deb
        sudo dpkg -i gotop.deb
        rm gotop.deb
    else
        echo "Could not find gotop .deb package for v4.2.0"
    fi
    sudo apt-get install jq -y
    sudo apt-get install -y zulu8-ca-jre-headless
    sudo apt-get install -y zulu17-ca-jre-headless
    sudo apt-get install -y zulu21-ca-jre-headless
    sudo apt install python3 -y
    sudo apt install python3-pip -y

elif [ "$OS" = "Ubuntu" ]; then
    jq '.DISTRO = "Ubuntu"' config.json > config.tmp && mv config.tmp config.json
    sudo apt update && sudo apt install -y
    sudo apt-get install jq -y
    sudo apt install tmux -y

    # Install gotop (latest .deb from v4.2.0 release)
    GOTOP_URL=$(curl -s https://api.github.com/repos/xxxserxxx/gotop/releases/tags/v4.2.0 \
      | grep "browser_download_url" \
      | grep "amd64.deb" \
      | cut -d '"' -f 4 | head -n 1)

    if [ -n "$GOTOP_URL" ]; then
        wget "$GOTOP_URL" -O gotop.deb
        sudo dpkg -i gotop.deb
        rm gotop.deb
    else
        echo "Could not find gotop .deb package for v4.2.0"
    fi

    sudo apt install openjdk-8-jre-headless -y
    sudo apt install openjdk-17-jre-headless -y
    sudo apt install openjdk-21-jre-headless -y
    sudo apt install python3 -y
    sudo apt install python3-pip -y

else
    echo "Unsupported OS: $OS"
    echo "Please use Debian or Ubuntu." 
    exit 1
fi

jq '.SETUP = true' config.json > config.tmp && mv config.tmp config.json

clear
echo "Java installation complete."
echo "would you like to install a test server it is a vanilla server with no mods See more at https://github.com/Mildoverlayed/Example-Minecraft-Server (Y/n)"
read -r install_test_server
if [[ "$install_test_server" = "Y" || "$install_test_server" = "y" ]]; then
    echo "Installing test server..."
    cd Instances 
    git clone https://github.com/Mildoverlayed/Example-Minecraft-Server.git
    echo "Test server installed in Instances/Example-Minecraft-Server"
    echo "To run the server, run server.py and follow the instructions."
else
    echo "Skipping test server installation."
    echo "You can manually clone the repository later if needed."
    echo "Thank you for using My Minecraft Server Manager!"
    exit 1
fi


exit 0