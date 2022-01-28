FROM python:3.10-alpine
LABEL maintainer="Nisarg Joshi"

# Setting PYTHONUNBUFFERED to a non empty value ensures that the python output is sent straight to terminal (e.g. your container log) without being first buffered and that you can see the output of your application (e.g. django logs) in real time.
ENV PYTHONUNBUFFERED 1

RUN echo "https://mirrors.sustech.edu.cn/alpine/v3.15/main" > /etc/apk/repositories ; \
    echo "https://mirrors.sustech.edu.cn/alpine/v3.15/community" >> /etc/apk/repositories ;

RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers libffi-dev libressl-dev

COPY ./requirements.txt /requirements.txt
COPY ./app /app

WORKDIR /app
EXPOSE 8000

RUN python -m venv venv
RUN source venv/bin/activate
RUN pip install --upgrade pip
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r /requirements.txt
RUN apk del .tmp-deps

RUN adduser --disabled-password --no-create-home app

USER app
