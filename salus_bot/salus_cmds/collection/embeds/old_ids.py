import discord

def old_report(ctx, user):
  creation = int(str(user.created_at.timestamp()).split('.')[0])
  embed = discord.Embed(color = 0xff0000, title = f'Scammer information {user}', description="Mass-added user. Please open a ticket in [KSF](https://www.discord.gg/ksf) for more information.\nInformation -")
  embed.add_field(name = 'User: ', value = f"{user}\n<@{user.id}>\n**ID: **`{user.id}`", inline = False)
  embed.add_field(name = 'Account Created: ', value = f"<t:{creation}:D>\n<t:{creation}:R>", inline = False)
  embed.set_footer(text = f'User: {user.id} | (!) USER REPORTED (!)', icon_url = 'https://www.pngall.com/wp-content/uploads/8/Red-Warning.png')
  return embed