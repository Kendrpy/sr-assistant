import os
# Discord libs
import discord
from discord.ext import commands
from discord.ext.commands import cooldown
import salus_cmds as cmd
from salus_cmds.config import add_role, update_role, remove_role
# Vars
token = os.environ['TOKEN']
bot = commands.Bot(command_prefix = 's-', intents = discord.Intents.all())

@bot.event
async def on_ready():
  print("KSF Bot: Ready")

sensei = [508106724075634709, 165343848669642754, 808403290755825715]
KSF = 829600493398786078
authorized = [829600493398786078]

@bot.command(name='add')
@commands.has_any_role(add_role)
@cooldown(1, 1000, commands.BucketType.user)
async def cmd_add(ctx):
  # if ctx.author.id not in sensei:
  #   return
  if ctx.guild.id != KSF:
    return
  await cmd.add_report(ctx, bot)
  cmd_add.reset_cooldown(ctx)
@cmd_add.error
async def cmd_add_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
      if ctx.author.id == 322725846517547009:
        await ctx.send("You don't have access to this role, my Lord")
      else:
        await ctx.send("You don't have access to this role")

@bot.command(name='update')
@commands.has_any_role(update_role)
@cooldown(1, 1000, commands.BucketType.user)
async def cmd_update(ctx):
  # if ctx.author.id not in sensei:
  #   return
  if ctx.guild.id != KSF:
    return
  await cmd.update_report(ctx, bot)
  cmd_update.reset_cooldown(ctx)
@cmd_update.error
async def cmd_update_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
      if ctx.author.id == 322725846517547009:
        await ctx.send("You don't have access to this role, my Lord")
      else:
        await ctx.send("You don't have access to this role")

@bot.command(name='remove')
@commands.has_any_role(remove_role)
@cooldown(1, 1000, commands.BucketType.user)
async def cmd_remove(ctx):
  # if ctx.author.id not in sensei:
  #   return
  if ctx.guild.id != KSF:
    return
  await cmd.remove_report(ctx, bot)
  cmd_remove.reset_cooldown(ctx)
@cmd_remove.error
async def cmd_remove_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
      if ctx.author.id == 322725846517547009:
        await ctx.send("You don't have access to this role, my Lord")
      else:
        await ctx.send("You don't have access to this role")

@bot.command(name='c')
@commands.has_any_role(remove_role, add_role, update_role)
async def cmd_search(ctx):
  # if ctx.author.id not in sensei:
  #   return
  if ctx.guild.id not in authorized:
    return
  await cmd.search_report(ctx, bot)
  

# @bot.command(name='test')
# async def cmd_alt(ctx):
#   req.sr_reports(ctx.message.content.split(' ')[1])

bot.run(token)
