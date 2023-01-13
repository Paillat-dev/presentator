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
## Requirements
- Python 3.8
- Pip
- A Discord bot token
- An openai api key
- (Optional) An Nvidia GPU (for image generation)

## Installation
- Clone the repository
- Install the requirements with 
`pip install -r requirements.txt`
- Install scoop (if not alredy installed) by typing the following commands:
```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
```
- Install marp by doing
```
scoop install marp
```
- Restart your computer
- Create a file named `key.env` and put your openai api key in it
- Create a file named `token.env` and put your discord bot token in it
- In the main.py file, at the first line, enable or disable the image generation (by default it's disabled)
```python
# Enable or disable image generation
use_images = False
```

### Image generation (optional)
- Install [Stable Diffusion UI](https://github.com/cmdr2/stable-diffusion-ui) and switch to the `beta` branch.
- Copy the `./image_gen_api/main.py` file to the `stable-diffusion-ui` folder
- Open the file called `Dev Console.cmd` in the `stable-diffusion-ui` folder and run the following commands:
```
pip install uvicorn
pip install fastapi
```

# Running
- Run the `main.py` file with :
```
python main.py
```

### Image generation (optional)
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
