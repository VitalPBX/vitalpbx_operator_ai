#!/bin/bash
# This code is the property of VitalPBX LLC Company
# License: Proprietary
# Date: 2-Dec-2023
# VitalPBX AI Operator

# Exit on any error
set -e

# Display a welcome message
echo -e "************************************************************"
echo -e "*         Welcome to the AI Operator installation          *"
echo -e "************************************************************"

# Change directory to the AGI scripts location
cd /var/lib/asterisk/agi-bin/

# Download required scripts from GitHub
wget https://raw.githubusercontent.com/VitalPBX/vitalpbx_operator_ai/main/operator-ai.py -P /var/lib/asterisk/agi-bin/
wget https://raw.githubusercontent.com/VitalPBX/vitalpbx_operator_ai/main/record-prompt.py -P /var/lib/asterisk/agi-bin/

# Set execute permissions for the downloaded scripts
chmod +x /var/lib/asterisk/agi-bin/operator-ai.py
chmod +x /var/lib/asterisk/agi-bin/record-prompt.py

# Download Asterisk configuration file
wget https://raw.githubusercontent.com/VitalPBX/vitalpbx_operator_ai_chatgpt/main/extensions__71-operator-ai.conf -P /etc/asterisk/vitalpbx/

# Reload the Asterisk dialplan
asterisk -rx "dialplan reload"

# Display installation instructions
echo -e "\n"
echo -e "************************************************************"
echo -e "*         Remember to first create the .env file           *"
echo -e "*        with your OpenAI and Azure credentials.           *"
echo -e "*            And then create the Voice Guides              *"
echo -e "************************************************************"
echo -e "\n"
echo -e "************************************************************"
echo -e "*       All components have been installed correctly       *"
echo -e "*                To ask ChatGPT questions                  *"
echo -e "*        Dial *885 for English or *886 for Spanish         *"
echo -e "*  Remember to create the Assistants on the OpenAI website *"
echo -e "*   and you must upload a Phonebook with the name or area  *"
echo -e "*            and corresponding extension numbers.          *"
echo -e "************************************************************"
