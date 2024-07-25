import PIL.Image


def methode_x(image):
    image = PIL.Image.open(image)
    # TODO : transparence
    image = image.convert("RGBA")
    # Renvoie un tuple : (longueur, largeur)
    size = image.size

    compacted_image = []

    for i in range(size[1]):
        compacted_image += [[]]

        for j in range(size[0]):
            if compacted_image[-1] and compacted_image[-1][-1][-1] == image.getpixel((j, i)):
                compacted_image[-1][-1][0] += 1

            else:
                compacted_image[-1] += [[1, image.getpixel((j, i))]]

    return compacted_image