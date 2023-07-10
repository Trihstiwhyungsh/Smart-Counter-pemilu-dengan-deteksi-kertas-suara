FROM python:3.8.16-alpine3.17
RUN apk --no-cache update && \
    apk add --no-cache --update-cache gfortran build-base libpng-dev \
    openblas-dev cmake automake gcc lapack-dev
WORKDIR /app
COPY ./requirements/prod.txt /app/requirements.txt
# RUN /usr/local/bin/python -m pip install --upgrade pip
RUN python3 -m venv /opt/venv
RUN . /opt/venv/bin/activate
RUN pip install -r requirements.txt
RUN python migration.py
COPY . .
EXPOSE 8000
CMD ["gunicorn", "--bind 0.0.0.0:8000", "--workers=5", "--threads=2", "main:app"]