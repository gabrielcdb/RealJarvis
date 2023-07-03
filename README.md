# RealJarvis
A working Speech to Speech AI assistant that can interact with you, manage your system, and more!

This project is just a scratch of the potential power of this tool.
You do not hesitate to provide me with ideas to get it better and accomplish better tasks, it's for now working on python but will soon be hosted as a desktop app or maybe an android app. Stay tuned!

Languages suported are ... A lot!
ASR (whisper models allow 96 )
LLM (ChatGPT well, basically any language spoken on internet before 2021, if it has enough speakers)
TTS (-eleven labs multilingual allows English, German, Polish, Spanish, Italian, French, Portuguese, and Hindi
     -gTTS allows any google translation languages, but not yet suported in code, coming soon (you can set it up manually)
     )
     
Required for use:

APIS KEYS, key them secret, never ever push or commit them!

    -openai API KEY : https://platform.openai.com/account/api-keys   ()

    (Optional to get a waayyyyy better voice) 
    -Eleven labs API KEY : https://beta.elevenlabs.io/subscription (Clic on your profile icon, and get the key)

Libraries 

    For Speech recognition:
        -openai
        -whisper

    For Display and sound:
        -pygame (audio playing, and Jarvis display)

    For Text to Speech (pick at least one of them, then set up you disered speeach model):
        -pyttsx3
        -gTTS
        -elevenlabs (best but not free)

    For audio treatment:
        -wave
    
    to install a library you can use: 
        py -m pip install libraryname

    here is a list of all commands I ran:
        For Speech recognition:
            py -m pip install openai
            py -m pip install whisper

        For Display and sound:
            py -m pip install pygame

        For Text to Speech (pick one of them, then set up you disered speeach model)
            py -m pip install pyttsx3
            py -m pip install gTTS
            py -m pip install elevenlabs
            (i don't remember why this one) py -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118



Set up
    -Install python (mine is 3.10)
    -Install libraries
    -Run Jarvis
    -Enter you api keys (they'll be stored locally, the file is in git ignored)
    -Choose your Speech to text model
    -Choose your Text to speech model
    -(coming soon: choose your GPT model)
    -Enjoy your ride

Customization:
    You can create custom methods, to run when GPT detect them!
    Many incoming!


//Special thanks for the adintool data segmentation very functional tool provided as part of Julius speech recognition tool
    see : https://github.com/julius-speech/julius/tree/master/adintool

    Also, The LEE_UENO model refered in the code is a model I have localy but can't share since it was provided to me in a Scholar work by my laboratory Sensei at Nagoya Institute of Technology, so I pushed it but if I have no return from them saying I can publish it, you will not be able too use it.
    Also, huge thanks to them (Akinobu Lee and Sei Ueno) who introduced me to ASR and speech recognition technologies.