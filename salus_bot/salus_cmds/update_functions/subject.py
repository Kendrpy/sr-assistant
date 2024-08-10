from ..utils import search_id, check_id
from .. import db_requests as rq

bot_message =  '<:IB_whitebutterfly:986499134666194954> Okay, let\'s start this Update !\nWho are you **updating**?'
bot_message_kyo =  '<:IB_whitebutterfly:986499134666194954> Okay, let\'s start this Update, Daddy ! :heart:\nWho are you **updating**?'
cancel = 'cancel'

async def select_subject(ctx, bot):
  while True:
    if ctx.author.id == 850782021658607676:
      await ctx.send(bot_message_kyo)
    else:
      await ctx.send(bot_message)
    def check(m):
      return (m.channel.id == ctx.message.channel.id) and (m.author == ctx.author) and (not m.reference) and (m.mentions or m.content.isdigit() or m.content.lower() == cancel)
    msg = await bot.wait_for('message', check=check)
    if msg.content.lower() == cancel:
      return False
    elif msg.mentions:
      user = msg.mentions[0]
    elif msg.content.isdigit():
      if await check_id(bot, int(msg.content)):
        user = await search_id(bot, int(msg.content))
      else:
        if ctx.author.id == 850782021658607676:
          await ctx.send('DADDY NO ! That\'s not a valid ID !')
        else:
          await ctx.send('Not a valid ID')
        continue
    data = dict()
    if user == bot.user:
      await ctx.send(f'Only Sensei can update me :smiling_face_with_3_hearts:')
    if rq.search(user.id):
      return user.id
    else:
      if ctx.author.id == 850782021658607676:
        await ctx.send(f'User `{user.id}` is not reported, Daddy :heart:')
      else:
        await ctx.send(f'User `{user.id}` is not reported.')
    continue