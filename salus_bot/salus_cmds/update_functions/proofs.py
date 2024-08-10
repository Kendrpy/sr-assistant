import re
import asyncio
import discord
import requests as rq
from discord.ui import View
from ..utils import image_links_regex
from .type import rq_type
from .. import db_requests as req

async def select_proofs(ctx, bot, subject):
  class AskView(View):
      def __init__(self):
          super().__init__(timeout=None)
          self.value = None
      @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
      async def yes_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Updating proofs', view = self)
          self.value = 1
          self.stop()

      @discord.ui.button(label='No', style=discord.ButtonStyle.red)
      async def no_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Not updating proofs', view = self)
          self.value = 0
          self.stop()

  view = AskView()
  msg = await ctx.send('Do you want to update proofs?', view = view)
  def check(m):
    return (m.channel.id == ctx.message.channel.id) and (m.author == ctx.author) and (m.content.lower() == 'cancel')
  tasks = [asyncio.create_task(view.wait()),
                 asyncio.create_task(bot.wait_for('message', check=check))]
  done_tasks, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
  if tasks[1] in done_tasks:
    return False 
  elif not int(view.value):
    return None
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
  while True:
    if msg.content.lower() == 'cancel':
      return False
    else:
      img_uploads = [x.url for x in msg.attachments if x.content_type.startswith('image')]
      urls = msg.content
      imgs = [x.group() for x in re.finditer(r'{0}'.format(image_links_regex), urls)]
      result = list()
      if imgs:
        for img in imgs:
          if rq.get(img).status_code == 200:
            result.append(img)
      result += img_uploads
      if result:
        break
      else:
        ctx.send('Please enter valid Images links or uploads')
        continue
      
  type = await rq_type(ctx, bot)
  if not type:
    imgs = req.get_proofs(subject).split(',')
    for img in result:
      imgs.append(img)
    req.update_proofs(','.join(imgs), subject)
    return True
  else:
    req.update_proofs(','.join(result), subject)
    return True
    