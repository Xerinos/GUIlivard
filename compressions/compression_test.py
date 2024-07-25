import PIL.Image

class ImageConverter:

    def __init__(self):
        pass

    def compress(self, image):
        image = PIL.Image.open(image)
        # TODO : transparence
        image = image.convert("RGBA")
        # Renvoie un tuple : (longueur, largeur)
        size = image.size

        # TODO : new methode : [[color, [places]], ...]         (mcc : methode color compact)
        # TODO : places can be "1x5:2" or "5x5" for exemple

        def methode_mcc():
            pass

        # TODO : Check block compression (mb : methode block)

        def methode_ctc():
            """Methode Char to Char"""

            def step1():
                compacted_image = [[], str(size[0]) + "x" + str(size[1])]

                # Parcourir tous les pixels (par lignes)
                for i in range(size[1]):
                    for j in range(size[0]):

                        # Définir la couleur avec un caractère ASCII
                        color = ""

                        # Pour chaque couleur :
                        for c in image.getpixel((j, i)):
                            # Définir la couleur au caractère ASCII correspondant + 40 (nombre dans la table)
                            color += str(chr(c + 40))

                        # Si La dernière couleur, c'est-à-dire le paramètre alpha, est de 255:
                        if color[-1] == str(chr(255 + 40)):
                            # Il est inutile de l'écrire
                            compacted_image[0] += [color[0] + color[1] + color[2]]

                        # Sinon on précise la valeur
                        else:
                            compacted_image[0] += [color]

                return compacted_image

            # On détermine un facteur d'apparition d'une couleur
            def step2(compacted_image):
                compacted_image2 = [[], compacted_image[1]]
                last_color = ""

                # Pour chaque couleur encodée,
                for k in range(len(compacted_image[0])):

                    # Si c'est la première couleur,
                    if len(compacted_image2[0]) == 0:
                        # La couleur précédente est mis à elle même
                        last_color = compacted_image[0][k]
                        # On l'ajoute dans la nouvelle liste d'objets compressés
                        compacted_image2[0] += [last_color]

                    # Si l'élément est égal au précédent,
                    elif compacted_image[0][k] == last_color:

                        # Si le dernier élément est déjà le multiple d'une couleur,
                        if chr(15) in compacted_image2[0][-1]:
                            # On ajoute 1 au multiple
                            compacted_image2[0][-1] = chr(
                                ord(compacted_image2[0][-1].split(chr(15))[0]) + 1
                            ) + chr(15) + compacted_image2[0][-1].split(chr(15))[1]

                        # Sinon
                        else:
                            # On dit que la dernière couleur apparait 2 fois
                            compacted_image2[0][-1] = chr(2 + 40) + chr(15) + compacted_image2[0][-1]

                    # Sinon,
                    else:
                        # On ajoute la couleur à la liste, et on la défini comme la dernière couleur
                        last_color = compacted_image[0][k]
                        compacted_image2[0] += [last_color]

                return compacted_image2

            def step3(image):
                # Combiner toutes les couleurs en 1 str
                compacted_image = ["", image[1]]

                for i in range(len(image[0])):
                    if i == len(image[0]) - 1:
                        compacted_image[0] += image[0][i]

                    else:
                        compacted_image[0] += image[0][i] + chr(16)

                return compacted_image

            return step3(step2(step1()))

        def methode_mc2c(img, alpha: bool = True):
            """Methode Color to Char 2.0

            Les couleurs (entre 0 et 255) sont converties vers le caractère UNICODE correspondant tel que color + 40
            Le caractère signalant la redondance d'1 élément est le caractère UNICODE 35 (#) (dans une ligne)
                Le caractère suivant le # est le caractère UNICODE du multiplicateur de la couleur suivante.
            Le caractère signalant la redondance d'une ligne est le caractère UNICODE 36 ($) (dans une ligne)
            Le caractère UNICODE 37 (%) permet de dire la taille de l'image
            """

            # Convertir chaque couleur avec le nombre associé
            def convert2char(img):
                conversion = []

                # Parcourir les pixels de l'image
                for i in range(size[1]):
                    conversion += [[]]

                    for j in range(size[0]):
                        color = img.getpixel((j, i))
                        r = color[0]
                        g = color[1]
                        b = color[2]
                        a = color[3]

                        if alpha:
                            # Ajouter le code correspondant à la couleur
                            conversion[i] += [chr(r + 40) + chr(g + 40) + chr(b + 40) + chr(a + 40)]
                        else:
                            # Ajouter le code correspondant à la couleur
                            conversion[i] += [chr(r + 40) + chr(g + 40) + chr(b + 40)]

                return conversion

            def assemble_columns(conversion1):
                conversion = []
                last_color = ""
                multiplier = 1

                # Pour chaque ligne
                for i in range(len(conversion1)):
                    conversion += [""]

                    # Pour chaque colonne
                    for j in range(len(conversion1[0])):
                        color = conversion1[i][j]

                        # Si la couleur est la même que la dernière
                        if last_color == color:
                            # On ajoute 1
                            multiplier += 1

                        # Sinon
                        else:
                            # On ajoute la couleur précédente
                            if multiplier > 1:
                                conversion[i] += "#" + str(chr(multiplier + 40)) + last_color
                            elif multiplier <= 1 and last_color:
                                conversion[i] += last_color

                            # On remet le reste à 0
                            multiplier = 1
                            last_color = color

                    # On ajoute la couleur précédente
                    if multiplier > 1:
                        conversion[i] += "#" + str(chr(multiplier + 40)) + last_color
                    else:
                        conversion[i] += last_color

                    # On remet le reste à 0
                    multiplier = 1
                    last_color = ""

                return conversion

            # Assembler les différentes lines en 1
            def assemble_lines(conversion2):
                conversion = ""
                last_line = ""
                multiplier = 1

                for i in range(len(conversion2)):
                    color = conversion2[i]

                    # Si la couleur est la même que la dernière
                    if last_line == color:
                        # On ajoute 1
                        multiplier += 1

                    # Sinon
                    else:
                        # On ajoute la couleur précédente
                        if multiplier > 1:
                            conversion += "$" + str(chr(multiplier + 40)) + last_line
                        elif multiplier <= 1 and last_line:
                            conversion += last_line

                        # On reset le reste
                        multiplier = 1
                        last_line = color

                # On ajoute la couleur précédente
                if multiplier > 1:
                    conversion += "$" + str(chr(multiplier + 40)) + last_line
                elif multiplier <= 1 and last_line:
                    conversion += last_line

                return conversion

            def size_adder(image: str, size: tuple[int, int]):
                return image + "%" + str(chr(size[0] + 40)) + str(chr(size[1] + 40))

            step1 = convert2char(img)
            step2 = assemble_columns(step1)
            step3 = assemble_lines(step2)
            step4 = size_adder(step3, size)

            methode = ""

            if alpha:
                methode = "mc2cA"

            else:
                methode = "mc2c"

            return [step4, methode]

        def methode_mc2hex(img, alpha: bool = True):
            # Convertir chaque couleur avec le nombre associé
            def convert2char(img):
                conversion = []

                # Parcourir les pixels de l'image
                for i in range(size[1]):
                    conversion += [[]]

                    for j in range(size[0]):
                        color = img.getpixel((j, i))
                        r = color[0]
                        g = color[1]
                        b = color[2]
                        a = color[3]

                        if alpha:
                            # Ajouter le code correspondant à la couleur
                            conversion[i] += [chr(r + 40) + chr(g + 40) + chr(b + 40) + chr(a + 40)]
                        else:
                            # Ajouter le code correspondant à la couleur
                            conversion[i] += [chr(r + 40) + chr(g + 40) + chr(b + 40)]

                return conversion

            def assemble_columns(conversion1):
                conversion = []
                last_color = ""
                multiplier = 1

                # Pour chaque ligne
                for i in range(len(conversion1)):
                    conversion += [""]

                    # Pour chaque colonne
                    for j in range(len(conversion1[0])):
                        color = conversion1[i][j]

                        # Si la couleur est la même que la dernière
                        if last_color == color:
                            # On ajoute 1
                            multiplier += 1

                        # Sinon
                        else:
                            # On ajoute la couleur précédente
                            if multiplier > 1:
                                conversion[i] += "#" + str(chr(multiplier + 40)) + last_color
                            elif multiplier <= 1 and last_color:
                                conversion[i] += last_color

                            # On remet le reste à 0
                            multiplier = 1
                            last_color = color

                    # On ajoute la couleur précédente
                    if multiplier > 1:
                        conversion[i] += "#" + str(chr(multiplier + 40)) + last_color
                    else:
                        conversion[i] += last_color

                    # On remet le reste à 0
                    multiplier = 1
                    last_color = ""

                return conversion

            # Assembler les différentes lines en 1
            def assemble_lines(conversion2):
                conversion = ""
                last_line = ""
                multiplier = 1

                for i in range(len(conversion2)):
                    color = conversion2[i]

                    # Si la couleur est la même que la dernière
                    if last_line == color:
                        # On ajoute 1
                        multiplier += 1

                    # Sinon
                    else:
                        # On ajoute la couleur précédente
                        if multiplier > 1:
                            conversion += "$" + str(chr(multiplier + 40)) + last_line
                        elif multiplier <= 1 and last_line:
                            conversion += last_line

                        # On reset le reste
                        multiplier = 1
                        last_line = color

                # On ajoute la couleur précédente
                if multiplier > 1:
                    conversion += "$" + str(chr(multiplier + 40)) + last_line
                elif multiplier <= 1 and last_line:
                    conversion += last_line

                return conversion

            def size_adder(image: str, size: tuple[int, int]):
                return image + "%" + str(chr(size[0] + 40)) + str(chr(size[1] + 40))

            step1 = convert2char(img)
            step2 = assemble_columns(step1)
            step3 = assemble_lines(step2)
            step4 = size_adder(step3, size)

            methode = ""

            if alpha:
                methode = "mc2cA"

            else:
                methode = "mc2c"

            return [step4, methode]

        # mcc = [methode_mcc(), "mcc"]
        mctc = [methode_ctc(), "mctc"]
        mc2cA = methode_mc2c(image)
        mc2c = methode_mc2c(image, False)

        test_list = [mctc, mc2c, mc2cA]

        take_methode = mctc

        for methode in test_list:
            print(methode[1] + " : " + str(len(str(methode[0]))))

            if len(str(methode[0])) < len(str(take_methode[0])):
                take_methode = methode

        return take_methode[0], take_methode[1]

    def uncompress(self, compacted_image, methode):
        image = []

        if methode == "mnc":
            image = compacted_image

        elif methode == "myx":
            for i in range(len(compacted_image)):

                for row in range(compacted_image[i][0]):
                    image += [[]]
                    image[-1] += compacted_image[i][-1]

            image = self.uncompress(image, "my")


        elif methode == "mxy":
            for i in range(len(compacted_image)):

                for row in range(compacted_image[i][0]):
                    image += [[]]
                    image[-1] += compacted_image[i][-1]

            image = self.uncompress(image, "mx")

        elif methode == "mx":
            for i in range(len(compacted_image)):
                image += [[]]

                for j in range(len(compacted_image[i])):

                    for k in range(compacted_image[i][j][0]):
                        image[-1] += [compacted_image[i][j][-1]]

        elif methode == "my":
            for i in range(len(compacted_image)):

                counter = 0

                for j in range(len(compacted_image[i])):

                    for k in range(compacted_image[i][j][0]):
                        if i == 0:
                            image += [[]]
                            image[-1] += [compacted_image[i][j][1]]

                        else:
                            image[counter] += [compacted_image[i][j][1]]

                        counter += 1

        elif methode == "mcc":
            pixels = True
            x = 0
            y = 0

            while pixels:

                for color in compacted_image:

                    for pixel in range(len(compacted_image[color])):

                        if compacted_image[color][pixel] == str(x) + "x" + str(y):
                            image[x] += color
            pass

        elif methode == "mctc":
            def color_finder(color: str):
                ncolor = []
                for char in color:
                    ncolor += [ord(char) - 40]

                return ncolor

            compacted_image = [compacted_image[0].split(chr(16)), compacted_image[1]]
            image = [[]]
            px = 0
            line = 0

            for i in compacted_image[0]:

                if px == int(compacted_image[1].split("x")[0]):
                    image += [[]]
                    line += 1
                    px = 0

                if chr(15) in i:
                    if px + ord(i.split(chr(15))[0]) - 40 > int(compacted_image[1].split("x")[0]):
                        pixels_at_beginning = px + ord(i.split(chr(15))[0]) - 40 - int(compacted_image[1].split("x")[0])
                        pixels_at_end = ord(i.split(chr(15))[0]) - 40 - pixels_at_beginning

                        image[line] += [[pixels_at_end, color_finder(i.split(chr(15))[1])]]

                        image += [[]]
                        line += 1
                        px = pixels_at_beginning

                        image[line] += [[pixels_at_beginning, color_finder(i.split(chr(15))[1])]]

                    else:
                        image[line] += [[ord(i.split(chr(15))[0]) - 40, color_finder(i.split(chr(15))[1])]]
                        px += ord(i.split(chr(15))[0]) - 40

                else:
                    image[line] += [color_finder(i)]
                    px += 1

            return image

        elif methode == "mctc":
            # Séparer les couleurs
            def step3(compacted_image):
                compacted_image = [compacted_image[0].split(chr(16)), compacted_image[1]]

                new_compacted_image = []

                for i in range(len(compacted_image[0])):

                    if chr(15) in compacted_image[0][i]:

                        for j in range(int(ord(compacted_image[0][i].split(chr(15))[0]) - 40)):
                            new_compacted_image += [compacted_image[0][i].split(chr(15))[1]]

                    else:
                        new_compacted_image += [compacted_image[0][i]]

                return [new_compacted_image, compacted_image[1]]

            def step2(compacted_image):
                new_compacted_image = []
                turn = 0
                elements = []

                for i in range(len(compacted_image[0])):
                    turn += 1

                    elements += [compacted_image[0][i]]

                    if turn == int(compacted_image[1].split("x")[0]):
                        new_compacted_image += [elements]

                        elements = []
                        turn = 0

                return new_compacted_image

            def step1(compacted_image):
                image = []

                for i in range(len(compacted_image)):
                    image += [[]]

                    for j in range(len(compacted_image[0])):

                        color = []

                        for c in compacted_image[i][j]:
                            color += [ord(c) - 40]

                        if len(color) == 4:
                            image[i] += [color]

                        else:
                            image[i] += [[color[0], color[1], color[2], 255]]

                return image

            image = step1(step2(step3(compacted_image)))

        elif methode == "mc2c" or methode == "mc2cA":

            def get_size(encoded_img):
                size = encoded_img.split("%")[1]
                size = [ord(size[0]) - 40, ord(size[1]) - 40]

                image = encoded_img.split("%")[0]

                return image, size

            def converter(encoded_img, size, color_quality):
                lines = size[1]
                line_counter = 0

                image = []
                line = []
                line_multiplier = 1

                columns = size[0]
                element_counter = 0

                while line_counter != lines:

                    if encoded_img[0] == "$":
                        line_multiplier = ord(encoded_img[1]) - 40
                        encoded_img = encoded_img[2:]

                    elif encoded_img[0] == "#":
                        multiplier = ord(encoded_img[1]) - 40
                        element_counter += multiplier
                        encoded_img = encoded_img[2:]

                        color = encoded_img[0:color_quality]
                        rgb = []
                        for element in range(len(color)):
                            rgb += [ord(color[element]) - 40]
                        line += [rgb] * multiplier

                        encoded_img = encoded_img[color_quality:]

                    else:
                        element_counter += 1

                        color = encoded_img[0:color_quality]
                        rgb = []
                        for element in range(len(color)):
                            rgb += [ord(color[element]) - 40]
                        line += [rgb]

                        encoded_img = encoded_img[color_quality:]

                    # Si la ligne est pleine
                    if element_counter == columns:
                        # On ajoute 1 ou plus au nombre de lignes
                        line_counter += line_multiplier
                        # On ajoute la ligne à l'image finale
                        image += [line] * line_multiplier

                        line = []
                        line_multiplier = 1
                        element_counter = 0

                return image

            color_panel = 0
            if methode == "mc2c":
                color_panel = 3
            else:
                color_panel = 4

            uncompression_step1, size = get_size(compacted_image)
            image = converter(uncompression_step1, size, color_panel)

        return image


