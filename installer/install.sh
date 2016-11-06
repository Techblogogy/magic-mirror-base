#!/usr/bin/env bash

# This is a basic Magic Mirror installation image

# NOTE: Make sure you install this on clean Raspbian Jessie image
# for maximum compatability

# === System (Part 1)

# Apt-Update
# echo -e "\e[35mUpdating linux repositories\e[0m"
# sudo apt-get update


# === Repository Clone
cd ~

# Getting Magic Mirror Repository
echo -e "\e[35mDownloading Magic Mirror repository\e[0m"
if git clone https://github.com/Techblogogy/magic-mirror-base.git; then
    echo -e "\e[32mRepository downloaded\e[0m"
else
    echo -e "\e[31mRepository download failed\e[0m"
    exit;
fi

cd ~/magic-mirror-base || exit


# === NodeJS

# Install NodeJS
echo " "
echo -e "\e[35mInstalling NodeJS\e[0m"
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install -y nodejs
echo -e "\e[32mNodeJS Installed\e[0m"

# Npm install
echo " "
echo -e "\e[35mInstalling javascript packages\e[0m"
if npm install; then
    echo -e "\e[35mJS Packages installed\e[0m"
else
    echo -e "\e[31mJS Packages install failed"
    exit;
fi


# === Python

cd ~/magic-mirror-base/server || exit

# Install Python Dependencies
echo " "
echo -e "\e[35mInstalling Python-dev\e[0m"
if sudo apt-get install -y python-dev; then
    echo -e "\e[32mPython Dev installed\e[0m"
else
    echo -e "\e[31mPython Dev install failed"
    exit;
fi

# Install pip
echo " "
echo -e "\e[35mInstalling pip\e[0m"
if sudo apt-get install -y python-pip; then
    echo -e "\e[32mPip installed\e[0m"
else
    echo -e "\e[31mPip install failed"
    exit;
fi

# Install Pyaudio
echo " "
echo -e "\e[35mInstalling Pyaudio\e[0m"
if sudo apt-get install -y python-pyaudio; then
    echo -e "\e[32mPyaudio installed\e[0m"
else
    echo -e "\e[31mPyaudio install failed"
    exit;
fi

# Install Pip Dependencies
echo " "
echo "\e[35mInstalling pip dependencies. This may take a while, please wait...\e[0m"
if sudo pip install -r requirments.txt; then
    echo -e "\e[32mPip dependencies installed\e[0m"
else
    echo -e "\e[31mPip dependencies install failed"
    exit;
fi


# === Python (Part 2)

# Add Mirror executable to bin
echo " "
echo -e "\e[35mAdding application to Bin\e[0m"
chmod a+x mirror

if sudo ln -s ~/magic-mirror-base/server/mirror /usr/local/bin; then
    echo -e "\e[32mAdded application to bin\e[0m"
else
    echo -e "\e[31mAdding application to bin failed"
    exit;
fi

# TODO: Copy resources
mkdir ~/.local/share/mirror_server
cd ~/magic-mirror-base/installer

cp -avr ~/magic-mirror-base/installer/data/ ~/.local/share/mirror_server


# TODO: Copy Config File

# TODO: Autostart

# TODO: Splash screen
