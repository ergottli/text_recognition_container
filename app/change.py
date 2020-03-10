import os
from os.path import dirname, realpath


UPLOAD_FOLDER = os.path.join(dirname(realpath(__file__)), 'tmp_upload')

RESULT_FOLDER = os.path.join(dirname(realpath(__file__)), 'result')


def break_text(filename, string_answer):
    input_file = os.path.join(UPLOAD_FOLDER, filename)
    f = open(os.path.join(RESULT_FOLDER, filename.split('.')[0] + "_out.txt"), 'w', encoding="utf-8")
    f.write(string_answer)
    return "OK"
