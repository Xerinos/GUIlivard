import PIL.Image


def methode_nc(image):
    # Get the image colors
    image = PIL.Image.open(image)
    image = image.convert("RGBA")
    # Renvoie un tuple : (longueur, largeur)
    size = image.size

    compacted_image = []

    for i in range(size[1]):
        compacted_image += [[]]

        for j in range(size[0]):
            compacted_image[i] += [image.getpixel((j, i))]

    return compacted_image