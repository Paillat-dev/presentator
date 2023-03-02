import openai
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
import zipfile
from zipfile import ZipFile
from dotenv import load_dotenv
load_dotenv()
use_images = os.getenv("USE_IMAGES")
cooldown = os.getenv("COOLDOWN")
if use_images != "No": import imagesGeneration
logging.basicConfig(level=logging.INFO)
imageint = ""
if use_images != "No": imageint = "To add an image illustration , use ![bg left:50% 70%](a-long-detailed-description-of-the-image.png) at the beginning of the slide, just after \"---\". Use only .png. It's not possible to add technical images but only illustrations. The images are generated by an ai, the name of the file should be a detailed quite long description of the image wanted. You always need to specify the description of the image."
intstructions = f'''Here is a presentation with marp. It's not possible to make slides longer than 200 characters. to separate slides, 
"

---

"
 then go at the line. The presentatio should be for everybody, all technical words and concepts, explained. {imageint} The presentation is minimum 20 slides long. You can use bulletpoints. Use markdown formatting (titles, etc...). The presentation has also a conclusion.'''
bot = discord.Bot()

styles = ["default", "gaia", "uncover", "default-dark", "gaia-dark", "uncover-dark", "olive"]
languages = ["english", "french", "spanish", "german", "italian", "portuguese", "russian", "chinese", "japanese", "korean", "arabic"]
darkstyles = ["default-dark", "gaia-dark", "uncover-dark"]
customstyles = ["olive"]
async def get_style(ctx: discord.AutocompleteContext):
    """Returns a list of colors that begin with the characters entered so far."""
    return [style for style in styles if style.startswith(ctx.value.lower())]
async def get_ln(ctx: discord.AutocompleteContext):
    return [language for language in languages if language.startswith(ctx.value.lower())]

@bot.slash_command(name="private_present", description="Generate a presentation with marp, private command for user 707196665668436019")
@option(name="subject", description="The subject of the presentation", required=True)
@option(name="style", description="The style of the presentation", required=False, autocomplete=get_style)
@option(name="center", description="Center the text", required=False)
@option(name="language", description="The language of the presentation", required=False, autocomplete=get_ln)
@option(name="indications", description="The indications for the presentation", required=False)
#command wprks only in dm and only for user 707196665668436019
@commands.is_owner()
async def private_present(ctx: discord.ApplicationContext, subject: str, style: str = "default", center: bool = True, language: str = "english", indications: str = ""):
    await present(ctx, subject, style, language, indications)

@bot.slash_command(name="present", description="Generate a presentation with marp")
#we create a function that takes the subject of the presentation and the style of the presentation as arguments, and that
@option(name="subject", description="The subject of the presentation", required=True)
@option(name="style", description="The style of the presentation", required=False, autocomplete=get_style)
@option(name="center", description="Center the text", required=False)
@option(name="language", description="The language of the presentation", required=False, autocomplete=get_ln)
@option(name="indications", description="The indications for the presentation", required=False)
# a cooldown of duration cooldown seconds, except if the user is 707196665668436019
#@commands.cooldown(1, int(cooldown), commands.BucketType.user)
@commands.cooldown(1, int(cooldown), commands.BucketType.guild)
async def normal_present(ctx: discord.ApplicationContext, subject: str, style: str = "default", center: bool = True, language: str = "english", indications: str = ""):
    await present(ctx, subject, style, language, indications)
async def present(ctx: discord.ApplicationContext, subject: str, style: str = "default", center: bool = True, language: str = "english", indications: str = ""):
    await ctx.defer()
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d-%H-%M-%S")
    #if the style is dark
    dark = False
    if style in darkstyles: 
        style = style.replace("-dark", "")
        dark = True 
    marp = f'''---
marp: true
theme: {styles[styles.index(style)]}
class:
'''
    if dark: marp = marp + f"    - invert\n---"
    if center: marp = marp + "    - lead\n---"
    else: marp = marp + "\n---"
