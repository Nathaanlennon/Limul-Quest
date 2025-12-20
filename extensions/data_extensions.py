# this is where all the additionnal data will be put, all the data that is not originally in the game-engine. 
# It will be imported in the universe_data and the player_data in the core but the said core will never know nor use it, it's only for your additional extensions that you make
from world import *
from test import saucisse

# You need to import your world classes here to be able to use them in the worlds dictionary below.
# from world import Test, Test2, Test3

# this is where you define the different worlds that your game will have.
# the name of the wolrd is the key and the value is the Class that defines the world.
worlds = {
    "Village1": Village1,
    "ButcherHouse": ButcherHouse,
    "Theatre": Theatre,
    "Village2": Village2,
    "zooKeeperHouse": zooKeeperHouse,
    "Zoo": Zoo,
    "Forest": Forest,
    "Cave": Cave,
    "Guild": Guild,
    "Forge": Forge,
    # "my_world": MyWorldClass,
}

# VERY IMPORTANT: those data dictionaries bellow can contain any type you want, including objects 
# BUT : if you use objects instances, you HAVE TO MAKE SURE that the classes has a function called "extract_data" that will return a serializable version of the object as a dictionary
# please add your instances in the instances below in universe_data
# if you don't do that, saving/loading the game will not work properly.
universe_data = {
    "instances": {
"saucisse":saucisse
    }
}

# If your objects need universe, add the instance in the list below, and self.universe in your class, so the program will do instance.universe = self
# you will need to import the instances at the top of the file too to do it.
# in those classes you HAVE TO HAVE the init_universe(self, universe) function that will set self.universe = universe at least, it's because yoy maybe need to init things that needs universe
instances = [
    # exemple: instance1, instance2
    saucisse
]

player_data = {
    "instances": {

    }
}
