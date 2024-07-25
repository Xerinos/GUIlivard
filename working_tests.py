from GUIlivard import *


class TestSpriteManager:

    def __init__(self):
        self.sprite_manager = SpriteManager()

    def test_image_add(self):
        self.sprite_manager.add_image("test", "%1e#1e57007f#1e000000%1e#1e000000#1e57007f", (60, 60))

        if self.sprite_manager.images != {"test": ["%1e#1e57007f#1e000000%1e#1e000000#1e57007f", (60, 60)]}:
            print("Exception in Image Add methode !")
            return False

        return True

    def test_sprite_add(self):
        self.sprite_manager.add_sprite("test", (10, 20), {"isAlive": True})

        if self.sprite_manager.sprites != {"test": [[(10, 20), {"isAlive": True}]]}:
            print("Exception in Sprite Add methode !")
            return False

        return True

    def test_sprite_remove(self):
        self.sprite_manager.remove_sprite("test")

        if self.sprite_manager.sprites != {} and self.sprite_manager.images != {"test": ["%1e#1e57007f#1e000000%1e#1e000000#1e57007f", (60, 60)]}:
            print("Exception in Sprite Remove methode !")
            return False

        return True

    def test_image_remove(self):
        self.sprite_manager.remove_image("test")

        if self.sprite_manager.sprites != {} and self.sprite_manager.images != {}:
            print("Exception in Image Remove methode !")
            return False

        return True

    def run_test(self):
        counter = 0

        counter += 1 if not self.test_image_add() else 0
        counter += 1 if not self.test_sprite_add() else 0
        counter += 1 if not self.test_sprite_remove() else 0
        counter += 1 if not self.test_image_remove() else 0

        print(f"{counter} issues occurred !")
        return


TestSpriteManager().run_test()


