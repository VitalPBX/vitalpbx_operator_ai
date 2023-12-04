#!/usr/bin/env python3
import time
import os
import sys
from dotenv import load_dotenv
import openai
from openai import OpenAI
import re
# For Asterisk AGI
from asterisk.agi import *

# Load environment variables from a .env file
load_dotenv("/var/lib/asterisk/agi-bin/.env")
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_ASSISTANT_ID = os.environ.get('OPENAI_ASSISTANT_ID')
OPENAI_INSTRUCTIONS = os.environ.get('OPENAI_INSTRUCTIONS')

client = OpenAI()
thread = client.beta.threads.create()

agi = AGI()

# Check if a file name was provided
uniquedid = sys.argv[1] if len(sys.argv) > 1 else None
context = sys.argv[2] if len(sys.argv) > 1 else None
language = sys.argv[3] if len(sys.argv) > 1 else None
tts_engine = sys.argv[4] if len(sys.argv) > 1 else None
instructions = sys.argv[5] if len(sys.argv) > 1 else None

if uniquedid is None:
    print("No filename provided for the recording.")
    sys.exit(1)

# Check if a file name was provided
recording_path = f"/tmp/rec{uniquedid}"

if language == "es":
    azure_language = "es-ES" 
    azure_voice_name = "es-ES-ElviraNeural"
    wait_message = "/var/lib/asterisk/sounds/op_ai_wait-es.mp3"
    transfer_message = "/var/lib/asterisk/sounds/op_ai_transfer-es.mp3"
    short_message = "/var/lib/asterisk/sounds/op_ai_short-message-es.mp3"
    user_not_found = "/var/lib/asterisk/sounds/op_ai_user_not_found-es.mp3"
    multiple_users = "/var/lib/asterisk/sounds/op_ai_multiple_users-es.mp3"
else:
    azure_language = "en-US" 
    azure_voice_name = "en-US-JennyNeural"
    wait_message = "/var/lib/asterisk/sounds/op_ai_wait-en.mp3"
    transfer_message = "/var/lib/asterisk/sounds/op_ai_transfer-en.mp3"
    short_message = "/var/lib/asterisk/sounds/op_ai_short-message-en.mp3"
    user_not_found = "/var/lib/asterisk/sounds/op_ai_user_not_found-en.mp3"
    multiple_users = "/var/lib/asterisk/sounds/op_ai_multiple_users-en.mp3"

# Files can also be added to a Message in a Thread. These files are only accessible within this specific thread.
# After having uploaded a file, you can pass the ID of this File when creating the Message.

def main():
    try:
        # We send the 'raw' command to record the audio, 'q' for no beep, 2 seconds of silence, '30' max duration, 'y' to overwrite existing file
        sys.stdout.write('EXEC Record ' + recording_path + '.wav,3,30,y\n')
        sys.stdout.flush()
        # We await Asterisk's response
        result = sys.stdin.readline().strip()

        if result.startswith("200 result="):

            # Please wait while I search for the extension number.
            agi.appexec('MP3Player', wait_message)
           
            #DEBUG
            agi.verbose("Successful Recording",2)

            # Once everything is fine, we send the audio to OpenAI Whisper to convert it to Text
            openai.api_key = OPENAI_API_KEY
            audio_file = open(recording_path + ".wav", "rb")
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
            chatgpt_question = transcript.text
            chatgpt_question_agi = chatgpt_question.replace('\n', ' ') 

	    # If nothing is recorded, Whisper returns "you", so you have to ask again.
            if chatgpt_question == "you":
                # Your message is too short, please try again.
                agi.appexec('MP3Player', short_message)
                agi.verbose("Message too short",2)
                sys.exit(1)

            #DEBUG
            agi.verbose("AUDIO TRANSCRIPT: " + chatgpt_question_agi,2)

            message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=chatgpt_question
            )

            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=OPENAI_ASSISTANT_ID,
                instructions=OPENAI_INSTRUCTIONS
            )

            runStatus = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

            # Wait for Assistant to respond
            while runStatus.status != "completed":
                time.sleep(1)
                runStatus = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

            # Get the last message
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )

            response = messages.data[0].content[0].text.value

            #DEBUG
            response_agi = response.replace('\n', ' ')
            agi.verbose("OPERATOR AI RESPONSE: " + response_agi,2)

            extensions = re.findall(r'\d+', response_agi)
            if len(extensions) == 1:
                extension_number = extensions[0]
                agi.verbose("EXTENSION NUMBER: " + extension_number,2)
                # Transferring your call, please hold.
                agi.appexec('MP3Player', transfer_message)
                # Priority to use
                priority = "1"
                # Make the transfer
                agi.set_context(context)
                agi.set_extension(extension_number)
                agi.set_priority(priority)
            elif len(extensions) > 1:
                # Multiple matches have been found, could you be more specific please.
                agi.appexec('MP3Player', multiple_users)
                sys.exit(1)
            else: # Ask Again
                agi.verbose("Extension number not found.")
                # I'm sorry, we were unable to find the information you requested. Please try again.
                agi.appexec('MP3Player', user_not_found)
                sys.exit(1)
        else:
            agi.verbose("Error while recording: %s" % result)

    except Exception as e:
        agi.verbose("ERROR:" + str(e))

if __name__ == "__main__":
    main()
