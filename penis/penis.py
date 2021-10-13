import random
import discord
from redbot.core import commands, Config

class Penis(commands.Cog):
    """Fight people with your penis and check who has the longest one"""

    __author__ = "krak3n & Aioxas"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthor: {self.__author__}"    

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=98713798, force_registration=True)
        default_global = {"rigged": []}
        self.config.register_global(**default_global)

    @commands.command(aliases=["pp"])
    @commands.cooldown(rate=1, per=3, type=commands.BucketType.user)    
    @commands.bot_has_permissions(embed_links=True)     
    async def penis(self, ctx: commands.Context, *, user: discord.Member = None):
        """
        Displays user's penis size.
        """
        if not user:
            user = ctx.author            
        embed = discord.Embed(
            title="Penis size machine ",color=await ctx.embed_color()
        )     

        rigged = await self.config.rigged()
        if await self.bot.is_owner(user) or self.bot.user.id == user.id or user.id in rigged:
            embed.description=(f"**{user.name}'s penis:**\n8{'=' * random.randint(30,69)}D")
        else:
            embed.description=(f"**{user.name}'s penis:**\n8{'=' * random.randint(0, 35)}D")

        await ctx.reply(embed=embed, mention_author=False)

    @commands.group()
    @commands.is_owner()
    async def ppset(self, ctx):
        """Penis-related settings"""

    @ppset.command(name="add")
    async def pp_add(self, ctx: commands.Context, *, user: discord.Member = None):
        """Add a user to the rigged penis list. They have small pps tbh."""
        rigged = await self.config.rigged()
        if user.id in rigged:
            await ctx.send(f"{user.display_name} is already in the rigged list")
        else:
            rigged.append(user.id)
            await self.config.rigged.set(rigged)
            await ctx.send(f"{user.display_name} has been add to the rigged list.")

    @ppset.command(name="list")
    async def pp_list(self, ctx: commands.Context):
        """List the rigged people cause they have small pp."""
        rigged = await self.config.rigged()
        if len(rigged) < 1:
            await ctx.send(
                "Rigged list is currently empty, add new people to the rigged list using ppset add"
                " <Discord name or nickname>"
            )
            return
        rigged = [self.bot.get_user(rigged_id).display_name for rigged_id in rigged]
        rigged = sorted(
            rigged,
            key=lambda item: (
                int(item.partition(" ")[0]) if item[0].isdigit() else float("inf"),
                item,
            ),
        )
        msg = ", ".join(rigged[:-2] + [" and ".join(rigged[-2:])])
        await ctx.send(f"Current people with rigged pps are: {msg}")

    @ppset.command(name="remove")
    async def pp_remove(self, ctx: commands.Context, *, user: discord.Member = None):
        """Remove a user from rigged list cause they bumped their size somehow."""
        rigged = await self.config.rigged()
        if user.id not in rigged:
            await ctx.send(f"{user.display_name} is not in the rigged list.")
        else:
            rigged.remove(user.id)
            await self.config.rigged.set(rigged)
            await ctx.send(f"{user.display_name} has been removed from the rigged list.")
