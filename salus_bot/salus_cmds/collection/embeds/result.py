import discord
from discord.ui import Button, View
from .constants import EMPTY

async def result_embed(arg, users, message, **kwargs):
  def add_embed(arg, users):
    embed = discord.Embed(color = arg['tag_color'], title = arg['tag_name'])
    avatar = users['subject'].avatar if users['subject'].avatar else users['subject'].default_avatar
    embed.set_thumbnail(url = avatar)
    embed.add_field(name = 'User info', value = f"<@{arg['subject_id']}>\n{users['subject']}\n**ID: **`{arg['subject_id']}`", inline = True)
    if arg['alts']:
      alts = ''
      for alt in arg['alts'].split(','):
        alts += f'`{alt}` '
      embed.add_field(name = 'Alt Accounts IDs', value = alts, inline = True)
    else:
      embed.add_field(name = 'Alt Accounts IDs', value = EMPTY, inline = True)
    embed.add_field(name = 'KSF Staff Reporter', value = f"<@{arg['sr_id']}>\n{users['sr_user']}\n**ID: **`{arg['sr_id']}`", inline = True)  
    embed.add_field(name = 'Game', value = f"`{arg['game']}`", inline = True)
    embed.add_field(name = 'Added On', value = f"<t:{int(arg['timestamp'])}:D>\n<t:{int(arg['timestamp'])}:R>", inline = True)
    if str(arg['anonymous']) == '1':
      embed.add_field(name = 'Reporter', value = f"`Anonymous report`", inline = True)
    else:
      if arg['reporter_id'] == 'Unknown':
        embed.add_field(name = 'Reporter', value = f"`Unknown`", inline = True)
      else:
        embed.add_field(name = 'Reporter', value = f"<@{arg['reporter_id']}>\n{users['reporter']}\n**ID: **`{arg['reporter_id']}`", inline = True)
    if arg['reason'] != '':
      embed.add_field(name = 'Reason(s)', value = f"> {arg['reason']}", inline = False)
    else:
      embed.add_field(name = 'Reason(s)', value = f"`No reason`", inline = False)
    return embed
  show_proofs = Button(label ='Show proofs', style = discord.ButtonStyle.blurple)
  async def other_callback(interaction):
      async def show_proofs(arg):
        embeds = list()
        embeds.append(add_embed(arg, users))
        proofs = arg['proofs'].split(',')
        num = 9 if len(proofs) <= 9 else 8
        for index, proof in enumerate(proofs):
          if index < num:
            embeds.append(discord.Embed(color = arg['tag_color'], description=EMPTY))
            embeds[index+1].set_image(url = proof)
          else:
            break
        if len(proofs) > 9:
          text = ''
          for i in range(8, len(proofs)):
            text += f'[Proof {i+1}]({str(proofs[i])})\n'
          embeds.append(discord.Embed(color = arg['tag_color'], description=text))
          
        return embeds
      await interaction.response.edit_message(embeds=await show_proofs(arg), view=None)
      return True
  show_proofs.callback = other_callback
  view = View() 
  if arg['proofs']:
    view.add_item(show_proofs)
  await message.channel.send(embed=add_embed(arg, users), view =view)
  if 'shout' in kwargs:
    bot = kwargs.get('bot')
    channel = bot.get_channel(int(kwargs.get('channel')))
    msg = await channel.send(f"<a:KSFalert:897042289514405929> {arg['tag_name']} {kwargs.get('shout')} <a:KSFalert:897042289514405929> <@&{kwargs.get('shout_ping')}>",embed=add_embed(arg, users), view=view)
    await msg.publish()