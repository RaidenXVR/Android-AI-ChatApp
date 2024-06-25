from typing import Optional

from asynckivy import sleep
from PIL import Image
from io import BytesIO


async def get_response(chat_str: str, mode:str):
    await sleep(1)
    img = Image.open("./assets/ranni.jpg")
    bio = BytesIO()
    img.save(bio, format=img.format)
    img_byte = bio.getvalue()

    return {"message": "echo " + chat_str, "type": "image", "image": img_byte, "content_type": 'nsfw'}
