FROM python:3.9

WORKDIR /home/code

apk add --no-cache ffmpeg
COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY . /home/code/

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000