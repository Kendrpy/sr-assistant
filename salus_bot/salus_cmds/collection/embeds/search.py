import discord

def not_reported(ctx, user):
  green = 'https://upload.wikimedia.org/wikipedia/commons/2/2d/Basic_green_dot.png'
  yellow = 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Location_dot_orange.svg/1024px-Location_dot_orange.svg.png'
  creation = int(str(user.created_at.timestamp()).split('.')[0])
  msg = int(str(ctx.message.created_at.timestamp()).split('.')[0])
  not_rep = 'User is not reported !'
  age = '(!) Account age is less than 14 days'
  color = 0xFFA500 if msg - creation < 1200000 else 0x00ff00
  dot = yellow if msg - creation < 1200000 else green
  foot = age if msg - creation < 1200000 else not_rep
  embed = discord.Embed(color = color, title = f'User information {user}', description="Information -")
  embed.add_field(name = 'User: ', value = f"{user}\n<@{user.id}>\n**ID: **`{user.id}`", inline = False)
  embed.add_field(name = 'Account Created: ', value = f"<t:{creation}:D>\n<t:{creation}:R>", inline = False)
  embed.set_footer(text = f'User: {user.id} | {foot}', icon_url = dot)
  return embed