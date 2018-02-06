import asyncio
import discord

client = discord.Client()
permEditor = discord.Permissions()
permOverwrite = discord.PermissionOverwrite()
token = "token"
debug_start = "------DEBUG ZONE---------"
debug_end = "-------------------------"


def ownerCheck(auteur):
    
    print(auteur)
    if auteur == 'GinoX27#8745' or auteur == 'GinoX27':
        return True
    else:
        return False

@client.event
async def on_message(message):

    if message.content.startswith("!gameStatus"):
        gameStatus = message.content.split("!gameStatus")
        gameStatus = " ".join(gameStatus)
        await client.change_status(game=discord.Game(name=gameStatus), idle=False)

    if message.content.startswith("!mute"):
        print(debug_start)
        print(message.content)
        print(debug_end)
        userToMute = message.content.split("!mute")
        userToMute = "".join(userToMute)
        userToMute = userToMute.split("<@")
        userToMute = "".join(userToMute)
        userToMute = userToMute.split(">")
        userToMute = "".join(userToMute)
        permOverwrite.send_messages = False
        member = discord.utils.get(message.server.members, id=userToMute)
        print(debug_start)
        print("ID : "+userToMute)
        #print("Méthode : "+str(discord.utils.get(message.server.members, id=userToMute)))
        print("Méthode : "+str(member))
        print(debug_end)
        await client.edit_channel_permissions(message.channel, member, permOverwrite)

    if message.content.startswith("!unmute"):
        pass

    if message.content.startswith("!clear"):
        clr_amount = message.content.split("!clear")
        clr_amount = "".join(clr_amount)
        clr_amount = int(clr_amount) #On met en place le nombre indiqué par la personne
        if clr_amount >= 101:
            await client.delete_message(message)
            e_clr = discord.Embed(title="Montant maximum dépassé",
                                  description="Le montant ne doit pas excéder 100",
                                  color=0x010101)
            clr_ans_dnd = await client.send_message(message.channel, embed=e_clr)
            await asyncio.sleep(3)
            list_del_dnd = [e_clr, clr_ans_dnd]
            await client.delete_message(clr_ans_dnd)
            pass
        elif clr_amount <= 100:
            await client.delete_message(message)
            await client.purge_from(message.channel, limit=clr_amount)
            e_clr2 = discord.Embed(title="Messages supprimés")
            clr_ans_grt = await client.send_message(message.channel, embed=e_clr2)
            await asyncio.sleep(3)
            list_del_grt = [e_clr2, clr_ans_grt]
            await client.delete_message(clr_ans_grt)
            pass


    if message.content.startswith("!test"):
        print("test reçu")
        await client.send_message(message.channel, "J'ai bien reçu ton putain de test")

    if message.content.startswith("!etest") and ownerCheck(str(message.author)) == True:
        print("Embed test reçu")
        e_answer = discord.Embed(color=0x010101)
        e_answer.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        e_answer.add_field(name="Champ1", value="Valeur1")
        e_answer.add_field(name="Champ2", value="Valeur2")
        await client.send_message(message.channel, embed=e_answer)
        print(debug_start)
        print(debug_end)
        pass
    if message.content == '#authorCheck':
        print(ownerCheck(str(message.author)))
        await client.send_message(message.channel, ownerCheck(message.author))

    if message.content.startswith("!myroles"):
        #top_role = message.author.top_role
        #print(top_role)
        all_roles = message.author.roles
        for sev_roles in all_roles[1:]:
            print(sev_roles)
            await client.send_message(message.channel, sev_roles)

    #if message.content.startswith("!mycreation"):
        #crea_jour = message.author.created_at.strftime('%d/%m/%Y')
        #crea_temps = message.author.created_at.strftime('%H:%M:%S.%f')
        #e_answer = discord.Embed(color=0x010101, title='')
        #e_answer.add_field(name="lol")

@client.event
async def on_message_delete(message):
    if message.author == client.user:
        pass
    elif message.content.startswith("!clear"):
        pass
    else:
        print(debug_start)
        log_chan = discord.utils.get(message.server.channels, name="log")
        print(log_chan)
        print(log_chan.id)
        print(debug_end)
        deleted_since = message.timestamp.strftime("%d/%m/%Y %H:%M:%S.%f")
        e2_embed = discord.Embed(title="Ce message a été supprimé", 
                                 description=message.content, 
                                 color=0x010101)
        #e2_embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        e2_embed.add_field(name="Auteur", value=message.author.mention)
        e2_embed.add_field(name="Salon", value=message.channel.mention)
        e2_embed.add_field(name="Temps", value=deleted_since)
        await client.send_message(log_chan, embed=e2_embed)

@client.event
async def on_message_edit(before, after):
    if after.author == client.user:
        pass
    else:
        log_chan = discord.utils.get(after.server.channels, name="log")
        edited_since = after.timestamp.strftime("%d/%m/%Y %H:%M:%S.%f")
        edit_embed = discord.Embed(title="Message édité !", color=0x010101)
        edit_embed.add_field(name="Avant", value=before.content)
        edit_embed.add_field(name="Après", value=after.content, inline=False)
        edit_embed.add_field(name="Auteur", value=after.author.mention)
        edit_embed.add_field(name="Salon", value=after.channel.mention)
        edit_embed.add_field(name="Temps", value=edited_since)
        await client.send_message(log_chan, embed=edit_embed)

@client.event
async def on_member_join(member):
    pass

@client.event
async def on_ready():
    print(client.user.name + " Connecté")
    print("ID: " + client.user.id)
    print("---------------------")

client.run(token)