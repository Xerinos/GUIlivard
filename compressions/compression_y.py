import PIL.Image


def methode_y(image):
    # Get the image colors
    image = PIL.Image.open(image)
    image = image.convert("RGBA")
    # Renvoie un tuple : (longueur, largeur)
    size = image.size

    compacted_image = []

    for i in range(size[0]):
        compacted_image += [[]]

        for j in range(size[1]):
            if compacted_image[-1] and compacted_image[-1][-1][-1] == image.getpixel((i, j)):
                compacted_image[-1][-1][0] += 1

            else:
                compacted_image[-1] += [[1, image.getpixel((i, j))]]

    return compacted_image