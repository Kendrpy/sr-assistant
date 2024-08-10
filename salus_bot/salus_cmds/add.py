import discord
from discord.ui import Button, View
from .add_functions import *
from .utils import search_id, check_id
from . import db_requests as req
from .collection import embeds as emb
from .config import shout_channel, add_ping


async def add_report(ctx, bot):
  tasks = [
    select_subject,
    select_reporter,
    select_anonymous,
    select_game,
    select_tag,
    add_alt,
    select_reason,
    select_proofs
  ]
  selector = [
      'subject_id',
      'reporter_id',
      'anonymous',
      'game',
      'tag_id',
      'alts',
      'reason',
      'proofs',
  ]
  data = dict()
  for index, task in enumerate(tasks):
    result = await task(ctx, bot)
    if result == False:
      if ctx.author.id == 850782021658607676:
        await ctx.send('I cancelled the report, Daddy')
      else:
        await ctx.send('Report has been cancelled')
      data = dict()
      return False
    elif result == None:
      data[selector[index]] = ''
    else:
      data[selector[index]] = result
  
  if data:
    tag = req.search_tag(data['tag_id'])
    data['tag_name'] = tag['tag_name']
    data['tag_color'] = tag['tag_color']
    data['sr_id'] = ctx.message.author.id
    data['timestamp'] = str(ctx.message.created_at.timestamp()).split('.')[0]
    users = {
      'subject' : await search_id(bot, data['subject_id']),
      'sr_user' : await search_id(bot, data['sr_id']),
      'reporter' : await search_id(bot, data['reporter_id'])
    }
    msg = await emb.result_embed(data, users, ctx.message, shout='Added', channel=shout_channel, shout_ping=add_ping, bot=bot)
    # msg = await emb.result_embed(data, users, ctx.message)
    req.add(data)
    if req.old_search(data['subject_id']):
      req.old_remove(data['subject_id'])
    return True