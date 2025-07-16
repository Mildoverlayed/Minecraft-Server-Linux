#!/bin/bash

echo "Before we start, we need to know what package manager to use. 1-5"
echo "[1.] APT"
echo "[2.] DPKG"
echo "[3.] RPM"
echo "[4.] Flatpak"
echo "[5.] Pacman"
read package_manager
if [ "$package_manager" -eq 1 ]; then
    apt update && apt upgrade -y
    apt install openjdk-8-jre-headless -y
    apt install openjdk-17-jre-headless -y
    apt install openjdk-21-jre-headless -y



elif [ "$package_manager" -eq 2 ]; then
    echo "You selected DPKG."
elif [ "$package_manager" -eq 3 ]; then
    echo "You selected RPM."
elif [ "$package_manager" -eq 4 ]; then
    echo "You selected Flatpak."
elif [ "$package_manager" -eq 5 ]; then
    echo "You selected Pacman."
else
    echo "Invalid selection. Please run the script again and select a valid option."
    exit 1
fi