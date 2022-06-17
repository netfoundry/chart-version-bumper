FROM python:3.9-bullseye

WORKDIR /app

COPY auto_bump ./

COPY ./requirements.txt ./

COPY entrypoint.sh ./entrypoint.sh

RUN python -m pip install --upgrade pip

RUN pip install requirements.txt

ENTRYPOINT ["./entrypoint.sh"]