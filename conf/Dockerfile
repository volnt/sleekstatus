FROM ubuntu

MAINTAINER Florent Espanet <florent.esp@gmail.com>

# Dependencies
RUN apt-get update
RUN apt-get install -y unzip nginx gunicorn supervisor
RUN apt-get install -y python python-dev python-distribute python-pip

# Add the application to the docker instance
ADD sleekstatus /sleekstatus/
ADD config.py /sleekstatus/app/config.py
ADD nginx.conf /etc/nginx/sites-available/watchfulhawk
ADD supervisord.conf /etc/supervisor/conf.d/
WORKDIR /sleekstatus/

# Forward the web port
EXPOSE 80

# Install the application
RUN pip install -e /sleekstatus/

# Configure nginx
RUN ln -s /etc/nginx/sites-available/watchfulhawk /etc/nginx/sites-enabled/watchfulhawk
RUN rm /etc/nginx/sites-enabled/default
RUN service nginx restart

CMD supervisord