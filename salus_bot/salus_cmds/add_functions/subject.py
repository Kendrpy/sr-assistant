from ..utils import search_id, check_id
from .. import db_requests as rq
from ..collection import embeds as emb

bot_message =  '<:IB_whitebutterfly:986499134666194954> Okay, let\'s start this report !\nWho are you **reporting**?'
bot_message_kyo =  '<:IB_whitebutterfly:986499134666194954> Okay let\'s start this report, Daddy ! :heart:\nWho are you **reporting**?'
cancel = 'cancel'

async def select_subject(ctx, bot):
  while True:
    if ctx.author.id == 850782021658607676:
      await ctx.send(bot_message_kyo)
    else:
      await ctx.send(bot_message)
    def check(m):
      return (m.author == ctx.author) and (m.channel.id == ctx.message.channel.id) and (not m.reference) and (m.mentions or m.content.isdigit() or m.content.lower() == cancel)
    msg = await bot.wait_for('message', check=check)
    if msg.content.lower() == cancel:
      return False
    elif msg.mentions:
      user = msg.mentions[0]
    elif msg.content.isdigit():
      if await check_id(bot, int(msg.content)):
        user = await search_id(bot, int(msg.content))
      else:
        user = False
    else:
      pass
    if user:
      data = dict()
      if user == bot.user:
        if ctx.author.id == 850782021658607676:
          await ctx.send("Daddy... what are you doing?\nDADDY STAHP ! :sob:")
        else:
          await ctx.send('https://media.discordapp.net/attachments/980723866441768980/989333029921099857/unknown.png')
        continue
      data = rq.search(user.id)
      if data:
        tag = rq.search_tag(data['tag_id'])
        data['tag_name'] = tag['tag_name']
        data['tag_color'] = tag['tag_color']
        users = {
          'subject' : await search_id(bot, data['subject_id']),
          'sr_user' : await search_id(bot, data['sr_id']),
          'reporter' : await search_id(bot, data['reporter_id'])
        }
        await ctx.send(f'User `{user.id}` is already reported')
        await emb.result_embed(data, users, ctx.message)
        return False
      else:
        return user.id
    else:
      if ctx.author.id == 850782021658607676:
        await ctx.send('DADDY NO ! That\'s not a valid ID')
      else:
        await ctx.send('Not a valid ID')
      continue