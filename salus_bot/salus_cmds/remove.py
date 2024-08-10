import discord
import asyncio

# Import Requests and Embeds
from .collection import embeds as emb
from . import db_requests as req
from .utils import search_id, check_id
from .config import shout_channel, update_ping

async def remove_report(ctx, bot):
  msg = ctx.message.content.split(' ')[1:]
  if not msg:
    if ctx.author.id == 850782021658607676:
      await ctx.send('Aww Daddy ! Wrong command ! Type `s-c <discord_user_id>` or `s-c @mention_user` to search someone')
    else:
      await ctx.send('Wrong command, type `s-c <discord_user_id>` or `s-c @mention_user` to search someone')
    return True
  if ctx.message.mentions:
    user = ctx.message.mentions[0].id
  elif msg[0].isnumeric():
    user = int(msg[0])
  else:
    if ctx.author.id == 850782021658607676:
      await ctx.send('Aww Daddy ! Wrong command ! Type `s-c <discord_user_id>` or `s-c @mention_user` to search someone')
    else:
      await ctx.send('Wrong command, type `s-c <discord_user_id>` or `s-c @mention_user` to search someone')
    return True
  if await check_id(bot, user):
    req_user = await search_id(bot, user)
    user_data = req.search(user)
    if not user_data:
      user_data = req.old_search(user)
    if user_data:
      data = dict() 
      data['sr'] = ctx.author
      data['user'] = req_user
      data['subject_id'] = user
      if ctx.author.id == 850782021658607676:
        await ctx.send('What\'s the reason for removing this report, Daddy?')
      else:
        await ctx.send('What\'s the reason for removing this report?')
      def check(m):
        return (m.author == ctx.author) and (m.channel.id == ctx.message.channel.id)
      data['reason'] = (await bot.wait_for('message', check=check)).content
      if data['reason'].lower() == 'cancel':
        await ctx.send('Remove canceled')
        return True
      data['timestamp'] = str(ctx.message.created_at.timestamp()).split('.')[0]
      delete = req.delete(data)
      if not delete:
        ctx.send('There has been an error deleting this report')
        return False
      channel = bot.get_channel(int(shout_channel))
      await ctx.send(embed = emb.delete_embed(data))
      msg = await channel.send(f'<@&{update_ping}>', embed = emb.delete_embed(data))
      await msg.publish()
      return True
    else:
      await ctx.send(embed = emb.not_reported(ctx, req_user))
      return True
  else:
    await ctx.send('Invalid user ID')
    return