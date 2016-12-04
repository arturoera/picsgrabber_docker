FROM python:2.7

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        mysql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY picsgrabber_src/requirements.txt ./
RUN pip install -r requirements.txt
COPY picsgrabber_src/ .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]