import asyncio
import discord
from discord.ui import Button, View
from discord.utils import get

# Import Requests and Embeds
from .collection import embeds as emb
from . import db_requests as rq
from .utils import search_id, check_id

roles = {
  921064407096754218 : 'Owner',
  882838495419314237 : 'Head admin',
  985939443162685500 : 'Admin',
  876907626145910814 : 'Head scammer reporter',
  832191446933176380 : 'Scammer reporter',
  941841807526989824 : 'Trial scam reporter'
  }

# roles = {
#   989410601254141952 : 'Ownerussy'
# }

async def search_report(ctx, bot):
  try:
    id = ctx.message.content.split(' ')[1]
  except IndexError:
    if ctx.author.id == 850782021658607676:
      await ctx.send('Daddy type `s-c <discord_user_id>` or `s-c @mention_user` to search someone')
    else:
      await ctx.send('Search command: Type `s-c <discord_user_id>` or `s-c @mention_user` to search someone')
    return
  if not id or ctx.message.attachments:
    if ctx.author.id == 850782021658607676:
      await ctx.send('Daddy type `s-c <discord_user_id>` or `s-c @mention_user` to search someone')
    else:
      await ctx.send('Search command: Type `s-c <discord_user_id>` or `s-c @mention_user` to search someone')
  elif ctx.message.mentions or id.isnumeric():
    if ctx.message.mentions:
      user = ctx.message.mentions[0].id
    else:
      if await check_id(bot, id):
        user = id
      else:
        await ctx.send('Invalid user ID')
        return
    if ctx.guild.get_member(int(user)) is not None:
      staff = ctx.guild.get_member(int(user))
      if staff:
        for role, role_name in roles.items():
          if get(ctx.guild.roles, id=role) in staff.roles:
            await ctx.send(embed = emb.staff_embed(staff, role_name))
            return
    if int(user) == bot.user.id:
      await ctx.send(embed = emb.whois_salus_embed(ctx.author))
      return
    data = rq.search(user)
    if data:
      tag = rq.search_tag(data['tag_id'])
      data['tag_name'] = tag['tag_name']
      data['tag_color'] = tag['tag_color']
      users = {
        'subject' : await search_id(bot, data['subject_id']),
        'sr_user' : await search_id(bot, data['sr_id']),
        'reporter' : await search_id(bot, data['reporter_id'])
      }
      await emb.result_embed(data, users, ctx.message)
    elif rq.old_search(user):
      await ctx.send(embed = emb.old_report(ctx, await search_id(bot, user)))
    else:
      await ctx.send(embed = emb.not_reported(ctx, await search_id(bot, user)))
  else:
    if ctx.author.id == 850782021658607676:
      await ctx.send('Wrong command Daddy, type `s-c <discord_user_id>` or `s-c @mention_user` to search someone')
    else:
      await ctx.send('Wrong command, type `s-c <discord_user_id>` or `s-c @mention_user` to search someone')
