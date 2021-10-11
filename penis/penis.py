import random
import discord
from redbot.core import commands

class Penis(commands.Cog):
    "Fight people with your penis and check who has the longest one"
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['pp'])
    async def penis(self, ctx, *, user: discord.Member = None):
        """
        Displays users penis size.
        """
                    
        embed = discord.Embed(
            title="Penis size machine ",color=await ctx.embed_color()
        )     
        embed.description=(f"**{ctx.author.name or user.name}'s penis:**\n8{'=' * random.randint(0, 30)}D")

        await ctx.send(embed=embed)   
