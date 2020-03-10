# Previously used
# python3-dev build-essential libssl-dev libffi-dev
#python3-setuptools python3-venv 

FROM		debian:latest
RUN		apt update && apt upgrade -y && \
		apt install -y default-jre python3-pip libsm6 libxext6 libxrender-dev && \
		apt install -y poppler-utils tesseract-ocr tesseract-ocr-rus > /requirements_apt.txt
EXPOSE		5000
COPY		app /home/app
WORKDIR		/home/app
#RUN		python3 -m venv venv
#RUN		source venv/bin/activate
RUN		pip3 install  gunicorn flask numpy pillow pdf2image pytesseract opencv-python tika-app
RUN		pip3 freeze > requirements_pip3.txt
#add out flask app to e\ENV
RUN		echo "export FLASK_APP=app.py" >> ~/.profile
ENTRYPOINT	["gunicorn", "-t", "604800","-b", "0.0.0.0:5000", "app:app"]
