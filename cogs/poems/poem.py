import os 
import config
import json
from discord.ext import commands
from .poem_templates import poem_selection_template, find_poem

#TODO: Manter uma to-do list para um dado membro.

here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, "stored_values.json")

try: 
    with open(filename) as file:
        stored_instances = json.load(file)
except FileNotFoundError:
    stored_instances = {}


class poem():
    def __init__(self, member, channel, state=False, sent_message=None):
        self.member = member
        self.channel = channel
        self.state = state
        self.sent_message = sent_message

    # Instantiate poem object as a selection
    async def selection(self):
        emb = poem_selection_template()
        await self.channel.send(f"{self.member.mention}")
        self.sent_message = await self.channel.send(embed=emb)

    # Update poem
    async def update_poem(self, reacted_message, emoji):
        for x,y in config.SUPPORTED_WRITERS:
            if y == emoji:
                 writer = x
                 break

        emb = find_poem(writer)
        await reacted_message.edit(embed=emb)

    # Dict <--> Object Equivalence
    def to_dict(self):
        return {
            "member": self.member.id,
            "channel": self.channel.id,
            "sent_message": self.sent_message.id,
            "state": self.state
        }


class poems(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()    
    async def on_raw_reaction_add(self, payload):
        member = payload.member 
        emoji = payload.emoji

        if member.id not in stored_instances: 
            return

        # Test if emoji is valid
        if str(emoji) in config.COLOUR_CIRCLES:     
            for quest_dic in stored_instances:
                
                quest = stored_instances[quest_dic]
                
                if quest["sent_message"] == payload.message_id and not quest["state"]:      
                    
                    guild = self.client.get_guild(payload.guild_id)
                    
                    # Recreate the poem's instance
                    current_template = poem(member,
                        guild.get_channel(quest["channel"]),
                        True,
                        await guild.get_channel(quest["channel"]).fetch_message(quest["sent_message"])
                        )

                    # Selection template --> Poem
                    await current_template.update_poem(
                        await guild.get_channel(quest["channel"]).fetch_message(quest["sent_message"]),
                        str(emoji)
                        )
                    
                    # Poem has been sent
                    quest["state"] = True

    @commands.command(name="poem", aliases=["poema"])
    async def new_poem(self, ctx):
        member = ctx.message.author 
        channel = ctx.message.channel

        # Check for user's template instance
        if member.id in stored_instances:
            msg = await channel.fetch_message(stored_instances[member.id]["sent_message"])
            await msg.delete()
            stored_instances[member.id] = None

        # Abir um novo template de escolha
        n_poem = poem(member, channel, False)
        await n_poem.selection()
        
        # Guardar os dados do template atual
        stored_instances[member.id] = n_poem.to_dict()
        
        with open(filename, "w") as file:
            json.dump(stored_instances, file)

def setup(client):
    client.add_cog(poems(client))