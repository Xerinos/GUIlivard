import PIL.Image


def methode_xy(image):
    # Get the image colors
    image = PIL.Image.open(image)
    image = image.convert("RGBA")
    # Renvoie un tuple : (longueur, largeur)
    size = image.size
    compacted_image = []


    for i in range(size[1]):
        compacted_image += [[1, []]]

        for j in range(size[0]):
            if compacted_image[-1][-1] and compacted_image[-1][-1][-1][-1] == image.getpixel((j, i)):
                compacted_image[-1][-1][-1][0] += 1

            else:
                compacted_image[-1][-1] += [[1, image.getpixel((j, i))]]

        if len(compacted_image) > 1 and compacted_image[-1][-1] == compacted_image[-2][-1]:
            compacted_image[-2][0] += 1
            del compacted_image[-1]

    return compacted_image