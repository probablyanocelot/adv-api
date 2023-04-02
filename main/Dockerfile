FROM python:3.9

# set workdir
WORKDIR /app

# env vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app.py

COPY ./requirements.txt /app/requirements.txt
RUN export LDFLAGS="-L/usr/local/opt/openssl/lib"
RUN pip install -r requirements.txt

# copy project
COPY . /app
# EXPOSE 5000
# RUN ls -la
# RUN chmod 777 /app/docker-entrypoint.sh \
    # && ln -s /app/docker-entrypoint.sh /

# ENTRYPOINT ["/docker-entrypoint.sh"]
# CMD ["run"]
# CMD set -e \
    # && flask db upgrade \
    # && gunicorn -c gunicorn.config.py wsgi:app