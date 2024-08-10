import re
from ..utils import image_links_regex

bot_message = 'What is the **reason** for reporting this?'
cancel = 'cancel'

async def select_reason(ctx, bot):
  while True:
    await ctx.send(bot_message)
    def check(m):
      return (m.author == ctx.author) and (m.channel.id == ctx.message.channel.id)
    msg = await bot.wait_for('message', check=check)
    urls = [x.group() for x in re.finditer(r'{0}'.format(image_links_regex), msg.content, re.S | re.I |  re.M)]
    if msg.content.lower() == cancel:
      return False
    elif msg.content.lower() == 'n':
      return None
    elif urls or msg.attachments:
      await ctx.send('Images aren\'t allowed in reasons, keep that for later.')
      continue
    elif len(msg.content) > 1023:
      await ctx.send('Message is too long. Max lenght should be 1024 characters.')
      continue
    else:
      return msg.content

