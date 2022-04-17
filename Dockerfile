FROM python:3.9-alpine3.15

WORKDIR /home/code

RUN apk add --no-cache ffmpeg

COPY ./requirements/prod.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY . /home/code/

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000