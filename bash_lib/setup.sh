#!/bin/bash
set -eux

### How to install homebrew:
### https://brew.sh/

# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

### How to install docker: 
### https://stackoverflow.com/questions/32744780/install-docker-toolbox-on-a-mac-via-command-line

# Install docker toolbox
brew cask install docker-toolbox

# Install docker
brew cask reinstall docker

open /Applications/Docker.app

echo("Waiting for docker to open...")
sleep 30

docker login