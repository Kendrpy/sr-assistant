import discord
from ... import db_requests as req 

def staff_embed(staff, role):
  reports = req.sr_reports(staff.id)
  creation = int(str(staff.created_at.timestamp()).split('.')[0])
  if staff.id == 165343848669642754:
    color = 0x420D1E
  else:
    color = 0x03B5FC
  if staff.id == 808403290755825715:
    avatar = 'https://c.tenor.com/uoszxRS3NQIAAAAC/ratjam-jam.gif'
  else:
    avatar = staff.avatar if staff.avatar else staff.default_avatar
  embed = discord.Embed(color = color, title = f'KSF Staff - {staff}', description="Information -")
  embed.set_thumbnail(url = avatar)
  embed.add_field(name = 'User info', value = f"<@{staff.id}>\n**Username:**\n`{staff}`\n**ID:**\n`{staff.id}`", inline = True)
  if reports:
    embed.add_field(name = 'Rank ', value = f"{role}\n`{reports} reports`", inline = True)
  else:  
    embed.add_field(name = 'Rank ', value = f"{role}", inline = True)
  embed.add_field(name = 'Account Created: ', value = f"<t:{creation}:D>\n<t:{creation}:R>", inline = False)
  return embed