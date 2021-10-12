import random
import discord
from redbot.core import commands

class Penis(commands.Cog):
    "Fight people with your penis and check who has the longest one"

    __author__ = "krak3n"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthor: {self.__author__}"    

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['pp'])
    @commands.cooldown(rate=1, per=3, type=commands.BucketType.user)    
    @commands.bot_has_permissions(embed_links=True)     
    async def penis(self, ctx, *, user: discord.Member = None):
        """
        Displays user's penis size.
        """
        if not user:
            user = ctx.author            
        embed = discord.Embed(
            title="Penis size machine ",color=await ctx.embed_color()
        )     
        
        if await self.bot.is_owner(user) or self.bot.user.id == user.id:
            embed.description=(f"**{user.name}'s penis:**\n8{'=' * random.randint(30,69)}D")
        else:
            embed.description=(f"**{user.name}'s penis:**\n8{'=' * random.randint(0, 35)}D")

        await ctx.reply(embed=embed,mention_author=False)   
