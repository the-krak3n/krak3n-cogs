import random
import asyncio
import discord
from redbot.core import commands, Config
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import ReactionPredicate


class Penis(commands.Cog):
    """Fight people with your penis and check who has the longest one"""

    __author__ = "krak3n & Aioxas"
    __version__ = 0.3

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthor: {self.__author__}\nCog Version: {self.__version__}"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=98713798, force_registration=True
        )
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
            title="Penis size machine ", color=await ctx.embed_color()
        )

        rigged = await self.config.rigged()
        if (
            await self.bot.is_owner(user)
            or self.bot.user.id == user.id
            or user.id in rigged
        ):
            embed.description = f"**{user}'s penis:**\n8{'=' * random.randint(30,69)}D"
        else:
            embed.description = f"**{user}'s penis:**\n8{'=' * random.randint(0, 35)}D"

        await ctx.reply(embed=embed, mention_author=False)

    @commands.group()
    @commands.is_owner()
    async def ppset(self, ctx):
        """Penis-related settings"""

    @ppset.command(name="add")
    async def pp_add(self, ctx: commands.Context, *, user: discord.Member = None):
        """Add a user to the rigged penis list. They have small pps tbh."""
        rigged = await self.config.rigged()
        if not user:
            raise commands.UserInputError
        if user.id in rigged:
            await ctx.send(f"{user} is already in the rigged pp list")
        else:
            rigged.append(user.id)
            await self.config.rigged.set(rigged)
            await ctx.send(f"{user} has been added to the rigged pp list.")

    @ppset.command(name="list")
    async def pp_list(self, ctx: commands.Context):
        """List the rigged people cause they have small pp."""
        rigged = await self.config.rigged()
        if len(rigged) < 1:
            await ctx.send(
                f"Rigged pp list is currently empty. Add new people to the list using `{ctx.clean_prefix}ppset add <Discord name or nickname>`"
            )
            return
        rigged = [self.bot.get_user(rigged_id).name for rigged_id in rigged]
        rigged = sorted(
            rigged,
            key=lambda item: (
                int(item.partition(" ")[0]) if item[0].isdigit() else float("inf"),
                item,
            ),
        )
        msg = ", ".join(rigged[:-2] + [" and ".join(rigged[-2:])])
        await ctx.send(f"Current people with rigged pps are: `{msg}`")

    @ppset.command(name="remove")
    async def pp_remove(self, ctx: commands.Context, *, user: discord.Member = None):
        """Remove a user from rigged penis list cause they bumped their size somehow."""
        rigged = await self.config.rigged()
        if not user:
            raise commands.UserInputError
        if user.id not in rigged:
            await ctx.send(f"{user} is not in the rigged pp list.")
        else:
            rigged.remove(user.id)
            await self.config.rigged.set(rigged)
            await ctx.send(f"{user} has been removed from the rigged pp list.")

    @ppset.command(name="clear")
    @commands.bot_has_permissions(add_reactions=True)
    async def ppset_clear(self, ctx: commands.Context):
        """Clear [botname]'s rigged penis list. They dont deserve it."""
        rigged = await self.config.rigged()
        msg = await ctx.send("Do you really dont want every user in the rigged pp list to be removed?")     
        start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)
        pred = ReactionPredicate.yes_or_no(msg, ctx.author)
        try:
            await self.bot.wait_for("reaction_add", check=pred, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send("How rude..ignoring me.......")
        else:
            if pred.result is True:
                rigged.clear()
                await self.config.rigged.set(rigged)
                await ctx.send("Removed everyone from the rigged pp list, they suck..")
            else:    
                await ctx.send("I guess you still want them to have their pp privileges, so I wont clear.")             