image_path = "../assets/test.png"
converted_img, mth = ImageConverter().compress(image_path)

with open("../check.txt", "w", encoding="utf-8") as f:
    f.write(converted_img)
    f.close()

image = ImageConverter().uncompress(converted_img, mth)

"""
oiseau.jpg              text_test.PNG           test_numwork.jpeg       none.png       
mnc   : 1275815         mnc   :  506142         mnc   :  812536         mnc   :   63120
mxy   : 1480939         mxy   :  460926         mxy   :  960952         mxy   :     110
myx   : 1427987         myx   :  523167         myx   :  947968         myx   :     110
mx    : 1479739         mx    :  460466         mx    :  959842         mx    :    2940
my    : 1426657         my    :  521917         my    :  947133         my    :    2940
mctc  :  454919         mctc  :  128294         mctc  :  273107         mctc  :    1617
mc2cA :  241727         mc2cA :   71707         mc2cA :  144307         mc2cA :      31
mc2c  :  182612         mc2c  :   54663         mc2c  :  108643         mc2c  :      27

tombstone.png           test.png       
mnc   :  213853         mnc   :   43583
mxy   :  117598         mxy   :      92
myx   :  141476         myx   :     114
mx    :  120963         mx    :    1053
my    :  140976         my    :    5297
mctc  :   48831         mctc  :     443
mc2cA :   20517         mc2cA :      21
mc2c  :   13484         mc2c  :      18
"""