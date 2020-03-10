from image_mod import convert_image_to_string
from text_mod import receive_text_from_file
from tikapp import TikaApp
import os

# Supported file types
text_files = 'text/plain', 'application/msword',\
             'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.ms-outlook',\
             'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation',\
             'application/pdf', 'application/vnd.oasis.opendocument.formula', 'text/html', 'application/xml',\
             'application/java', 'application/java-archive'
image_files = 'image/bmp', 'image/x-portable-anymap', 'image/png', 'image/jpeg', 'image/pjpeg',\
              'image/jpeg', 'image/pjpeg', 'image/tiff', 'image/gif'

tika_client = TikaApp(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'src', 'tika-app-1.22.jar'))


def text_rec(path: str, lang='rus'):
    if not os.path.exists(path):
        return None
    content_type = tika_client.detect_content_type(path)
    if content_type in text_files:
        return receive_text_from_file(path, ext=content_type.split('/')[-1])
    elif content_type in image_files:
        return convert_image_to_string(path, lang_arg=lang, ext=content_type.split('/')[-1])
    else:
        return None
