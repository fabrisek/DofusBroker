import logging

def setup_logs():
    logger = logging.getLogger("bot")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Gestionnaire de fichier pour les logs du bot et de Discord
    file_handler = logging.FileHandler('bot.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    discord_logger = logging.getLogger('discord')
    discord_logger.setLevel(logging.INFO)
    discord_logger.addHandler(file_handler)

    # Gestionnaire de console pour les logs du bot et de Discord
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    discord_logger.addHandler(console_handler)

    return logger
