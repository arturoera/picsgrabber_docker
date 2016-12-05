FROM python:2.7
MAINTAINER Arturo Ochoa <arturo.era@gmail.com>

# Enable production settings by default; for development, this can be set to
# `false` in `docker run --env`
ENV DJANGO_PRODUCTION=true

# Set terminal to be noninteractive
ENV DEBIAN_FRONTEND noninteractive

# Enable MySQL root user creation without interactive input
RUN echo 'mysql-server mysql-server/root_password password devrootpass' | debconf-set-selections
RUN echo 'mysql-server mysql-server/root_password_again password devrootpass' | debconf-set-selections

# Install packages
RUN apt-get update && apt-get install -y \
    git \
    mysql-client \
    mysql-server \
    nginx \
    supervisor \
    vim


# Handle urllib3 InsecurePlatformWarning
RUN apt-get install -y libffi-dev libssl-dev libpython2.7-dev
RUN pip install requests[security] ndg-httpsclient pyasn1

# Configure Django project
ADD . /code
RUN mkdir /djangomedia
RUN mkdir /static
RUN mkdir /logs
RUN mkdir /logs/nginx
RUN mkdir /logs/gunicorn
WORKDIR /code
RUN pip install -r picsgrabber_src/requirements.txt
RUN chmod ug+x /code/docker_files/initialize.sh

# Expose ports
# 80 = Nginx
# 8000 = Gunicorn
# 3306 = MySQL
EXPOSE 80 8000 3306

# Configure Nginx
RUN ln -s /code/docker_files/nginx.conf /etc/nginx/sites-enabled/django_docker.conf
RUN rm /etc/nginx/sites-enabled/default

# Run Supervisor (i.e., start MySQL, Nginx, and Gunicorn)
COPY docker_files/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]
