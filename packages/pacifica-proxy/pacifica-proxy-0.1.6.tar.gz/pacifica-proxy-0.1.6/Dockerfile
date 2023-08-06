FROM python:3.8

WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir .
RUN pip install --no-cache-dir uwsgi
EXPOSE 8180
ENTRYPOINT ["/bin/bash", "/usr/src/app/entrypoint.sh"]
