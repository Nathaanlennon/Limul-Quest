# this is where all the additionnal data will be put, all the data that is not originally in the game-engine. 
# It will be imported in the universe_data and the player_data in the core but the said core will never know nor use it, it's only for your additional extensions that you make


# You need to import your world classes here to be able to use them in the worlds dictionary below.
# from world import Test, Test2, Test3

from world import Village1;
from world import ButcherHouse;
from world import Theatre;
from world import Village2;
from world import zooKeeperHouse;
from world import Zoo;
from world import Forest;
from world import Cave;


# this is where you define the different worlds that your game will have.
# the name of the wolrd is the key and the value is the Class that defines the world.
worlds = {
    "Village1": Village1,
    "ButcherHouse": ButcherHouse,
    "Theatre" : Theatre,
    "Village2": Village2,
    "zooKeeperHouse": zooKeeperHouse,
    "Zoo": Zoo,
    "Forest": Forest,
    "Cave": Cave,
    

}

# VERY IMPORTANT: those data dictionaries bellow can contain any type you want, including objects 
# BUT : if you use objects instances, you HAVE TO MAKE SURE that the classes has a function called "extract_data" that will return a serializable version of the object as a dictionary
# if you don't do that, saving/loading the game will not work properly.
universe_data = {
    
}


player_data = {
    
}