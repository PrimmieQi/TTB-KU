import nextcord
from nextcord.ext import commands
import core.timetable as Timetable
from dotenv import load_dotenv
import os

load_dotenv()

Token = os.getenv("TOKEN")

                        #On Ready
#############################################################
class Bot(nextcord.ext.commands.Bot):
    async def on_ready(self):
        for guild in self.guilds:
            self.default_guild_ids.append(guild.id)

    async def on_guild_join(self, guild: nextcord.Guild):
        self.default_guild_ids.append(guild.id) 
#############################################################

bot = commands.Bot(command_prefix="$")

@bot.slash_command(name="ttb", description="Get your timetable")
async def send(interaction: nextcord.Interaction):
    await interaction.response.send_modal(Timetable.NextcordHandler())

bot.run(Token) 
