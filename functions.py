from asynckivy import sleep


async def get_response(chat_str:str):
    await sleep(3)
    return "echo "+ chat_str
