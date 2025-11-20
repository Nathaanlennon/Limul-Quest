# this is where all the additionnal data will be put, all the data that is not originally in the game-engine. 
# It will be imported in the universe_data and the player_data in the core but the said core will never know nor use it, it's only for your additional extensions that you make

universe_data = {
    
}

player_data = {
    "abilities": {
        "fireball": {
            "name": "Fireball",
            "damage": 2,
            "accuracy": 0.0,
            "description": "A ball of fire that burns the enemy."
        },
        "ice_shard": {
            "name": "Ice Shard",
            "damage": 20,
            "accuracy": 0.9,
            "description": "A sharp shard of ice that pierces the enemy."
        }
    },
}