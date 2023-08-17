FROM python:3.8-slim-buster
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 unzip -y && pip install -r requirements.txt
RUN pip install -r requirements.txt
CMD ["python","app.py"]