import sdkit
from sdkit.models import load_model
from sdkit.generate import generate_images
from sdkit.utils import save_images, log
from sdkit.filter import apply_filters
import os
from fastapi import FastAPI
#This is an API on the port 9009 that generates images from a prompt
#The prompt is the text that the model will use to generate the image
#The path is the path where the image will be saved
#The model is a model that generates images from text

path=""
prompt=""
app = FastAPI()
context = sdkit.Context()
context.model_paths['stable-diffusion'] = '.\\models\\stable-diffusion\\openjourney-v2-unpruned.ckpt'
load_model(context, 'stable-diffusion')
context.model_paths['gfpgan'] = '.\\models\\gfpgan\\GFPGANv1.3.pth'
load_model(context, 'gfpgan')
print("Model loaded")
@app.get("/generate_image")
async def generate(prompt,path):
    # set the path to the model file on the disk (.ckpt or .safetensors file)
    print(f"Generating image for prompt: {prompt} and path: {path}")
    # generate the image
    image = generate_images(context, prompt=prompt, seed=42, width=512, height=512)
    image_face_fixed = apply_filters(context, 'gfpgan', image)
    # save the image
    save_images(image_face_fixed, dir_path=path, file_name=prompt, output_format='png')

    log.info("Generated images!")