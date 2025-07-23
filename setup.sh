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
    curl -O https://github.com/xxxserxxx/gotop/releases/download/v4.2.0/gotop_v4.2.0_linux_amd64.deb
    sudo dpkg -i gotop_v4.2.0_linux_amd64.deb
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
    curl -O https://github.com/xxxserxxx/gotop/releases/download/v4.2.0/gotop_v4.2.0_linux_amd64.deb 
    sudo dpkg -i gotop_v4.2.0_linux_amd64.deb
    sudo apt install openjdk-8-jre-headless -y
    sudo apt install openjdk-17-jre-headless -y
    sudo apt install openjdk-21-jre-headless -y
    sudo apt install python3 -y
    sudo apt install python3-pip -y

else
    echo "Unsupported OS: $OS"
    echo "Please use Debian or Ubuntu. Ubuntu is recommended." 
    exit 1
fi
echo "package installation complete."

echo "seting file permissions"
chmod 777 config.json
chmod 777 server.py
chmod 777 Instances

echo "\n\n\n"

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

jq '.SETUP = true' config.json > config.tmp && mv config.tmp config.json

echo "\n\n\n"
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
    echo "Please move the server version you want to use into the Instances folder."
else
    echo "Skipping test server installation."
    echo "You can manually clone the repository later if needed."
    exit 1
fi
    echo "Thank you for using My Minecraft Server Manager!"

exit 0