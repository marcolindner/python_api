from models import Item

class Helper():

    def find_item(itemid: str, items: Item):
        for item in items:
            if item.id == itemid:
                return item
        return None

    def replace_item(new_item: Item, items: Item):
        for index, item in enumerate(items):
            if item.id == new_item.id:
                items[index] = new_item
            else:
                return None