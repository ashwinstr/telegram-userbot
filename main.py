from threading import Thread
from pyrogram import Client, idle
from pyrogram import filters
from modules import *
import modules
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

# pyrogram client
session_string = os.environ["SESSION_STRING"]
app = Client(
    session_string,
    api_id=os.environ["API_ID"],
    api_hash=os.environ["API_HASH"]
)

def main():
    #start the client first
    app.start()

    # this function map is the workaround/fix for eval is evil, but still uses eval to be made, pretty ironic :P
    # map/dict of all functions/modules available in ./modules folder
    function_map = {}
    for i in modules.loadable_mods:
        function_map[f".{str(i)}"] = eval(f"{i}.{i}")

    # message filter to check if the message is from user and has `text` at the start
    def dynamic_data_filter(data):
        async def func(flt, _, message):
            if message.text is not None and message.from_user is not None:
                return message.from_user.is_self and message.text.startswith(flt.data)
        return filters.create(func, data=data)

    # on message listener and function execute ONLY if its in function_map
    @app.on_message(dynamic_data_filter("."))
    async def my_function(client, message):
        method = message.text.split(" ",1)[0]
        if method in function_map.keys():
            Thread(target=function_map[method],args=(client,message)).start()

    # start all the runnable threads
    for i in modules.runnable_scripts:
        Thread(target=eval(f"{i}.runnable"),args=(app,)).start()

    # keep running
    idle()

if __name__ == "__main__":
    main()