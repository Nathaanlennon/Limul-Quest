import os
import json
from engine.core.logging_setup import logger
from engine.core.ItemManager import item_list_renderer, Inventory, dealItem

class ShopManager:
    def __init__(self, player=None):
        self.shops = [] # list of inventories representing shops
        self.player = player
        self.current_shop = None
        # load shops from assets/shops/shops.json
        shops_file = "assets/shops/shops.json"
        if os.path.exists(shops_file) and os.path.isfile(shops_file):
            try:
                with open(shops_file, "r", encoding="utf-8") as f:
                    shops = json.load(f)
                    for shop in shops:
                        new_shop = Inventory()
                        new_shop.load_data(shop)
                        self.shops.append(new_shop)
            except (json.JSONDecodeError, OSError) as e:
                logger.warning(f"Erreur lors du chargement de {shops_file} : {e}")
                self.shops = []
        else:
            logger.warning(f"Fichier de shops introuvable : {shops_file}")
            self.shops = []

    def require(self, item_id):
        # verify if the requirements for the item to appears in the shop are met
        if self.current_shop is None:
            return False

        item_data = self.current_shop.items.get(item_id, {})
        require = item_data.get("require", {})
        if not require or require == {}:
            return True
        for key, value in require.items():
            if key.startswith("player:"):
                subkey = key.split(":", 1)[1]
                if subkey.startswith("has_item:"):
                    item_req_id = subkey.split(":", 1)[1]
                    if self.player.inventory.items.get(item_req_id, 0) < 1:
                        return False
                else:
                    if self.player.ext_data.get(subkey) != value:
                        return False
            elif key.startswith("level:"):
                level_req = int(key.split(":", 1)[1])
                if self.player.level < level_req:
                    return False
            else:
                if self.player.ext_data.get(key) != value:
                    return False
        return True

    def set_shop(self, shop_id):
        if 0<=shop_id < len(self.shops):
            self.current_shop = self.shops[shop_id]
            dealItem.setup_dealer(inventory_a=self.player.inventory, inventory_b=self.current_shop, mode="buy")
            # set items in item_list_renderer
            item_list = {}
            for item, data in self.current_shop.items.items():
                if self.require(item):
                    item_list[item] = data["quantity"]
            item_list_renderer.set_list(item_list)
            item_list_renderer.current_index = 0

        else:
            logger.warning(f"Shop '{shop_id}' introuvable dans la base de données de shops.")
            self.current_shop = None






shop_manager = ShopManager()
def setup_shops(player):
    shop_manager.player = player