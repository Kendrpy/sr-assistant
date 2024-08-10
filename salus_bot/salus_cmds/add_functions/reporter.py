from ..utils import search_id, check_id

bot_message = 'Who **reported** this?'
cancel = 'cancel'

async def select_reporter(ctx, bot):
  while True:
    await ctx.send(bot_message)
    def check(m):
      return (m.channel.id == ctx.message.channel.id) and (m.author == ctx.author) and (not m.reference) and (m.mentions or m.content.isdigit() or m.content.lower() == cancel)
    msg = await bot.wait_for('message', check=check)
    if msg.content.lower() == cancel:
      return False
    elif msg.mentions:
      user = msg.mentions[0]
      return str(user.id)
    elif msg.content.isdigit():
      if await check_id(bot, int(msg.content)):
        result = await search_id(bot, int(msg.content))
        return result.id
      else:
        await ctx.send('Not a valid ID')
    continue


