#!/bin/bash
echo -e "\e[33mThis Script requires root privileges"
sudo clear;
echo -e "\e[33mInstalling..."
echo "===================================================="
echo "   Step 1 - Removing old versions (if existent)..."
sudo rm /usr/local/bin/dockerbuilder
sudo rm /usr/local/bin/dbd
echo "   Step 2 - Adding the new version..."
sudo cp ./src/dockerbuilder.py /usr/local/bin/dbd
sudo cp ./src/dockerbuilder.py /usr/local/bin/dockerbuilder
echo "   Step 3 - Applying execution permissions..."
sudo chown $USER:$USER /usr/local/bin/dbd
sudo chown $USER:$USER /usr/local/bin/dockerbuilder
sudo chmod +x /usr/local/bin/dbd
sudo chmod u+x /usr/local/bin/dbd
sudo chmod +x /usr/local/bin/dockerbuilder
sudo chmod u+x /usr/local/bin/dockerbuilder
echo "   Aaaand we're done."
echo "===================================================="
dbd
