import cv2
from encoder import undecode_secret_key, decoding_text

def decode(SECRET_KEY, image)->str:
    """
    Декодирует изображение
    :param SECRET_KEY: Секретный ключ
    :param image: Изображение
    :return: Закодированный текст
    """
    f = open(SECRET_KEY, "r", encoding="UTF-32")
    SECRET_KEY = f.read()
    f.close()

    img = cv2.imread(image)
    system, img_origin = undecode_secret_key(SECRET_KEY)

    code = (system + 1) - (img_origin - img.flatten())
    code = "".join(map(str, code)).replace(f"{system + 1}", "")

    text = ""
    for idx in range(0, len(code), 4):
        sym = code[idx:idx+4]
        text+=decoding_text(sym)
    return text



r = decode("secret.txt", "img_result.png")
print(r)




