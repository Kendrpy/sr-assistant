import discord
import asyncio
from discord.ui import View
from ..utils import search_id, check_id

async def add_alt(ctx, bot):
  class AltView(View):
      def __init__(self):
          super().__init__(timeout=None)
          self.value = None
      @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
      async def yes_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Reporting an alt', view = self)
          self.value = 1
          self.stop()

      @discord.ui.button(label='No', style=discord.ButtonStyle.red)
      async def no_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Not reporting an alt', view = self)
          self.value = 0
          self.stop()

  view = AltView()
  msg = await ctx.send('Do you want to report an **alt**?', view = view)
  def check(m):
    return (m.author == ctx.author) and (m.channel.id == ctx.message.channel.id) and (m.content.lower() == 'cancel')
  tasks = [asyncio.create_task(view.wait()),
                 asyncio.create_task(bot.wait_for('message', check=check))]
  done_tasks, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
  if tasks[1] in done_tasks:
    return False
  else:
    answer = int(view.value)
  if not answer:
    return None
  else:
    while True:
      await ctx.send('Who are the alts you want to report?')
      def check(m):
        return (m.author == ctx.author) and (not m.reference) and (m.channel.id == ctx.message.channel.id)
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
        if id.isdigit() and int(id) != bot.user.id and int(id) != int(ctx.author.id) and int(id) < 9223372036854775807:
          if await check_id(bot, id):
            users.append(str(id))
          else:
            invalid.append(id)
      if invalid:
        invalid = ' '.join(list(dict.fromkeys(invalid)))
        await ctx.send(f'Invalid IDs:\n```\n{invalid}\n```')
      if not users:
        ctx.send('Please enter new ones')
        continue
      users = list(dict.fromkeys(users))
      strprint = ' '.join(users)
      await ctx.send(f'Added alts IDs:\n```\n{strprint}\n```')
      return ','.join(users)