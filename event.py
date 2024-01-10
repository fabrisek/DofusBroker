from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f"{self.bot.user} is now online and is connected to " + str(len(self.bot.guilds)) + " servers")
        self.logger.info(f'Connecte en tant que {self.bot.user.name}')

        try:      
            synced = await self.bot.tree.sync()
            self.logger.info(f"Synced {len(synced)} command(s)")

            async for guild in self.bot.fetch_guilds(limit=250):
                self.logger.info(" - " + guild.name + " - " + str(guild.id))

        except Exception as e:
            self.logger.error(str(e))

async def setup(bot, logger):
    # finally, adding the cog to the bot
    await bot.add_cog(Events(bot=bot, logger=logger))