#    if style in customstyles: 
#        marp = f"/* @theme {style} */\n" + marp
#        print(marp)
    prompt = f"{intstructions} {indications} The subject of the presentation is: {subject} The Language is: {language} <|endofprompt|> \n {marp}"    
    subject2 = subject
    forbidden = ["\\", "/", "?", "!", ":", ";", "(", ")", "[", "]", "{", "}", "'", '"', "=", "+", "*", "&", "^", "%", "$", "#", "@", "`", "~", "|", "<", ">", ",", ".", "?", " "]
    for i in forbidden: 
        if i in subject: subject = subject.replace(i, "-")
    #we save teh subject in base64 in a variable
    #if dosen't exist, create a directory called "userid" where the userid is the id of the user who called the command
    uid = str(ctx.author.id)
    if not os.path.exists("./data/"+uid):
        os.mkdir("./data/"+uid)
    datenow = datetime.datetime.now()
    datenow = datenow.strftime("%Y-%m-%d-%H-%M-%S")
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
    if len(subject) > 15: subject = subject[:15]    
    b64 = base64.urlsafe_b64encode(subject.encode("utf-8"))
    os.mkdir(f"./data/{uid}/{b64}{datenow}")
    path = f"./data/{uid}/{b64}{datenow}"
    with open(f"{path}/{subject}-images.txt", "w", encoding="utf8") as f:
        for image in image_filenames:
            f.write(image + "\n")
    with open(f"{path}/{subject}.md", "w", encoding="utf8") as f: f.write(present)
    if len(image_filenames) > 0 and  use_images!="no":
        #now we first remove the extension from the image filenames by removing the last 4 characters
        image_filenames = [image[:-4] for image in image_filenames]
        print(image_filenames)
        for images in image_filenames:
            print ("generating image " + images + "with " + str(use_images))
            r = await imagesGeneration.generate(images, f"{os.getcwd()}\\data\\{uid}\\{b64}{datenow}\\", str(use_images), apikey)
            if str(use_images) == "sd": os.rename(f"{os.getcwd()}\\.\\data\\{uid}\\{b64}{datenow}\\{images}_0.png", f"{os.getcwd()}\\data\\{uid}\\{b64}{datenow}\\{images}.png")
            if str(use_images) == "dalle":
                image_url = r['data'][0]['url']
                img_data = requests.get(image_url).content
                with open(f'{path}/{images}.png', 'wb') as handler:
                    handler.write(img_data)
                await asyncio.sleep(15) #wait 15 seconds to avoid rate limiting
    cmd = f"--pdf --allow-local-files {path}/{subject}.md"
    if style in customstyles: cmd = cmd + f" --theme ./themes/{style}.css"
    if os.path.exists("./marp.exe"):
        os.system(f"marp.exe {cmd}")
    else:
        cmd = cmd.replace("'", "\\'")
        os.system(f"./marp {cmd}")
    cmd = f" --image png -o {path}/{subject}.png --allow-local-files {path}/{subject}.md"
    if style in customstyles: cmd = cmd + f" --theme ./themes/{style}.css"
    if os.path.exists("./marp.exe"):
        os.system(f"marp.exe {cmd}")
    else:
        cmd = cmd.replace("'", "\\'")
        os.system(f"./marp {cmd}")
    cmd = f" --html --allow-local-files {path}/{subject}.md"
    if style in customstyles: cmd = cmd + f" --theme ./themes/{style}.css" 
    if os.path.exists("./marp.exe"):
        os.system(f"marp.exe {cmd}")
    else:
        cmd = cmd.replace("'", "\\'") 
        os.system(f"./marp {cmd}")
    cmd = f" --pptx --allow-local-files {path}/{subject}.md"
    if style in customstyles: cmd = cmd + f" --theme ./themes/{style}.css" 
    if os.path.exists("./marp.exe"):
        os.system(f"marp.exe {cmd}")
    else:
        cmd = cmd.replace("'", "\\'") 
        os.system(f"./marp {cmd}")
    #now, we create a zip file with all the files
    zipObj = ZipFile(f"{path}/{subject}.zip", 'w')
    zipObj.write(f"{path}/{subject}.md", f"{subject}.md")
    zipObj.write(f"{path}/{subject}.html", f"{subject}.html")
    zipObj.write(f"{path}/{subject}.pdf", f"{subject}.pdf")
    zipObj.write(f"{path}/{subject}.png", f"{subject}.png")
    zipObj.write(f"{path}/{subject}.pptx", f"{subject}.pptx")
    with open(f"{path}/{subject}-images.txt", "r", encoding="utf8") as f:
        for image in f.readlines():
            zipObj.write(f"{path}/{image.strip()}", f"{image.strip()}")
    zipObj.close()
    embed = discord.Embed(title=subject2, description="Thanks for using presentator bot. You will find your presentation in the attached zip file in the following formats: markdown, html, pdf, pptx, and the presentation' images. If you want to modify your presentation you can use the markdown file. More information about how to modify the file [HERE](https://marp.app).", color=discord.Color.brand_red())
    files = [discord.File(f"{path}/{subject}.zip"), discord.File(f"{path}/{subject}.png")]
    embed.set_image(url=f"attachment://{subject}.png")
    await ctx.respond(embed=embed, files=files)

@bot.slash_command(name="list", description="List all the presentations you have created")
async def list(ctx: discord.ApplicationContext):
    embed = discord.Embed(title="Presentations", description="Here is the list of all the presentations you have created. You can download the presentation in different formats (pdf, markdown, html) by doing `/get` \"*presentation id*\". The images are generated by an ai. If you want to modify your presentation you can use the markdown file. More information about how to modify the file [HERE](https://marp.app).", color=0x00ff00)
    liste = await get_presentations(str(ctx.author.id))
    for key in liste:
        embed.add_field(name=f"{liste[key]}", value=f"</get:1063051827010084925> `{key}`", inline=False)
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
    liste = await get_presentations(uid)
    if pid in liste:
        files = [discord.File(f"./data/{uid}/{pid}/{liste[pid]}.pdf"), discord.File(f"./data/{uid}/{pid}/{liste[pid]}.md"), discord.File(f"./data/{uid}/{pid}/{liste[pid]}.html")]
        await ctx.respond(files=files, ephemeral=True)

@bot.event
async def on_ready():
    print("Bot is ready")
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