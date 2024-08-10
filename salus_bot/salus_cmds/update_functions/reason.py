import re
import discord
import asyncio
from discord.ui import View
from ..utils import image_links_regex
from .type import rq_type
from .. import db_requests as rq

bot_message = 'What is the **reason** for reporting this?'
cancel = 'cancel'

async def select_reason(ctx, bot, subject):
  class AskView(View):
      def __init__(self):
          super().__init__(timeout=None)
          self.value = None
      @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
      async def yes_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Updating reason', view = self)
          self.value = 1
          self.stop()

      @discord.ui.button(label='No', style=discord.ButtonStyle.red)
      async def no_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Not updating reason', view = self)
          self.value = 0
          self.stop()

  view = AskView()
  msg = await ctx.send('Do you want to update the reason?', view = view)
  def check(m):
    return (m.author == ctx.author) and (m.content.lower() == 'cancel')
  tasks = [asyncio.create_task(view.wait()),
                 asyncio.create_task(bot.wait_for('message', check=check))]
  done_tasks, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
  if tasks[1] in done_tasks:
    return False 
  elif int(view.value) == False:
    return None
  while True:
    await ctx.send(bot_message)
    def check(m):
      return (m.author == ctx.author) and (m.channel.id == ctx.message.channel.id)
    msg = await bot.wait_for('message', check=check)
    urls = [x.group() for x in re.finditer(r'{0}'.format(image_links_regex), msg.content, re.S | re.I |  re.M)]
    if msg.content.lower() == cancel:
      return False
    elif msg.content.lower() == 'n':
      reason = None
      break
    elif urls or msg.attachments:
      await ctx.send('Images aren\'t allowed in reasons, keep that for later.')
      continue
    elif len(msg.content) > 1023:
      await ctx.send('Message is too long. Max lenght should be 1024 characters.')
      continue
    else:
      type = await rq_type(ctx, bot)
      if type == cancel:
        return False
      elif not type:
        result = rq.get_reason(subject)
        result = f'{result}\n{msg.content}'
        if len(result) > 1023:
          await ctx.send('Message is too long. Max lenght should be 1024 characters.')
          continue
        rq.update_reason(result, subject)
        return True
      else:
        rq.update_reason(msg.content, subject)
      return True

