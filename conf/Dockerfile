FROM ubuntu

MAINTAINER Florent Espanet <florent.esp@gmail.com>

# Dependencies
RUN apt-get update
RUN apt-get install -y unzip nginx
RUN apt-get install -y python python-dev python-distribute python-pip

# Add the application to the docker instance
ADD sleekstatus /sleekstatus/
ADD config.py /sleekstatus/app/config.py
WORKDIR /sleekstatus/

# Forward the web port
EXPOSE 80

# Install the application
RUN pip install -e /sleekstatus/

CMD python run.py