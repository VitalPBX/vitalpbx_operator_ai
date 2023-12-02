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
OPENAI_ASSISTANT_ID = "asst_"
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
./record-prompt.py op_ai_welcome-en "I am your AI Operator, after hearing the tone, could you please tell me the name of the person or the area you wish to communicate with?" "en-US"
./record-prompt.py op_ai_wait-en "Please wait while I search for the extension number." "en-US"
./record-prompt.py op_ai_transfer-en "Thank you for your patience. We are currently transferring your call to the appropriate party. Please hold." "en-US"
./record-prompt.py op_ai_short-message-en "Your message is too short, please try again." "en-US"
./record-prompt.py op_ai_user_not_found-en "I'm sorry, we were unable to find the information you requested. Please try again." "en-US"
./record-prompt.py op_ai_multiple_users-en "Multiple matches have been found, could you be more specific please." "en-US"
./record-prompt.py op_ai_welcome-es "Soy su Operador de IA, despues de escuchar el tono, ¿podría decirme el nombre de la persona o el área con la que desea comunicarse?" "es-ES"
./record-prompt.py op_ai_wait-es "Espere mientras busco el número de extensión." "es-ES"
./record-prompt.py op_ai_transfer-es "Gracias por su paciencia. Actualmente estamos transfiriendo su llamada al interlocutor correspondiente. Por favor espera." "es-ES"
./record-prompt.py op_ai_short-message-es "Tu mensaje es demasiado corto, inténtalo de nuevo." "es-ES"
./record-prompt.py op_ai_user_not_found-es "Lo sentimos, no pudimos encontrar la información que solicitaste. Inténtalo de nuevo." "es-ES"
./record-prompt.py op_ai_multiple_users-es "Se han encontrado varias coincidencias, ¿podría ser más específico, por favor?" "es-ES"
</pre>

