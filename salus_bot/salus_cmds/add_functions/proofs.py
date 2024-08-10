import re
import requests as rq
from ..utils import image_links_regex

async def select_proofs(ctx, bot):
  await ctx.send('What is the **proof** for this report?')
  def check(m):
    if (m.author == ctx.author) and (m.channel.id == ctx.message.channel.id):
      if m.content.lower() == 'cancel':
        return True
      urls = [x.group() for x in re.finditer(r'{0}'.format(image_links_regex), m.content, re.S | re.I |  re.M)]
      if urls or m.attachments:
        return True
      return False

  msg = await bot.wait_for('message', check=check)
  if msg.content.lower() == 'cancel':
    return False
  else:
    img_uploads = [x.url for x in msg.attachments if x.content_type.startswith('image')]
    urls = msg.content + ' ' + (' ').join(img_uploads)
    imgs = [x.group() for x in re.finditer(r'{0}'.format(image_links_regex), urls)]
    result = list()
    if imgs:
      for img in imgs:
        if rq.get(img).status_code == 200:
          result.append(img)
      if len(result) > 1:
        return (",").join(result)
      elif len(result) == 1:
        return result[0]
    return None
    