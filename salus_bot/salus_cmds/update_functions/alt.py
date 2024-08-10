import discord
import asyncio
from discord.ui import View
from ..utils import search_id, check_id
from .type import rq_type
from .. import db_requests as req

async def select_alts(ctx, bot, subject):
  class AltView(View):
      def __init__(self):
          super().__init__(timeout=None)
          self.value = None
      @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
      async def yes_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Reporting alts', view = self)
          self.value = 1
          self.stop()

      @discord.ui.button(label='No', style=discord.ButtonStyle.red)
      async def no_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Not reporting alts', view = self)
          self.value = 0
          self.stop()

  class ClearView(View):
      def __init__(self):
          super().__init__(timeout=None)
          self.value = None
      @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
      async def yes2_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Clearing alts', view = self)
          self.value = 1
          self.stop()

      @discord.ui.button(label='No', style=discord.ButtonStyle.red)
      async def no2_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Not clearing alts', view = self)
          self.value = 0
          self.stop()

  view = AltView()
  clearview = ClearView()
  msg = await ctx.send('Do you want to report **alts**?', view = view)
  def check(m):
    return (m.channel.id == ctx.message.channel.id) and (m.author == ctx.author) and (m.content.lower() == 'cancel')
  tasks = [asyncio.create_task(view.wait()),
                 asyncio.create_task(bot.wait_for('message', check=check))]
  done_tasks, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
  if tasks[1] in done_tasks:
    return False # cancelled
  else:
    answer = int(view.value) # answered
    if not answer: # not wanting to update alts
      if req.get_alts(subject):
        msg = await ctx.send('Do you want to **clear alts**?', view = clearview)
        def check(m):
          return (m.author == ctx.author) and (m.channel.id == ctx.message.channel.id) and (m.content.lower() == 'cancel')
        tasks = done_tasks = None
        tasks = [asyncio.create_task(clearview.wait()),
                      asyncio.create_task(bot.wait_for('message', check=check))]
        done_tasks, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        if tasks[1] in done_tasks:
          return False # Cancel
        else:
          if clearview.value:
            request = req.clear_alts(str(subject)) # done by clearing alts
            return True
          else:
            return None
      return None
    else:
      while True: # wanting to add alts
        await ctx.send('Who are the alts you want to report?')
        def check(m):
          return (m.channel.id == ctx.message.channel.id) and (m.author == ctx.author) and (not m.reference)
          # return (m.author == ctx.author) and (not m.reference) and (m.mentions or m.content.isdigit() or m.content.lower() == 'cancel')
        msg = await bot.wait_for('message', check=check)
        users = list()
        invalid = list()
        ids = msg.content.split(' ')
        if msg.content.lower() == 'cancel':
          return False
        if msg.mentions:
          if ctx.author in msg.mentions:
            await ctx.send('You cannot add yourself !')
            continue
          else:
            for user in msg.mentions:
              if user != ctx.author:
                users.append(str(user.id))
                ids.remove(f'<@{user.id}>')
        for id in ids:
          if id.isdigit() and int(id) != int(ctx.author.id) and int(id) < 9223372036854775807:
            if await check_id(bot, id):
              if ctx.author.id == int(id):
                await ctx.send('You cannot add yourself !')
                continue
              else:
                users.append(str(id))
            else:
              invalid.append(id)
        if invalid:
          invalid = ' '.join(invalid)
          await ctx.send(f'Invalid IDs:\n```\n{invalid}\n```')
        if users:
          strprint = ' '.join(users)
          await ctx.send(f'Added alts IDs:\n```\n{strprint}\n```')
          result = req.get_alts(str(subject))
          if result:
            result = result.split(',') 
            type = await rq_type(ctx, bot)
            if type:
              req.update_alts(','.join(result), int(subject))
              return True
            else:
              result += users
              req.update_alts(','.join(result), int(subject))
          else:
            req.update_alts(','.join(users), int(subject))
          return True
        else:
          if invalid:
            await ctx.send('Please fill out valid IDs')
          else:
            await ctx.send('Please fill out IDs')
          continue