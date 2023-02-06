import openai
# from openai import api_key
import discord
from discord import Intents
from discord.commands import slash_command, option
from discord.ext import commands
import re
import os
import asyncio
import logging
import datetime
import base64
import requests
from dotenv import load_dotenv
load_dotenv()
use_images = os.getenv("USE_IMAGES")
cooldown = os.getenv("COOLDOWN")
if use_images != "No": import imagesGeneration
logging.basicConfig(level=logging.INFO)
imageint = ""
if use_images != "No": imageint = "To add an image illustration , use ![bg left:50% 70%](a-description-of-the-image.png) at the beginning of the slide, just after \"---\". Use only .png. It's not possible to add technical images but only illustrations. The images are generated by an ai, the name of the file should be a detailed description of the image wanted.  For example \" ![bg left:50% 100%](a-man-wearing-a hat-ryding-a-bicicle.png)\" but don't need to show a person necessairly."
intstructions = f'''Here is a presentation with marp. It's not possible to make slides longer than 200 characters. to separate slides, 
"

---

"
 then go at the line. The presentatio should be for everybody, all technical words and concepts, explained. {imageint} The presentation is minimum 20 slides long. You can use bulletpoints. Use markdown formatting (titles, etc...). The presentation has also a conclusion.'''
bot = discord.Bot()

styles = ["default", "gaia", "uncover", "default-dark", "gaia-dark", "uncover-dark"]
languages = ["english", "french", "spanish", "german", "italian", "portuguese", "russian", "chinese", "japanese", "korean", "arabic"]
darkstyles = ["default-dark", "gaia-dark", "uncover-dark"]
async def get_style(ctx: discord.AutocompleteContext):
    """Returns a list of colors that begin with the characters entered so far."""
    return [color for color in styles if color.startswith(ctx.value.lower())]
async def get_ln(ctx: discord.AutocompleteContext):
    """Returns a list of colors that begin with the characters entered so far."""
    return [color for color in languages if color.startswith(ctx.value.lower())]

@bot.slash_command(name="private_present", description="Generate a presentation with marp, private command for user 707196665668436019")
#we create a function that takes the subject of the presentation and the style of the presentation as arguments, and that
@option(name="subject", description="The subject of the presentation", required=True)
@option(name="style", description="The style of the presentation", required=False, autocomplete=get_style)
@option(name="language", description="The language of the presentation", required=False, autocomplete=get_ln)
@option(name="indications", description="The indications for the presentation", required=False)
#command wprks only in dm and only for user 707196665668436019
@commands.is_owner()
async def private_present(ctx: discord.ApplicationContext, subject: str, style: str = "default", language: str = "english", indications: str = ""):
    await present(ctx, subject, style, language, indications)




@bot.slash_command(name="present", description="Generate a presentation with marp")
#we create a function that takes the subject of the presentation and the style of the presentation as arguments, and that
@option(name="subject", description="The subject of the presentation", required=True)
@option(name="style", description="The style of the presentation", required=False, autocomplete=get_style)
@option(name="language", description="The language of the presentation", required=False, autocomplete=get_ln)
@option(name="indications", description="The indications for the presentation", required=False)
# a cooldown of duration cooldown seconds, except if the user is 707196665668436019

#@commands.cooldown(1, int(cooldown), commands.BucketType.user)
@commands.cooldown(1, int(cooldown), commands.BucketType.guild)
async def normal_present(ctx: discord.ApplicationContext, subject: str, style: str = "default", language: str = "english", indications: str = ""):
    await present(ctx, subject, style, language, indications)


