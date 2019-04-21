import pytesseract
from PIL import Image, ImageEnhance


def crop_image_vcode(filename, location, size):
    x, y = location
    w, h = size

    image = Image.open(filename)

    img = image.crop((x, y, x+w, y+h))
    img = img.convert('L')  # 转换模式：L | RGB
    img = ImageEnhance.Contrast(img)  # 增强对比度
    img = img.enhance(2.0)  # 增加饱和度
    img.save("complated.png")
    print("[+] screenshot the vcode image to complated.png")


# crop_image("ocr.png", (544, 117), (115, 55))