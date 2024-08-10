import discord
import asyncio
from discord.ui import View
from .. import db_requests as rq

async def select_tag(ctx, bot):
  
  class TagView(View):
      def __init__(self):
          super().__init__(timeout=None)
          self.value = None
          
      @discord.ui.button(label='Scammer', style=discord.ButtonStyle.red)
      async def scammer_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Tag selected: Scammer', view = self)
          self.value = '0'
          self.stop()

      @discord.ui.button(label='Impersonator', style=discord.ButtonStyle.red)
      async def impersonator_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Tag selected: Impersonator', view = self)
          self.value = '1'
          self.stop()

      @discord.ui.button(label='Fake MM', style=discord.ButtonStyle.red)
      async def fakemm_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Tag selected: Fake MM', view = self)
          self.value = '2'
          self.stop()

      @discord.ui.button(label='Scam Server Owner', style=discord.ButtonStyle.red)
      async def scamown_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Tag selected: Scam Server Owner', view = self)
          self.value = '5'
          self.stop()

      @discord.ui.button(label='TWC', style=discord.ButtonStyle.gray)
      async def twc_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Tag selected: TWC', view = self)
          self.value = '3'
          self.stop()

      @discord.ui.button(label='Unprofessional MM', style=discord.ButtonStyle.gray)
      async def unprof_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Tag selected: Unprofessional MM', view = self)
          self.value = '4'
          self.stop()

  view = TagView()
  msg = await ctx.send('What\'s the **tag** of this report?', view = view)
  def check(m):
    return (m.channel.id == ctx.message.channel.id) and (m.author == ctx.author) and (m.content.lower() == 'cancel')
  tasks = [asyncio.create_task(view.wait()),
                 asyncio.create_task(bot.wait_for('message', check=check))]
  done_tasks, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
  if tasks[1] in done_tasks:
    return False
  else:
    return str(view.value)