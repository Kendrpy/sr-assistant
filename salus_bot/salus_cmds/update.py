from discord.ui import Button, View
from .update_functions import *
from .utils import search_id, check_id
from . import db_requests as rq
from .collection import embeds as emb
from .search import search_report
from .config import shout_channel, update_ping


async def update_report(ctx, bot):

  data = dict()
  data['subject_id'] = await select_subject(ctx, bot)
  if data['subject_id'] == False:
    if ctx.author.id == 850782021658607676:
      await ctx.send('Report has been cancelled, Daddy !')
    else:
      await ctx.send('Report has been cancelled')
    data = dict()
    return False

  updates = 0
  subject = data['subject_id']
  tasks = [
    select_tag,
    select_alts,
    select_reason,
    select_proofs
  ]
  data = rq.search(subject)
  tag = rq.search_tag(data['tag_id'])
  data['tag_name'] = tag['tag_name']
  data['tag_color'] = tag['tag_color']
  users = {
    'subject' : await search_id(bot, data['subject_id']),
    'sr_user' : await search_id(bot, data['sr_id']),
    'reporter' : await search_id(bot, data['reporter_id'])
  }
  await ctx.send(f'Updating `{subject}`')
  await emb.result_embed(data, users, ctx.message)
  for task in tasks:
    result = await task(ctx, bot, subject)
    if result == False:
      if ctx.author.id == 850782021658607676:
        await ctx.send('Report has been cancelled, Daddy !')
      else:
        await ctx.send('Report has been cancelled')
      data = dict()
      return
    elif result == None:
      continue
    else:
      updates += 1
  if not updates:
    if ctx.author.id == 850782021658607676:
      await ctx.send('No updates have been made, Daddy !')
    else:
      await ctx.send('No updates have been made')
  data = rq.search(subject)
  tag = rq.search_tag(data['tag_id'])
  data['tag_name'] = tag['tag_name']
  data['tag_color'] = tag['tag_color']
  msg = await emb.result_embed(data, users, ctx.message, shout='Update', channel=shout_channel, shout_ping=update_ping, bot=bot)
  # await emb.result_embed(data, users, ctx.message)