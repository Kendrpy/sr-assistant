import discord

image_links_regex = '(?:(?:https?)+\:\/\/+[a-zA-Z0-9\/\._-]{1,})+(?:(?:jpe?g|png|webp))'
links_regex = '((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'
emojis_regex = '<:\w*:\d*>'
async def search_id(bot, arg):
  if arg == 'Unknown':
    return 'Unknown'
  try:
    return await bot.fetch_user(arg)
  except discord.NotFound:
    return False

async def check_id(bot, arg):
  try:
    await bot.fetch_user(arg)
    return True
  except discord.NotFound:
    return False