import configparser
import os

import discord
from discord.ext import commands
import logs
import event
import sys
from broker import broker_commands

# Get Config
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

# Discord Config
DiscordToken = config["DEFAULT"]["discord_token"]
command_prefix = config["DEFAULT"]["command_prefix"]

# Configurer le logger en appelant la fonction setup_logger()
logger = logs.setup_logs()

class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=command_prefix,
            intents=discord.Intents.all()
        )

    async def setup_hook(self):
        event_cog = event.Events(self, logger)
        await self.add_cog(event_cog)

        broker_cog = broker_commands.BrokerCommands(self,logger)
        await self.add_cog(broker_cog)
        
DiscordBot().run(DiscordToken)