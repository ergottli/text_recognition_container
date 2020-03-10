from tikapp import TikaApp
from image_mod import convert_image_to_string
import os


tika_client = TikaApp(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'src', 'tika-app-1.22.jar'))


def receive_text_from_file(path: str, ext=None):
    text = tika_client.extract_only_content(path)
    if text == "" and ext == 'pdf':
        return convert_image_to_string(path, ext=ext)
    return text

