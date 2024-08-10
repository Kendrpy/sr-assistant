import discord
import asyncio
from discord.ui import View
from numpy import intc

async def rq_type(ctx, bot):
  class rq_typeView(View):
      def __init__(self):
          super().__init__(timeout=None)
          self.value = None
      @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
      async def yes_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Data will be **replaced**', view = self)
          self.value = 1
          self.stop()

      @discord.ui.button(label='No', style=discord.ButtonStyle.red)
      async def no_callback(self, interaction, button):
        if interaction.user == ctx.author:
          self.clear_items()
          await interaction.response.edit_message(content='Data will be **added**', view = self)
          self.value = 0
          self.stop()

  view = rq_typeView()
  msg = await ctx.send(f'Override the existing data?', view = view)
  def check(m):
    return (m.channel.id == ctx.message.channel.id) and (m.author == ctx.author) and (m.content.lower() == 'cancel')
  tasks = [asyncio.create_task(view.wait()),
                 asyncio.create_task(bot.wait_for('message', check=check))]
  done_tasks, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
  if tasks[1] in done_tasks:
    return 'cancel'
  else:
    return int(view.value)