import os
from os import name
from typing import List, Tuple
import discord
from datetime import datetime
from fuzzywuzzy.fuzz import ratio
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
LINES_PER_PAGE = 10

def sort(arr: List[Tuple[str, str]], query: str) -> List[Tuple[str, str]]:
    arr.sort(key=lambda x: ratio(x[1], query))
    return arr

@bot.event
async def on_ready():
    await bot.change_presence(activity=Activity(name="you | ks!help"))

@bot.command()
async def add(ctx: Context, name: str):
    msg: Message = ctx.message
    attachments: List[Attachment] = msg.attachments
    for i, a in enumerate(attachments):
        print(a.filename, a.url)
        id_ = hashlib.sha256((name+str(i)+repr(datetime.now())).encode()).digest().hex()
        em = Embed(title="Added!", description=f"name: {name}, id(generated): {id_}", url=a.url)
        await ctx.send(embed=em)
        with sm as s: 
            s.add(name, id_, a.url)

@bot.command()
async def search(ctx: Context, query: str, page=1):
    em = Embed(title="Search", description=f"Searching for query `{query}`..... page ***{page}***")
    with sm as s: 
        names = sort(s.get_names(), query)[(page-1)*LINES_PER_PAGE: page*LINES_PER_PAGE]
        if len(names):
            for id_, name in names:
                em.add_field(name=name, value=id_)
        else:
            em.add_field(name="Not found", value="no such map was found")
    await ctx.send(embed=em)

@bot.command()
async def update(ctx: Context, id_: str):
    msg: Message = ctx.message
    attachment: Attachment = msg.attachments[0]
    with sm as s:
        s.set_location(id_, attachment.url)

@bot.command()
async def get(ctx: Context, id_: str):
    with sm as s: 
        url = s.get_location(id_)
        if url is None:
            url = ""
            id_ = "***Error No Such Map ***"
        em = Embed(title="Here is your map![click for link]", description="map id: "+id_, url=url)
        em.set_image(url=url)
        await ctx.send(embed=em)

bot.run(TOKEN)
