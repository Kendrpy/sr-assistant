import discord
import asyncio
from discord.ui import View

async def select_anonymous(ctx, bot):
  class AnonymousView(View):
      def __init__(self):
          super().__init__(timeout=None)
          self.value = None
      @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
      async def yes_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Report **will be** Anonymous', view = self)
          self.value = 1
          self.stop()

      @discord.ui.button(label='No', style=discord.ButtonStyle.red)
      async def no_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Report will **not** be Anonymous', view = self)
          self.value = 0
          self.stop()

  view = AnonymousView()
  msg = await ctx.send('Do you want this report to be **Anonymous**?', view = view)
  def check(m):
    return (m.author == ctx.author) and (m.content.lower() == 'cancel') and (m.channel.id == ctx.message.channel.id)
  tasks = [asyncio.create_task(view.wait()),
                 asyncio.create_task(bot.wait_for('message', check=check))]
  done_tasks, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
  if tasks[1] in done_tasks:
    return False
  else:
    return str(view.value)