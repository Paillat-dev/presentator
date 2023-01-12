import requests
import os
async def generate(prompt,path):
    r = requests.get(f"http://localhost:8000/generate_image?prompt={prompt}&path={path}")
    return r.json()
#print the current working directory
print(os.getcwd())