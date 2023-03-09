# Presentator
 A Discord bot that generates FULL powerpoints about a given subject thanks to openai's gpt3.
 
 <img src="https://raw.githubusercontent.com/Paillat-dev/presentator/main/examples/steve-jobs/Steve-Jobs-1.png"  width="600" >
 <img src="https://raw.githubusercontent.com/Paillat-dev/presentator/main/examples/python/the-python-programming-language-1.png"  width="600" >
 
 
# How it works
- The bot sends a request to the openai api with the given subject and indications in the marp markdown format
- We extract the images from the markdown and send them to the image generation api
- We generate the pdf and html files from the markdown
- We send the pdf and html files to the user

# How to install
**IMPORTANT** Linux and MacOS installation isn't documented yet, if anyone wanths to complete it, feel free to do a pull request.
## Requirements
- Python 3.8 https://www.python.org/downloads/
- Pip https://pip.pypa.io/en/stable/installation/
- A Discord bot token https://www.writebots.com/discord-bot-token/
- An openai api key https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key
- (Optional) An Nvidia GPU (for local image generation)

## Installation
- Clone the repository
- Install the requirements with 
`pip install -r requirements.txt`
- Download the correct zip / tar marp file for your os [here](https://github.com/marp-team/marp-cli/releases/tag/v2.3.0).
- Extract the content of that file in the presentator folder (the one you downloaded on step 1).
- Restart your computer
- Put your openai api key and discord bot token in the `.env.example` file and rename it to `.env`

## Image generation (optional)
### With Stable Diffusion UI (powerful gpu option)
- **Do not use this option if you don't understand what you are doing!**
- Install [Stable Diffusion UI](https://github.com/cmdr2/stable-diffusion-ui) and switch to the `beta` branch.
- Copy the `./image_gen_api/main.py` file to the `stable-diffusion-ui` folder
- Open the file called `Dev Console.cmd` in the `stable-diffusion-ui` folder and run the following commands:
```
pip install uvicorn
pip install fastapi
```
- In the file `.env`, set the `USE_IMAGES` variable to `sd`
### With DALL·E 2 (costs dalle credits)
- In the file `.env`, set the `USE_IMAGES` variable to `dalle`
# Running
- Run the `main.py` file with :
```
python main.py
```

### Local image generation (optional, only if you use the local image generation option)
- Open the file called `Dev Console.cmd` in the `stable-diffusion-ui` folder and run the following commands:
```
uvicorn main:app --reload
```

# Commands
- `/present` : Generates a pdf presentation about the given subject
  
   Options:
    - `subject` : The subject of the presentation
    - `language` : The language of the presentation (default: `english`)
    - `style` : The style of the presentation (default: `default`)
    - `indications` : Some more instructions about how the presentation should be generated (default: `None`)
- `/list` : Lists all of your presentations
- `/get` : Gets a presentation by its id another time

# Help
You can join our discord server if you need help
https://discord.gg/pB6hXtUeDv

Have fun!
