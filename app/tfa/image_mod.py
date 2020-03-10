try:
    import cv2
    import pytesseract
    import numpy as np
    from PIL import Image as PI
    from pdf2image import convert_from_path
    from pdf2image.exceptions import (
        PDFInfoNotInstalledError,
        PDFPageCountError,
        PDFSyntaxError
    )
except ImportError:
    raise ImportError('ImportError')


def __get_text_from_pdf(image: str, lang_arg):
    images = convert_from_path(image, fmt='jpeg')
    res = str()
    for img in images:
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        res = res + (pytesseract.image_to_string(img, lang=lang_arg))
    return res


def convert_image_to_string(image: str, lang_arg='rus', ext=None):
    img = cv2.imread(image)
    if ext == 'pdf':
        return __get_text_from_pdf(image, lang_arg)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = pytesseract.image_to_string(img, lang=lang_arg)
    return res
