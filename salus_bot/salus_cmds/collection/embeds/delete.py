import discord
from .constants import EMPTY

def delete_embed(arg):
  embed = discord.Embed(color = 0x00ff00, title = f"User removed - {arg['user']}")
  if not arg['reason']:
    arg['reason'] = EMPTY
  embed.add_field(name = 'User ID', value = f"`{arg['subject_id']}`", inline = False)
  embed.add_field(name = 'Reason', value = f"{arg['reason']}", inline = False)
  embed.add_field(name = 'Removed by', value = f"<@{arg['sr'].id}>", inline = False)
  embed.add_field(name = 'Removed on', value = f"<t:{arg['timestamp']}:D>\n<t:{arg['timestamp']}:R>", inline = False)
  return embed