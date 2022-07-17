FROM python:3-alpine as build

RUN mkdir -p /output \
    && pip install --target /output \
        requests \
    && rm -rf /output/*-*info

ADD src/* /output/

FROM python:3-alpine

ENV TZ=Europe/Berlin
COPY --from=build /output /app

ENTRYPOINT [ "python", "-u", "/app/main.py" ]