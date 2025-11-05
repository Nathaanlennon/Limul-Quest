import logging

logger = logging.getLogger("game_logger")
logger.setLevel(logging.INFO)

# Création du handler fichier
file_handler = logging.FileHandler("game.log", mode="a")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# Ajouter le handler au logger
logger.addHandler(file_handler)
