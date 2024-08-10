import discord
import asyncio
from discord.ui import View

async def select_game(ctx, bot):
  class GameView(View):
      def __init__(self):
          super().__init__(timeout=None)
          self.value = None
          
      @discord.ui.button(label='Genshin', style=discord.ButtonStyle.blurple)
      async def genshin_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Game selected: Genshin', view = self)
          self.value = 'Genshin'
          self.stop()

      @discord.ui.button(label='Roblox', style=discord.ButtonStyle.blurple)
      async def roblox_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Game selected: Roblox', view = self)
          self.value = 'Roblox'
          self.stop()

      @discord.ui.button(label='Honkai', style=discord.ButtonStyle.blurple)
      async def honkai_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Game selected: Honkai', view = self)
          self.value = 'Honkai'
          self.stop()

      @discord.ui.button(label='IDV', style=discord.ButtonStyle.blurple)
      async def idv_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Game selected: IDV', view = self)
          self.value = 'IDV'
          self.stop()

      @discord.ui.button(label='Other', style=discord.ButtonStyle.blurple)
      async def other_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Game selected: Other', view = self)
          self.value = 'Other'
          self.stop()

  view = GameView()
  msg = await ctx.send('What **game** is it?', view = view)
  def check(m):
    return (m.author == ctx.author) and (m.content.lower() == 'cancel') and (m.channel.id == ctx.message.channel.id)
  tasks = [asyncio.create_task(view.wait()),
                 asyncio.create_task(bot.wait_for('message', check=check))]
  done_tasks, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
  if tasks[1] in done_tasks:
    return False
  else:
    return str(view.value)