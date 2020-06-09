#!/bin/bash

set -x
set -e

source .env

open -a /Applications/Firefox.app "https://discordapp.com/oauth2/authorize?client_id=${DISCORD_TOKEN}&scope=bot&permissions=536872960"
