# this is where all the additionnal data will be put, all the data that is not originally in the game-engine. 
# It will be imported in the universe_data and the player_data in the core but the said core will never know nor use it, it's only for your additional extensions that you make
from world import *

# You need to import your world classes here to be able to use them in the worlds dictionary below.
# from world import Test, Test2, Test3

# this is where you define the different worlds that your game will have.
# the name of the wolrd is the key and the value is the Class that defines the world.
worlds = {
    "Village1": Village1,
    "ButcherHouse": ButcherHouse,
    "Theatre" : Theatre,
    "Village2": Village2,
    "zooKeeperHouse": zooKeeperHouse,
    "Zoo": Zoo,
    "Forest" : Forest,
    "Cave" : Cave,
    "Guild" : Guild,
    "Forge" : Forge,
    #"my_world": MyWorldClass,
}

# VERY IMPORTANT: those data dictionaries bellow can contain any type you want, including objects 
# BUT : if you use objects instances, you HAVE TO MAKE SURE that the classes has a function called "extract_data" that will return a serializable version of the object as a dictionary
# if you don't do that, saving/loading the game will not work properly.
universe_data = {

}

player_data = {
    
}