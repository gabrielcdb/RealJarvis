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

## ⚠️ Limitations 

This experiment aims to showcase the potential of GPT as a AI functionnal assistant but comes with some limitations:

1. Not a polished application or product, just an experiment
2. May not perform well in complex, real-world business scenarios. In fact, if it actually does, please share your results!
3. Quite expensive to run, so set and monitor your API key limits with OpenAI!

## 🛡 Disclaimer

This project, TheRealJarvis, is an experimental application and is provided "as-is" without any warranty, express or implied. By using this software, you agree to assume all risks associated with its use, including but not limited to data loss, system failure, or any other issues that may arise.

The developers and contributors of this project do not accept any responsibility or liability for any losses, damages, or other consequences that may occur as a result of using this software. You are solely responsible for any decisions and actions taken based on the information provided by TheRealJarvis.

**Please note that the use of the GPT-4 language model and elevenlabs voice model can be expensive due to its token usage.** By utilizing this project, you acknowledge that you are responsible for monitoring and managing your own token usage and the associated costs. It is highly recommended to check your OpenAI API usage regularly and set up any necessary limits or alerts to prevent unexpected charges.

As an autonomous experiment, TheRealJarvis may generate content or take actions that are not in line with real-world business practices or legal requirements. It is your responsibility to ensure that any actions or decisions made based on the output of this software comply with all applicable laws, regulations, and ethical standards. The developers and contributors of this project shall not be held responsible for any consequences arising from the use of this software.

By using TheRealJarvis, you agree to indemnify, defend, and hold harmless the developers, contributors, and any affiliated parties from and against any and all claims, damages, losses, liabilities, costs, and expenses (including reasonable attorneys' fees) arising from your use of this software or your violation of these terms.

//Special thanks for the adintool data segmentation very functional tool provided as part of Julius speech recognition tool
    see : https://github.com/julius-speech/julius/tree/master/adintool

    Also, The LEE_UENO model refered in the code is a model I have localy but can't share since it was provided to me in a Scholar work by my laboratory Sensei at Nagoya Institute of Technology, so I pushed it but if I have no return from them saying I can publish it, you will not be able to use it.
    Also, huge thanks to them (Akinobu Lee and Sei Ueno) who introduced me to ASR and speech recognition technologies.