import cv2
import numpy as np

def coding_text(text)->tuple[int, str]:
    """
    Кодирование текста в восьмеричную (начиная с 1) систему
    :param text: Текст
    :return: Размер символа, Кодированный текст, где каждый символ определенной длины
    """

    sp = ["".join(list(str(int(j)+1) for j in str(format(ord(i), "o")))) for i in text]
    coded_sistem = len(max(sp, key=len))

    for i, e in enumerate(sp):
        sp[i] = e.rjust(coded_sistem, "1")

    return coded_sistem, "".join(sp)


def decoding_text(coded_sistem, code="")->str:
    """
    Декодирование текста из восьмеричной системы (начиная с 1)
    :param coded_sistem символы кодировки символа
    :param symbols: код
    :return: разкодированный текст
    """
    text = ""
    for idx in range(0, len(code), coded_sistem):
        symbols = code[idx:idx+coded_sistem]
        symbols = symbols.lstrip("1")

        if len(symbols) == 0:
            symbols = "1"

        symbols = "".join(str(int(i)-1) for i in symbols)
        num = int(symbols, 8)
        text += chr(num)
    return text





def code_image(img, text, system)->tuple[int,str, int]:
    """
    Кодирование всего изображения
    :param img: Изображение
    :param text: Текст
    :param system: Система исчисления кодирования. Чем меньше, тем менее заметно, но тем больше места
    :return: длина кодирования одного символа, имя файла с закодированным посланием, упущенные символы (0-все сообщение закодировано)
    """
    shape = img.shape

    img_orgin = img.copy()

    coded_sistem, coded_text = coding_text(text)

    idx_sym = 0

    full_coded = False

    for i in range(shape[0]):
        for j in range(shape[1]):
            for z in range(shape[2]):
                symbol = int(coded_text[idx_sym])
                if int(img[i][j][z]) - system -1 < 0:
                    continue
                idx_sym+=1
                img[i][j][z] -=  system + 1
                img[i][j][z] += symbol
                if idx_sym == len(coded_text):
                    full_coded = True
                    break
            if full_coded:
                break
        if full_coded:
            break

    cv2.imwrite("img_result.png", img)

    loose = 0
    if not full_coded:

        loose = (len(coded_text) - idx_sym) // coded_sistem

    # print(coded_text[:100])
    code = (system+1) - (img_orgin.flatten() - img.flatten())
    code = "".join(str(x) for x in code if x != system + 1)


    print("CORRECT FILE:",coded_text==code)


    return coded_sistem, "img_result.png", loose



if __name__ == "__main__":
    system = 8

    f = open("all-Warp-and-Piece.txt", "r", encoding="UTF-8") # текст
    img_name = "img.png"# изображение

    text = f.read()
    f.close()

    img = cv2.imread(img_name)

    coded_sistem, f, l = code_image(img, text, system)
    print("LOST SYMBOLS (AVERAGE)", l)
    print("CODE SISTEM:", coded_sistem)


    f1 = open("secret.txt", "w", encoding="UTF-8")
    f1.write(f"{coded_sistem} {system} {img_name}")
    f1.close()


    #TODO: проверить символы loose