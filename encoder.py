import cv2
import numpy as np

def coding_text(text)->str:
    """
    Кодирование текста в восьмеричную (начиная с 1) систему
    :param text: Текст
    :return: Кодированный текст, где каждый символ - 4 цифры
    """
    sp = ["".join(list(str(int(j)+1) for j in str(format(ord(i), "o")))) for i in text]
    for i, e in enumerate(sp):
        if len(e) < 4:
            sp[i] = ("1"*(4-len(e)))+e
    return "".join(sp)

def decoding_text(symbols="")->str:
    """
    Декодирование текста из восьмеричной системы (начиная с 1)
    :param symbols: символы
    :return: закодированную букву
    """
    symbols = symbols.removeprefix("1")
    symbols = symbols.removeprefix("1")
    symbols = symbols.removeprefix("1")
    symbols = "".join(str(int(i)-1) for i in symbols)
    num = int(symbols, 8)
    return chr(num)



def create_secret_key(img_origin, sistem)->str:
    """
    Создает секретный ключ на основе массива.
    :param img_origin: изображение для шифрования
    :param sistem: система исчисления
    :return: секретный ключ
    """
    s = chr(sistem+97) + "".join([chr(int(i)+97) for i in img_origin])

    return s



def undecode_secret_key(key)->tuple[int, np.array]:
    """
    Возвращает массив по ключу
    :param key: секретный ключ
    :return: система исчисления, массив
    """
    return ord(key[0])-97, np.array([ord(i)-97 for i in key[1:]])



def code_image(img, text, system)->tuple[str, str, int]:
    """
    Кодирование всего изображения
    :param img: Изображение
    :param text: Текст
    :param system: Система исчисления кодирования. Чем меньше, тем менее заметно, но тем больше места
    :return: Секретный ключ, имя файла, упущенные символы (0-все сообщение закодировано)
    """
    shape = img.shape

    img_orgin = img.copy()

    coded_text = coding_text(text)

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
        loose = (len(coded_text) - idx_sym) // 4

    print(img.shape)


    code = (system+1) - (img_orgin.flatten() - img.flatten())
    code = "".join(map(str, code)).replace(f"{system+1}","")
    print(coded_text==code)

    return create_secret_key(img_orgin.flatten(), system), "img_result.png", loose



if __name__ == "__main__":
    system = 8
    f = open("text.txt", "r", encoding="UTF-8")
    text = f.read()
    f.close()

    img = cv2.imread("img.png")

    key, f, l = code_image(img, text, system)
    print(l)

    with open("secret.txt", "w", encoding="UTF-32") as f:
        f.write(key)


    #TODO: проверить символы loose