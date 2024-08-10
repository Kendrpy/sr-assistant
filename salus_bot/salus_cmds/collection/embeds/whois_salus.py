import discord
from discord.ui import Button, View
from .constants import EMPTY

def whois_salus_embed(user):
  if user.id == 322725846517547009:
    embed = discord.Embed(color = 0xff0000, title = 'Lord Kayra, my name is... SALUSSY')
  else:
    embed = discord.Embed(color = 0xff0000, title = 'My name is... SALUSSY')
  embed.set_image(url = 'https://cdn.discordapp.com/attachments/985542931773521980/987752831689850930/SPOILER_export202206180059228820.png')
  return embed