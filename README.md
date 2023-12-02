# VitalPBX - AI Operator
Project that shows how to implement an AI Operator in VitalPBX using OpenaAI Assistances.
## Necessary Resources
1.	OpenAI Account (https://platform.openai.com/apps).
2.	Microsoft Azure Account (https://azure.microsoft.com/en-us/products/ai-services/text-to-speech)
3.	VitalPBX 4

## Installing dependencies
<pre>
  apt update
  apt install python3 python3-pip
  pip install azure-cognitiveservices-speech
</pre>

<pre>
  wget https://raw.githubusercontent.com/VitalPBX/vitalpbx_agent_ai_chatgpt/main/requirements.txt
</pre>

<pre>
  pip install -r requirements.txt
</pre>

## Install from script
Download the script
<pre>
  wget https://raw.githubusercontent.com/VitalPBX/vitalpbx_agent_ai_chatgpt/main/install.sh
</pre>

Give execution permissions
<pre>
  chmod +x install.sh
</pre>

Run the script
<pre>
  ./install.sh
</pre>

## Create .env file
Goto AGI directory
<pre>
  cd /var/lib/asterisk/agi-bin/
</pre>

Creating .env
<pre>
  nano .env
</pre>

Copy the following content and add the APIS Key.
<pre>
OPENAI_API_KEY = "sk-"
AZURE_SPEECH_KEY = ""
AZURE_SERVICE_REGION = "eastus"
PATH_TO_DOCUMENTS = "/var/lib/asterisk/agi-bin/docs/"
PATH_TO_DATABASE = "/var/lib/asterisk/agi-bin/data/"
</pre>

## Create voice guides
Goto AGI directory
<pre>
  cd /var/lib/asterisk/agi-bin/
</pre>

The format to record a prompt is as follows:
./record-prompt.py <strong>file-name "Text to record" language</strong><br>
<strong>file-name</strong> --> file name if extension mp3, remember that in the Agent AI script, the welcome audio is: welcome-en (English), welcome-es (Spanish), and the wait audio is: wait-en (English), and wait-es (Spanish).<br>
<strong>languaje</strong> --> could be "en-US" or "es-ES"<br>
If you want to add more languages, you must modify the scripts<br>

Below we show an example of how you should use the script to record the prompt.
<pre>
./record-prompt.py wait-en "Just a moment, please. We're fetching the information for you." "en-US"
./record-prompt.py welcome-en "Welcome to the Artificial intelligence Assistant. Please ask your question after the tone." "en-US"
./record-prompt.py short-message-en "Your question is too short. Please provide more details." "en-US"
./record-prompt.py anything-else-en "Can I assist you with anything else?" "en-US"  
./record-prompt.py wait-es "Un momento, por favor. Estamos buscando la información para ti." "es-ES"
./record-prompt.py welcome-es "Bienvenido al Asistente de Inteligencia Artificial, Haga su pregunta después del tono." "es-ES"
./record-prompt.py short-message-es "Tu pregunta es demasiado corta. Por favor, proporciona más detalles." "es-ES"
./record-prompt.py anything-else-es "¿Hay algo más en lo que pueda ayudarte?" "es-ES"  
</pre>

