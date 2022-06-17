FROM ubuntu:latest

WORKDIR /app

COPY auto_bump ./

COPY entrypoint.sh ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]