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
    sudo apt install pip3-pytz -y

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

echo "we now need to set the timezone for the server, please enter your timezone (e.g. Europe/London, America/New_York):"
echo "You can find your timezone at https://en.wikipedia.org/wiki/List_of_tz_database_time_zones make sure to use the TZ identifier."
read -r timezone
jq --arg timezone "$timezone" '.ZONE = $timezone' config.json > config.tmp && mv config.tmp config.json

jq '.SETUP = true' config.json > config.tmp && mv config.tmp config.json

echo "Would you like to use ngrok for outside local network access? (Y/n)"
read -r use_ngrok
if [[ "$use_ngrok" = "Y" || "$use_ngrok" = "y" ]]; then
    echo "Installing ngrok..."
    curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
  && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list \
  && sudo apt update \
  && sudo apt install ngrok
    echo "Ngrok installed. Please run 'ngrok authtoken YOUR_AUTH_TOKEN' to set up your account."
    echo "You can get your auth token from https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "please enter your ngrok authtoken:"
    read -r ngrok_token
    ngrok config add-authtoken "$ngrok_token"
    echo "Ngrok authtoken set successfully."
    echo "You can now use ngrok to expose your Minecraft server to the internet."
    jq '.NGROK = true' config.json > config.tmp && mv config.tmp config.json

else
    echo "Skipping ngrok installation."
    echo "You can install it later if needed."
fi

echo "Java installation complete."
echo "would you like to install a test server it is a vanilla server with no mods See more at https://github.com/Mildoverlayed/Example-Minecraft-Server or Custom "C" (Y/n/C)"
read -r install_test_server
if [[ "$install_test_server" = "Y" || "$install_test_server" = "y" ]]; then
    echo "Installing test server..."
    cd Instances 
    git clone https://github.com/Mildoverlayed/Example-Minecraft-Server.git
    echo "Test server installed in Instances/Example-Minecraft-Server"
    echo "To run the server, run StartServer.sh and follow the instructions."
elif [[ "$install_test_server" = "C" || "$install_test_server" = "c" ]]; then
    echo "Installing custom test server..."
    echo "Please enter the Example-Minecraft-Server Extension:"
    read -r custom_server_url
    git clone "$custom_server_url" Instances/Custom-Minecraft-Server
else
    echo "Skipping test server installation."
    echo "You can manually clone the repository later if needed."
    echo "Thank you for using My Minecraft Server Manager!"
    exit 1
fi

exit 0