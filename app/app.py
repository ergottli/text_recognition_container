# -*- coding: utf-8 -*-

from flask import Flask, request, send_file, url_for, Response, jsonify
import os
from os.path import join, dirname, realpath, normpath
from change import break_text
from werkzeug.utils import secure_filename
import json
import sys

sys.path.append(join(dirname(realpath(__file__)), "tfa"))

from text_recognition import text_rec

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'tmp_upload')

RESULT_FOLDER = join(dirname(realpath(__file__)), 'result')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER


@app.route('/result/<string:filename>', methods=['GET', 'POST'])
def download(filename):
	downloads = join(app.root_path, app.config['RESULT_FOLDER'])
	norm_downloads = normpath(downloads)
	download_file = join(norm_downloads, filename)
	if os.path.exists(download_file):
		res = send_file(download_file, as_attachment=True)
		os.remove(download_file)
	else:
		res = None
	return res


def do_answer(string_answer: str, file_name):
	file_name = file_name.split('.')[0] + "_out.txt"
	if os.path.exists(join(app.config['RESULT_FOLDER'], file_name)):
		out = url_for('download', filename=file_name, _external=True)
	else:
		out = "There is no file %s" % file_name
	answer = json.dumps({"id": "200",
						 "file": out,
						 "result": {"classification": string_answer}},
						ensure_ascii=False, separators=(",", ":"))
	answer = answer.encode('utf-8')
	return answer


@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		filename = secure_filename(file.filename)
		file.save(join(app.config['UPLOAD_FOLDER'], filename))
		string_answer = text_rec(join(app.config['UPLOAD_FOLDER'], filename))
		if not string_answer:
			string_answer = "None"
		break_text(filename, string_answer)
		if os.path.exists(join(app.config['UPLOAD_FOLDER'], filename)):
			os.remove(join(app.config['UPLOAD_FOLDER'], filename))
		return do_answer(string_answer, filename)
	return app.send_static_file('index.html')


if __name__ == '__main__':
	app.run()
