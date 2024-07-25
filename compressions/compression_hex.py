import PIL.Image


def dec_to_hex(number: int) -> str:
    return str(hex(number))[2:] if len(str(hex(number))[2:]) == 2 else "0" + str(hex(number))[2:]


def hex_to_dec(number: str) -> int:
    result = 0
    hex_char = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f')

    for char in range(len(number)):
        result += hex_char.index(number[-char - 1]) * 16 ** char

    return int(result)


def hex_converter(image: PIL.Image, alpha) -> list[list[str,],]:
    hex_colors = []

    # Pour chaque ligne
    for i in range(image.size[1]):
        hex_colors += [[]]

        # Pour chaque pixel (de chaque ligne)
        for j in range(image.size[0]):

            # Si on prend la transparence : (0, 0, 0, 0) sinon (0, 0, 0)
            if alpha:
                colors = dec_to_hex(image.getpixel((j, i))[0]) + dec_to_hex(image.getpixel((j, i))[1]) + dec_to_hex(
                    image.getpixel((j, i))[2]) + dec_to_hex(image.getpixel((j, i))[3])
            else:
                colors = dec_to_hex(image.getpixel((j, i))[0]) + dec_to_hex(image.getpixel((j, i))[1]) + dec_to_hex(
                    image.getpixel((j, i))[2])
            hex_colors[i] += [colors]

    return hex_colors


def compress_pixel(line: list[str,], delimiter: str) -> str:
    count = 0
    # Enregistre la dernière couleur
    last_color = ""
    # Enregistre le résultat
    result = ""

    # Pour chaque couleur :
    for color in line + ["NONE"]:

        # Si c'est la même que la dernière on ajoute 1 au compteur
        if color == last_color:
            count += 1

        else:
            if count == 0:
                result += last_color

            else:
                result += delimiter + dec_to_hex(count + 1) + last_color

            last_color = color
            count = 0

    return result


def compress_line(image: list[str,], delimiter: str) -> str:
    count = 0
    last_line = ""
    result = ""

    for line in image + ["NONE"]:

        if line == last_line:
            count += 1

        else:
            if count == 0:
                result += last_line

            else:
                result += delimiter + dec_to_hex(count + 1) + last_line

            last_line = line
            count = 0

    return result


def compression_hex(image, alpha: bool = False) -> (str, tuple[int, int]):
    image = PIL.Image.open(image)
    image = image.convert("RGBA")
    # Renvoie un tuple : (longueur, largeur)
    size = image.size

    hex_image = hex_converter(image, alpha)

    hex_image_pixel_compress = []
    for line in hex_image:
        hex_image_pixel_compress += [compress_pixel(line, "#")]

    return compress_line(hex_image_pixel_compress, "%"), size


def unpack_color(hex_color, alpha: bool = False) -> tuple[int, ...]:
    if alpha:
        return (hex_to_dec(hex_color[0:2]),
                hex_to_dec(hex_color[2:4]),
                hex_to_dec(hex_color[4:6]),
                hex_to_dec(hex_color[6:8]))

    else:
        return (hex_to_dec(hex_color[0:2]),
                hex_to_dec(hex_color[2:4]),
                hex_to_dec(hex_color[4:6]))


def uncompress_fast_print(compress_image: str, size: tuple[int, int], alpha: bool = False) -> list[list[tuple[int, tuple[int,]],],]:
    image = []

    delimiter = ("#", "%")

    x_count = 0

    x = 1
    y = 1

    while compress_image:
        # Si on a le caractère % -> Indiquer qu'il faut répéter la ligne ... fois
        if compress_image[0] == delimiter[1]:  # This is the line delimiter (%)
            y = hex_to_dec(compress_image[1:3])
            compress_image = compress_image[3:]

        # Si on a le caractère # -> Indiquer qu'il faut répéter la couleur ... fois
        if compress_image[0] == delimiter[0]:  # This is the color delimiter (#)
            x = hex_to_dec(compress_image[1:3])
            compress_image = compress_image[3:]

        if compress_image[0] != delimiter[0] and compress_image[0] != delimiter[1]:
            color: tuple
            if alpha:
                color = unpack_color(compress_image[0:8])
                compress_image = compress_image[8:]
            else:
                color = unpack_color(compress_image[0:6])
                compress_image = compress_image[6:]

            if y > 1:
                image += [(x, y, color)]

            elif x > 1:
                image += [(x, color)]

            else:
                image += [[color]]

            x_count += x
            x = 1

        if x_count == size[0]:
            y = 1
            x_count = 0

    return image


# ('%1e#1e57007f#1e000000%1e#1e000000#1e57007f', (60, 60))
print(compression_hex("../assets/test.png"))
print(uncompress_fast_print("#64ff0000%130026ff#63ffffff", (60, 60)))