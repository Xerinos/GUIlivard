from kandinsky import *
from ion import *


class SpriteManager:

    def __init__(self):
        # Contain all images as “name”: {"image”: image, “sizes”: (w, h)}
        self.images: dict = {}
        # Contain all sprites. It can be interpreted as an instance of an image
        # for each coordinate.
        # Sprites are stored by id as this :
        #       “id”: [{"image": "image name from self.images", "loc": position, "args": parameters}]
        self.sprites: dict = {}

    def add_image(self, name, image, sizes) -> False | dict:
        """
        Add the image to the list of image. Then you can create Sprites with it.
        :param name: The name of the image.
        :param image: The image (the version compressed; here we want the last compress version : hex_compression).
        :param sizes: The size of the image that is a tuple with (width, height).
        :return: It will return True after loading the image.
        """
        # If an image already exists with this name
        if name in self.images:
            # Choose another name or delete the image first
            return False

        else:
            # Add the image to the image list
            self.images[name] = {"image": image, "sizes": (sizes[0], sizes[1])}
            # Return the pair Key-Value created
            return {name: {"image": image, "sizes": (sizes[0], sizes[1])}}

    def add_sprite(self, image_name, position: list[int, int], parameters: dict) -> False | dict:
        """
        Add a sprite from an image
        :param image_name: The name of the image you want
        :param position: The x and y position you want to place the sprite
        :param parameters: Some more parameter if you need it. The goal is to do as if it is an object
        :return: It will return True after loading the sprite.
        """
        # If the image name does no exist
        if not (image_name in self.images):
            # You have to add the image before
            return False

        else:
            # Add the sprite
            self.sprites[str(int(self.sprites[-1]) + 1)] = {
                "image": image_name,
                "loc": position,
                "args": parameters
            }
            # Return the pair Key-Value created
            return {self.sprites[-1]: self.sprites[self.sprites[-1]]}

    def remove_image(self, name) -> False | dict:
        """
        Remove the image you want and in the same time all the sprites that use it
        :param name: The image name
        :return: Return True if the name is correct, else False.
        """
        # If it still sprites using this image
        if name in [identifier["image"] for identifier in self.sprites]:
            # You have to delete sprite first
            return False

        # If the image exists
        if name in self.images:
            # Del the images that correspond to it
            images = self.images[name]
            del self.images[name]
            return {name: images}

        else:
            # This image does not exist
            return False

    def remove_sprite(self, identifier) -> False | dict:
        """
        Remove all the sprites that use the image with the name given
        :param identifier: The identifier of the sprite
        :return: Return the sprite if the identifier is correct, else False.
        """
        # If an identifier match
        if identifier in self.sprites:
            # Del it
            sprite = self.sprites["id"]
            del self.sprites["id"]
            # Return the deleted element
            return {identifier: sprite}

        else:
            # If it does not exist…
            return False

    def check_collide_at(self, position: tuple[int, int]) -> list[str,]:
        """
        Get Sprites from the given position
        :param position: The position (x, y)
        :return: Return all the Sprites identifier at the position given in a list.
        """
        result: list = []

        # Check the position for each sprite
        for identifier in self.sprites:
            # If (x <= pos_x <= x + w) and (y <= pos_y <= y + h)
            if self.sprites[identifier]["loc"][0] <= position[0] <= self.sprites[identifier]["loc"][0] + self.images[self.sprites[identifier]["image"]]["sizes"][0] and self.sprites[identifier]["loc"][1] <= position[1] <= self.sprites[identifier]["loc"][1] + self.images[self.sprites[identifier]["image"]]["sizes"][1]:
                # Add the identifier to the list
                result += [identifier]

        # Return id
        return result

    def check_collide_between(self, position: tuple[int, int, int, int] | list[int, int, int, int]) -> list[str,]:
        """
        Get all sprites that touch the rect with the coordinates position (x, y, w, h).
        :param position: The position as (x, y, w, h)
        :return: Return a list with all Sprites identifiers that touch the rectangle given.
        """

        def del_duplicate(list1: list, list2: list) -> list:
            # Check for duplicate and add others to the main result list (result)
            for ident in list2:
                if id in list1:
                    pass
                else:
                    list1 += [ident]

            return list1

        """
        position[0] + position[2], position[1] + position[3]
        position[0], position[1]
        position[0] + position[2], position[1]
        position[0], position[1] + position[3]
        """
        # Put all identifier that collide with each corner of the given rect
        result = del_duplicate(
            del_duplicate([position[0] + position[2], position[1] + position[3]], [position[0], position[1]]),
            del_duplicate([position[0] + position[2], position[1]], [position[0], position[1] + position[3]]))

        # Check if the sprites are in the rect
        for identifier in self.sprites:
            x = self.sprites[identifier]["loc"][0]
            y = self.sprites[identifier]["loc"][1]
            w = self.images[self.sprites[identifier]["image"]]["sizes"][0]
            h = self.images[self.sprites[identifier]["image"]]["sizes"][1]

            if (position[0] < x < position[0] + position[2] and position[1] < y < position[1] + position[3] and
                position[0] < x + w < position[0] + position[2] and position[1] < y + h < position[1] + position[3]):
                result += [identifier]

        return result

    def get_by(self, key, value) -> list:
        """
        Get the sprites with the value of the argument given by the key
        :param key: The name of the argument.
        :param value: The value of the argument
        :return: Return all ID
        """
        result = []

        for group in self.sprites:
            for sprite in self.sprites[group]:

                if key in self.sprites[group][sprite] and self.sprites[group][sprite][key] == value:
                    result += [self.sprites[group][sprite]["id"]]

        return result


class EventManager:

    def __init__(self):
        pass


class Screen:

    def __init__(self):
        self.sizes = (320, 222)
        self.x = 0
        self.y = 0

    def fast_print(self, image, sizes, coordinates: tuple[int, int]):
        x = 0
        y = 0
        line_count = 0

        for shape in image:
            if len(shape) == 3:
                fill_rect(coordinates[0] + x, coordinates[1] + y, shape[0], shape[1], shape[-1])
                line_count = shape[1] - 1
                x += shape[0]

            elif len(shape) == 2:
                fill_rect(coordinates[0] + x, coordinates[1] + y, shape[0], line_count + 1, shape[-1])
                x += shape[0]

            else:
                set_pixel(coordinates[0] + x, coordinates[1] + y, shape[-1])
                x += 1

            if x == sizes[0]:
                x = 0
                y += line_count + 1
                line_count = 0


class GUIlivard:

    def __init__(self):
        pass