async def present(ctx: discord.ApplicationContext, subject: str, style: str = "default", language: str = "english", indications: str = ""):
    await ctx.defer()
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d-%H-%M-%S")
    marp = f'''---
marp: true
theme: {styles[styles.index(style)]}
class:
    - lead
'''
    if style in darkstyles: marp = marp + f"    - invert\n---"
    else: marp = marp + "\n---"
    prompt = f"{intstructions} {indications} The subject of the presentation is: {subject} The Language is: {language} <|endofprompt|> \n {marp}"    
    subject2 = subject
    subject = subject.replace(" ", "-")
    #we save teh subject in base64 in a variable
    b64 = base64.urlsafe_b64encode(subject.encode("utf-8"))
    #if dosen't exist, create a directory called "userid" where the userid is the id of the user who called the command
    uid = str(ctx.author.id)
    if not os.path.exists("./data/"+uid):
        os.mkdir("./data/"+uid)
    datenow = datetime.datetime.now()
    datenow = datenow.strftime("%Y-%m-%d-%H-%M-%S")
    os.mkdir(f"./data/{uid}/{b64}{datenow}")
    response = await openai.Completion.acreate(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.6,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["<|endofprompt|>"]
    )
    #we save the output in a variable
    output = response["choices"][0]["text"]
    present = marp + output
    ##we save the output in a file called "subject.md"
    matches = re.finditer(r'!\[.*?\]\((.*?)\)', present)
    image_filenames = []
    for match in matches:
        image_filenames.append(match.group(1))
    #we create a text file with the image names and a md file for the presentation with utf8 encoding
    with open(f"./data/{uid}/{b64}{datenow}/{subject}-images.txt", "w", encoding="utf8") as f:
        for image in image_filenames:
            f.write(image + "\n")
    #now we generate the images, if there are any
    if len(image_filenames) > 0 and  use_images!="no":
        #now we first remove the extension from the image filenames by removing the last 4 characters
        image_filenames = [image[:-4] for image in image_filenames]
        print(image_filenames)
        for images in image_filenames:
            #we download the image
            print ("generating image " + images + "with " + str(use_images))
            r = await imagesGeneration.generate(images, f"{os.getcwd()}\\data\\{uid}\\{b64}{datenow}\\", str(use_images), apikey)
            if str(use_images) == "sd": os.rename(f"{os.getcwd()}\\.\\data\\{uid}\\{b64}{datenow}\\{images}_0.png", f"{os.getcwd()}\\data\\{uid}\\{b64}{datenow}\\{images}.png")
            if str(use_images) == "dalle": 
                image_url = r['data'][0]['url']
                img_data = requests.get(image_url).content
                with open(f'./data/{uid}/{b64}{datenow}/{images}.png', 'wb') as handler:
                    handler.write(img_data)
    with open(f"./data/{uid}/{b64}{datenow}/{subject}.md", "w", encoding="utf8") as f: f.write(present)
    #we execute the command to convert the markdown file to a pdf and html file and also generate the first slide image
    current_dir = os.getcwd()
    print(current_dir)
    #cmd = f"./marp --pdf --allow-local-files data/{uid}/{b64}{datenow}/{subject}.md"
    cmd = f"./marp --pdf --allow-local-files {current_dir}/data/{uid}/{b64}{datenow}/{subject}.md"
    #we replace all the ' with \'
    cmd = cmd.replace("'", "\\'")
    os.system(cmd)
    print(cmd)
    #cmd = f"./marp --image png -o ./data/{uid}/{b64}{datenow}/{subject}.png --allow-local-files data/{uid}/{b64}{datenow}/{subject}.md"
    #the above command is not working in docker, so we use the following one
    cmd = f"./marp --image png -o {current_dir}/data/{uid}/{b64}{datenow}/{subject}.png --allow-local-files {current_dir}/data/{uid}/{b64}{datenow}/{subject}.md"
    cmd = cmd.replace("'", "\\'")
    #hopefully this will work in docker
    os.system(cmd)
    print(cmd)
    #cmd = f"./marp --html --allow-local-files data/{uid}/{b64}{datenow}/{subject}.md"

    cmd = f"./marp --html --allow-local-files {current_dir}/data/{uid}/{b64}{datenow}/{subject}.md"
    cmd = cmd.replace("'", "\\'")
    os.system(cmd)
    print(cmd)
    #we create an embed with the first slide imageand send it with the pdf file and the markdown file
    embed = discord.Embed(title=subject2, description="Thanks for using presentator bot. You can download the presentation in different formats (pdf, markdown, html). The images are generated by an ai. If you want to modify your presentation you can use the markdown file. More information about how to modify the file [HERE](https://marp.app).", color=0xaaaaaa)
    files = [discord.File(f"./data/{uid}/{b64}{datenow}/{subject}.pdf"), discord.File(f"./data/{uid}/{b64}{datenow}/{subject}.md"), discord.File(f"./data/{uid}/{b64}{datenow}/{subject}.html"), discord.File(f"./data/{uid}/{b64}{datenow}/{subject}.png")]
    embed.set_image(url=f"attachment://{subject}.png")
    #now we send the embed and all the 4 files (pdf, markdown, html, png) at the same time
    await ctx.respond(embed=embed, files=files)

@bot.slash_command(name="list", description="List all the presentations you have created")
async def list(ctx: discord.ApplicationContext):
    #we create an embed with the list of presentations
    embed = discord.Embed(title="Presentations", description="Here is the list of all the presentations you have created. You can download the presentation in different formats (pdf, markdown, html) by doing `/get` \"*presentation id*\". The images are generated by an ai. If you want to modify your presentation you can use the markdown file. More information about how to modify the file [HERE](https://marp.app).", color=0x00ff00)
    #we get the list of presentations
    liste = await get_presentations(str(ctx.author.id))
    #we add the list of presentations to the embed
    for key in liste:
        embed.add_field(name=f"{liste[key]}", value=f"</get:1063051827010084925> `{key}`", inline=False)
    #now we send the embed
    await ctx.respond(embed=embed, ephemeral=True)

async def get_presentations(uid):
    folders = os.listdir(f"./data/{uid}")
    names = {}
    for folder in folders:
        name = base64.urlsafe_b64decode(folder[2:-20]).decode("utf-8")
        names[folder] = name
    return names

@bot.slash_command(name="get", description="Get a presentation")
@option(name="pid", description="The id of the presentation", required=True)
async def get(ctx: discord.ApplicationContext, pid: str):
    uid = str(ctx.author.id)
    #we get the list of presentations
    liste = await get_presentations(uid)
    #we check if the presentation id is in the list
    if pid in liste:
        #if it is we send the pdf, markdown and html files
        files = [discord.File(f"./data/{uid}/{pid}/{liste[pid]}.pdf"), discord.File(f"./data/{uid}/{pid}/{liste[pid]}.md"), discord.File(f"./data/{uid}/{pid}/{liste[pid]}.html")]
        await ctx.respond(files=files, ephemeral=True)
#when the bot is ready we print a message
@bot.event
async def on_ready():
    print("Bot is ready")
    #if the data directory doesn't exist we create it
    if not os.path.exists("data"):
        os.mkdir("data")
@bot.event
async def on_application_command_error(ctx, error):
    #if there is an error we send a message to the user
    await ctx.respond(f"An error occured: {error}", ephemeral=True)
#get the openai key drom he key.env file
token = os.getenv("TOKEN")
apikey = os.getenv("OPENAI")
openai.api_key = apikey
bot.run(token)