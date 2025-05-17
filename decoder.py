import cv2
from encoder import decoding_text

def decode(file_origin, image, system, coded_sistem)->str:
    """
    Декодирует изображение
    :param file_origin: Оригинальное изображение
    :param image: Изображение
    :param system: Система кодирования
    :param coded_sistem: Длина кодирования одного символа
    :return: Закодированный текст
    """



    img = cv2.imread(image)
    img_origin = cv2.imread(file_origin).flatten()[:img.size]

    code = (system + 1) - (img_origin - img.flatten())
    code = "".join(str(x) for x in code if x != system + 1)
    text = decoding_text(coded_sistem, code )

    return text


if __name__ == "__main__":

    info_f = open("secret.txt", "r", encoding="UTF-8")
    coded_sistem, sistem, origin = info_f.read().split()
    coded_sistem = int(coded_sistem)
    sistem = int(sistem)

    r = decode(origin, "img_result.png", sistem, coded_sistem)
    f = open("text-decoded.txt","w", encoding="UTF-8")
    f.write(r)
    f.close()




