import os
from typing import List
import discord
from datetime import datetime
import hashlib
from discord.activity import Activity
from discord.embeds import Embed
from discord.message import Attachment, Message
from dotenv import load_dotenv
from discord.ext.commands import Bot, Context
from settings_manager import SettingsManager
load_dotenv() 

bot = Bot(command_prefix="ks!")
TOKEN = os.getenv("TOKEN")
sm = SettingsManager()

@bot.event
async def on_ready():
    await bot.change_presence(activity=Activity(name="you | ks!help"))

@bot.command()
async def add(ctx: Context, name: str):
    msg: Message = ctx.message
    attachments: List[Attachment] = msg.attachments
    for a in attachments:
        print(a.filename, a.url)
        id_ = hashlib.sha256((name+repr(datetime.now())).encode()).digest().hex()
        em = Embed(title="Added!", description=f"name: {name}, id(generated): {id_}", url=a.url)
        await ctx.send(embed=em)
        with sm as s: 
            s.add(name, id_, a.url)

@bot.command()
async def get(ctx: Context, id_: str):
    with sm as s: 
        url = s.get_location(id_)
        em = Embed(title="Here is your map!", description="map id: "+id_, url=url)
        await ctx.send(embed=em)

bot.run(TOKEN)
